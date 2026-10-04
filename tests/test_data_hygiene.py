"""Guards on the provider data tables themselves.

Stray whitespace and empty entries in a word list surface as malformed output
(double spaces inside a name, an empty month name) that type-only assertions
never catch.
"""

import pytest

from pashto_toolkit.fake.providers import LOCALES, PROVIDER_TYPES, provider_class


def _strings(obj):
    """Every string anywhere inside a value, including dictionary keys.

    Keys matter: ``color.all_colors`` holds the Pashto colour names as keys
    and the hex codes as values, so walking only the values misses the text.
    """
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for key, value in obj.items():
            yield from _strings(key)
            yield from _strings(value)
    elif isinstance(obj, (list, tuple, set, frozenset)):
        for item in obj:
            yield from _strings(item)
    else:
        for attr in ("name", "prefixes"):       # CreditCard carries strings
            if hasattr(obj, attr):
                yield from _strings(getattr(obj, attr))


def _tables(provider_type, locale):
    """Yield (attribute, entries) for every data table on a provider class."""
    cls = provider_class(provider_type, locale)
    for attr in dir(cls):
        if attr.startswith("_"):
            continue
        value = getattr(cls, attr, None)
        if callable(value):
            continue
        if isinstance(value, (list, tuple)) and value and all(isinstance(x, str) for x in value):
            yield attr, list(value)
        elif isinstance(value, dict):
            keys = [k for k in value if isinstance(k, str)]
            if keys:
                yield f"{attr} keys", keys
            for key, nested in value.items():
                entries = list(_strings(nested))
                if entries:
                    yield f"{attr}[{key!r}]", entries


@pytest.mark.parametrize("locale", LOCALES)
@pytest.mark.parametrize("provider_type", PROVIDER_TYPES)
def test_no_stray_whitespace_in_data(provider_type, locale):
    offenders = [
        f"{provider_type}.{attr}: {entry!r}"
        for attr, entries in _tables(provider_type, locale)
        for entry in entries
        if entry.strip() and (entry != entry.strip() or "  " in entry)
    ]
    assert not offenders, "stray whitespace in provider data:\n" + "\n".join(offenders)


@pytest.mark.parametrize("locale", LOCALES)
@pytest.mark.parametrize("provider_type", PROVIDER_TYPES)
def test_no_duplicate_entries_in_name_tables(provider_type, locale):
    """Repeated entries make those values proportionally more likely.

    Reported as a count rather than a list of names, so the failure stays
    readable.
    """
    offenders = []
    for attr, entries in _tables(provider_type, locale):
        if "name" not in attr and "companies" not in attr and "banks" not in attr:
            continue
        unique = len(set(entries))
        if unique < len(entries):
            share = 100 * (len(entries) - unique) / len(entries)
            offenders.append(f"{provider_type}.{attr}: {len(entries)} entries, {unique} unique ({share:.0f}% repeats)")
    assert not offenders, "repeated entries skew the distribution:\n" + "\n".join(offenders)


@pytest.mark.parametrize("locale", LOCALES)
def test_month_names_index_cleanly(locale):
    """month_name() indexes this tuple by date.month, so 1..12 must be filled."""
    month_names = provider_class("date_time", locale).month_names
    assert len(month_names) == 13, f"expected a 13-slot tuple, got {len(month_names)}"
    assert all(month_names[i] for i in range(1, 13)), f"empty month slot in {month_names}"
    assert len(set(month_names[1:])) == 12, "duplicate month names"


@pytest.mark.parametrize("locale", LOCALES)
def test_day_names_cover_the_week(locale):
    day_names = provider_class("date_time", locale).day_names
    assert len(day_names) == 7
    assert len(set(day_names)) == 7
    assert all(day_names)


