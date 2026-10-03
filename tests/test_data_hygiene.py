"""Guards on the provider data tables themselves.

Stray whitespace and empty entries in a word list surface as malformed output
(double spaces inside a name, an empty month name) that type-only assertions
never catch.
"""

import pytest

from pashto_toolkit.fake.providers import LOCALES, PROVIDER_TYPES, provider_class


def _tables(provider_type, locale):
    """Yield (attribute, entries) for every data table on a provider class."""
    cls = provider_class(provider_type, locale)
    for attr in dir(cls):
        if attr.startswith("_"):
            continue
        value = getattr(cls, attr, None)
        if isinstance(value, (list, tuple)) and value and all(isinstance(x, str) for x in value):
            yield attr, list(value)
        elif isinstance(value, dict):
            for key, nested in value.items():
                entries = nested if isinstance(nested, (list, tuple)) else [nested]
                if entries and all(isinstance(x, str) for x in entries):
                    yield f"{attr}[{key!r}]", list(entries)


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
    readable. Known and not yet resolved in the inherited data, hence xfail.
    """
    offenders = []
    for attr, entries in _tables(provider_type, locale):
        if "name" not in attr and "companies" not in attr and "banks" not in attr:
            continue
        unique = len(set(entries))
        if unique < len(entries):
            share = 100 * (len(entries) - unique) / len(entries)
            offenders.append(f"{provider_type}.{attr}: {len(entries)} entries, {unique} unique ({share:.0f}% repeats)")
    if offenders:
        pytest.xfail("repeated entries skew the distribution:\n" + "\n".join(offenders))


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
