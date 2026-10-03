"""Content tests for the Pashto locale.

These assert the *script and shape* of what comes out, not just that a string
came out at all, so a provider that silently falls back to Faker's en_US data
fails here instead of passing.
"""

import re

import pytest

from conftest import assert_latin, assert_pashto

REPEAT = 30


@pytest.mark.parametrize(
    "formatter",
    [
        "name",
        "name_male",
        "name_female",
        "first_name",
        "first_name_male",
        "first_name_female",
        "last_name",
        "prefix",
        "province",
        "city",
        "district",
        "street",
        "street_name",
        "state",
        "administrative_unit",
        "company",
        "company_suffix",
        "job",
        "color_name",
        "bank_name",
        "word",
        "sentence",
        "paragraph",
        "credit_card_provider",
        "month_name",
        "day_of_week",
    ],
)
def test_formatter_returns_pashto(pa, formatter):
    for _ in range(REPEAT):
        assert_pashto(getattr(pa, formatter)(), f"pa_AF.{formatter}")


def test_address_is_pashto_with_a_postcode(pa):
    for _ in range(REPEAT):
        value = pa.address()
        assert re.search(r"\d{5}", value), f"no postcode in {value!r}"
        # The street/district/city parts are Pashto; digits are ASCII.
        assert not re.search(r"[A-Za-z]", value), f"Latin letters in {value!r}"


def test_city_follows_the_province_when_one_is_given(pa):
    province = "کابل"
    assert pa.city(province) == pa.city(province), "city() is not a function of its province"


def test_postcode_is_five_digits(pa):
    for _ in range(REPEAT):
        assert re.fullmatch(r"\d{5}", pa.postcode())


def test_phone_numbers_are_afghan(pa):
    for _ in range(REPEAT):
        value = pa.phone_number()
        digits = re.sub(r"\D", "", value)
        assert value.startswith(("+93", "0")), f"not an Afghan dialling form: {value!r}"
        assert 9 <= len(digits) <= 12, f"implausible length {len(digits)} in {value!r}"


def test_country_code_is_afghanistan(pa):
    assert pa.current_country_code() == "AF"
    assert pa.current_country() == "Afghanistan"


def test_latin_formatters_stay_latin(pa):
    """Identifiers that must stay machine-readable are not localized."""
    for _ in range(REPEAT):
        assert_latin(pa.email(), "pa_AF.email")
        assert_latin(pa.user_name(), "pa_AF.user_name")
        assert_latin(pa.swift(), "pa_AF.swift")
        assert_latin(pa.domain_name(), "pa_AF.domain_name")


def test_email_is_well_formed(pa):
    for _ in range(REPEAT):
        assert re.fullmatch(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", pa.email()), pa.email()


def test_lorem_draws_on_the_pashto_word_list(pa):
    from pashto_toolkit.providers import provider_class

    words = set(provider_class("lorem", "pa_AF").word_list)
    assert len(words) > 100, "the Pashto word list looks truncated"
    for _ in range(REPEAT):
        assert pa.word() in words


def test_honorifics_are_titles_not_given_names(pa):
    """Regression: plain given names had leaked into the honorific lists.

    Words like خان, سردار, ملا and بی بی are genuinely both titles and names,
    so only the unambiguous given names are checked here.
    """
    from pashto_toolkit.providers import provider_class

    cls = provider_class("person", "pa_AF")
    titles = set(cls.prefixes_male) | set(cls.prefixes_female)
    not_titles = {"نجيب", "غلام", "ظاهر", "ښایسته"}
    assert not (titles & not_titles), f"given names used as honorifics: {sorted(titles & not_titles)}"
    for _ in range(100):
        assert pa.prefix() in titles


def test_most_names_carry_no_honorific(pa):
    """Regression: every generated name used to be prefixed with a title."""
    from pashto_toolkit.providers import provider_class

    titles = set(provider_class("person", "pa_AF").prefixes_male)
    titles |= set(provider_class("person", "pa_AF").prefixes_female)
    names = [pa.name() for _ in range(400)]
    with_title = sum(n.split()[0] in titles for n in names)
    assert 0 < with_title < len(names) * 0.6, f"{with_title}/{len(names)} names carry an honorific"


def test_names_have_no_stray_whitespace(pa):
    """Regression: name() used to return a trailing space."""
    for _ in range(200):
        value = pa.name()
        assert value == value.strip()
        assert "  " not in value