@pytest.mark.parametrize("locale", LOCALES)
def test_province_tables_agree(locale):
    """district() and city() key off the province name, so the spellings must match."""
    address = provider_class("address", locale)
    provinces = set(address.provinces)
    assert len(address.provinces) == 34, f"expected 34 provinces, got {len(address.provinces)}"
    assert len(provinces) == 34, "duplicate province names"

    for table in ("cities", "districts"):
        keys = set(getattr(address, table))
        assert not keys - provinces, f"{table} keys that are not provinces: {sorted(keys - provinces)}"
        assert not provinces - keys, f"provinces missing from {table}: {sorted(provinces - keys)}"


@pytest.mark.parametrize("locale", LOCALES)
def test_district_follows_the_requested_province(locale):
    """A province with no districts silently returns the province name instead."""
    from pashto_toolkit import PashtoFaker

    fake = PashtoFaker(locale)
    address = provider_class("address", locale)
    for province, districts in address.districts.items():
        value = fake.district(province)
        assert value in districts, f"{province}: got {value!r}, not one of its districts"


@pytest.mark.parametrize("locale", LOCALES)
def test_emails_and_usernames_are_always_well_formed(locale):
    """Regression: two-word names such as 'Bakht Awar' left a space in the address."""
    import re

    from pashto_toolkit import PashtoFaker

    fake = PashtoFaker(locale, seed=0)
    address = re.compile(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}")
    username = re.compile(r"[a-z0-9._]+")

    bad_emails = {value for value in (fake.email() for _ in range(3000)) if not address.fullmatch(value)}
    assert not bad_emails, f"malformed email addresses: {sorted(bad_emails)[:5]}"

    bad_names = {value for value in (fake.user_name() for _ in range(3000)) if not username.fullmatch(value)}
    assert not bad_names, f"malformed usernames: {sorted(bad_names)[:5]}"


@pytest.mark.parametrize("locale", LOCALES)
def test_pricetags_never_start_with_a_zero(locale):
    """Regression: the formats used `#` for the leading digit, giving '0,316'."""
    import re

    from pashto_toolkit import PashtoFaker

    fake = PashtoFaker(locale, seed=1)
    offenders = set()
    for _ in range(3000):
        value = fake.pricetag()
        digits = re.search(r"[\d,]+", value)
        assert digits, f"no amount in {value!r}"
        if digits.group().startswith("0"):
            offenders.add(value)
    assert not offenders, f"amounts with a leading zero: {sorted(offenders)[:5]}"


@pytest.mark.parametrize("locale", LOCALES)
def test_bics_are_a_valid_length_and_shape(locale):
    """Regression: a 2-character branch code made swift(11) 10 characters,
    and swift_code() left out the country code entirely."""
    import re

    from pashto_toolkit import PashtoFaker

    fake = PashtoFaker(locale, seed=5)
    pattern = re.compile(r"[A-Z]{4}AF[A-Z0-9]{2}([A-Z0-9]{3})?")
    for _ in range(1000):
        assert len(fake.swift(8)) == 8
        assert len(fake.swift(11)) == 11
        assert len(fake.swift_code()) == 11
        for value in (fake.swift(8), fake.swift(11), fake.swift_code()):
            assert pattern.fullmatch(value), f"not a valid BIC: {value}"

    branch_codes = provider_class("bank", locale).swift_branch_codes
    assert all(len(code) == 3 for code in branch_codes), f"BIC branch codes must be 3 chars: {branch_codes}"


@pytest.mark.parametrize("locale", LOCALES)
def test_msisdn_is_a_full_afghan_number(locale):
    """Regression: it was 12 digits. Afghan E.164 is 93 plus nine digits."""
    from pashto_toolkit import PashtoFaker

    fake = PashtoFaker(locale, seed=5)
    for _ in range(1000):
        value = fake.msisdn()
        assert value.isdigit(), value
        assert len(value) == 11, f"expected 11 digits, got {len(value)}: {value}"
        assert value.startswith("937"), value


@pytest.mark.parametrize("locale", LOCALES)
def test_names_never_stack_two_honorifics(locale):
    """Regression: output like 'بی بی بی بی غلجي' and 'Agha Wazir Umar'.

    Several words are both a title and a given name, so prepending a title
    unconditionally produced two in a row.
    """
    from pashto_toolkit import PashtoFaker

    person = provider_class("person", locale)
    titles = set(person.prefixes_male) | set(person.prefixes_female)
    fake = PashtoFaker(locale, seed=3)

    offenders = set()
    for _ in range(20000):
        tokens = fake.name().split()
        # Two leading titles only matters when a third token follows; a
        # two-token name is first name plus surname, and words like Khan are
        # legitimate surnames.
        if len(tokens) >= 3 and tokens[0] in titles and tokens[1] in titles:
            offenders.add(" ".join(tokens))
    assert not offenders, f"names with stacked honorifics: {sorted(offenders)[:5]}"


def test_pashto_surnames_are_not_female_given_names():
    """Regression: last_names held فاطمه, نجمه, ليلا and similar.

    An Afghan second name follows the father's or husband's name, so it is
    not a female given name.
    """
    person = provider_class("person", "pa_AF")
    surnames = set(person.last_names)
    female_given = {"شکيبا", "نسرين", "زينب", "مريم", "فاطمه", "ليلا", "زهرا",
                    "عایشه", "نرگس", "فرشته", "نجمه", "شيرين"}
    assert not (surnames & female_given), f"female given names used as surnames: {sorted(surnames & female_given)}"


def test_pashto_surnames_hold_no_place_names_or_common_nouns():
    """Regression: غور and قندهار are places; زوی and فرزند mean son and child."""
    person = provider_class("person", "pa_AF")
    surnames = set(person.last_names)
    wrong = {"غور", "قندهار", "زوی", "فرزند"}
    assert not (surnames & wrong), f"not surnames: {sorted(surnames & wrong)}"
    # The correct derived forms are the ones that belong.
    assert "کندهاري" in surnames


def test_pashto_surnames_have_no_duplicates():
    person = provider_class("person", "pa_AF")
    surnames = list(person.last_names)
    assert len(surnames) == len(set(surnames)), "duplicate surnames skew the distribution"


@pytest.mark.parametrize("provider_type", PROVIDER_TYPES)
def test_pashto_data_uses_pashto_letter_forms(provider_type):
    """The data is written in standard Afghan Pashto orthography.

    Arabic and Persian look-alikes are not used medially: ``ي`` (U+064A) only
    word-finally, where it is grammatical, and never ``ك`` (U+0643),
    ``گ`` (U+06AF) or ``ہ`` (U+06C1).
    """
    forbidden = {"ك": "ك Arabic kaf, use ک U+06A9",
                 "گ": "گ Persian gaf, use ګ U+06AB",
                 "ہ": "ہ Urdu heh, use ه U+0647"}
    offenders = []
    for attr, entries in _tables(provider_type, "pa_AF"):
        for entry in entries:
            for char, why in forbidden.items():
                if char in entry:
                    offenders.append(f"{provider_type}.{attr}: {entry!r} contains {why}")
            for word in entry.split():
                for index, char in enumerate(word):
                    if char == "ي" and index != len(word) - 1:
                        offenders.append(f"{provider_type}.{attr}: {entry!r} has a medial ي; use ی U+06CC")
    assert not offenders, "non-standard letter forms:\n" + "\n".join(offenders[:10])


@pytest.mark.parametrize("provider_type", PROVIDER_TYPES)
def test_alef_madda_is_preserved(provider_type):
    """``آ`` must not be folded to ``ا``.

    Place names such as فيض آباد, اسدآباد and دوآب carry it, as do words like
    آشپز. A lexicon-driven normalizer will fold it; the data must not.
    """
    folded = {"اباد", "اشپز", "اسماني", "اغلې", "اقچه"}
    offenders = [
        f"{provider_type}.{attr}: {entry!r}"
        for attr, entries in _tables(provider_type, "pa_AF")
        for entry in entries
        if any(word in folded for word in entry.split())
    ]
    assert not offenders, "alef-madda was folded away:\n" + "\n".join(offenders)


#: Words genuinely used for either sex in Afghanistan, so they belong in both
#: name pools: fortune, meadow, plane tree, river, jewel, flower, covenant.
UNISEX_LATIN = {"Bakht", "Chaman", "Chinar", "Darya", "Gohar", "Gul", "Paiman", "Ugay"}
UNISEX_PASHTO = {"امید", "بخت", "دریا", "سپین ګل", "لمر", "پیمان", "چمن", "چنار", "ښائسته", "ګل"}


def test_the_name_pools_only_overlap_on_unisex_names():
    """Regression: the Latin 'male' pool was a merge of male and female names.

    Spozmai (moon), Malalai, Muska (smile), Brekhna (lightning), Ghuncha
    (bud), Zaituna (olive) and 125 more women's names sat in it, so
    simple_profile() produced records like sex 'M' named 'Zaituna Wahidi'.
    """
    person = provider_class("person", "en_AF")
    male = set(person.pashto_male_first_names) | set(person.tajik_male_first_names)
    female = set(person.pashto_female_first_names) | set(person.tajik_female_first_names)
    unexpected = (male & female) - UNISEX_LATIN
    assert not unexpected, f"names in both pools that are not unisex: {sorted(unexpected)}"

    pashto = provider_class("person", "pa_AF")
    male_ps = set(pashto.pashto_male_first_names)
    female_ps = set(pashto.pashto_female_first_names)
    unexpected_ps = (male_ps & female_ps) - UNISEX_PASHTO
    assert not unexpected_ps, f"Pashto names in both pools that are not unisex: {sorted(unexpected_ps)}"


def test_known_womens_names_are_not_in_the_male_pool():
    """A sample of unmistakable women's names, pinned by hand."""
    known = {
        "Spozmai", "Malalai", "Muska", "Brekhna", "Zaituna", "Khatol", "Ghuncha",
        "Mina", "Durkhanai", "Wagma", "Nazo", "Shahlalai", "Shaperai", "Palwasha",
        "Zarghuna", "Gulalai", "Kashmala", "Banafsha", "Farishta", "Bibi",
    }
    for locale, male_attrs in (
        ("en_AF", ("pashto_male_first_names", "tajik_male_first_names")),
        ("pa_AF", ("male_first_names",)),
    ):
        person = provider_class("person", locale)
        male = set().union(*(set(getattr(person, attr)) for attr in male_attrs))
        leaked = sorted(known & male)
        assert not leaked, f"{locale}: women's names in the male pool: {leaked}"


@pytest.mark.parametrize("locale", LOCALES)
def test_profiles_are_gender_consistent(locale):
    """A record's username must come from the pool matching its sex."""
    from pashto_toolkit import PashtoFaker

    person = provider_class("person", locale)
    male_attr = "male_first_names" if locale == "pa_AF" else "pashto_male_first_names"
    female_attr = "female_first_names" if locale == "pa_AF" else "pashto_female_first_names"
    male = {n.lower() for n in getattr(person, male_attr)}
    female = {n.lower() for n in getattr(person, female_attr)}

    fake = PashtoFaker(locale, seed=7)
    mismatches = []
    for _ in range(3000):
        record = fake.simple_profile()
        stem = record["username"].split(".")[0]
        if record["sex"] == "F" and stem in male - female:
            mismatches.append(record)
        elif record["sex"] == "M" and stem in female - male:
            mismatches.append(record)
    # The Tajik pools are a separate source, so allow a small residue.
    assert len(mismatches) <= 15, f"{len(mismatches)}/3000 gender mismatches, e.g. {mismatches[:3]}"


def test_pashto_jobs_are_occupations_not_conditions():
    """Regression: the list held کوروالۍ, which reads as "blindness".

    The suffixes -والی, -توب and -تیا form an abstract noun — a state or
    quality — so a word ending in one is not a person's occupation.
    """
    jobs = provider_class("job", "pa_AF").jobs
    offenders = [job for job in jobs if job.endswith(("والی", "والۍ", "توب", "تیا"))]
    assert not offenders, f"abstract nouns in the job list, not occupations: {offenders}"
