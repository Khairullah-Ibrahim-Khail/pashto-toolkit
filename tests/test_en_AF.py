"""Content tests for the English-transliteration locale."""

import re

import pytest

from conftest import assert_latin

REPEAT = 30


@pytest.mark.parametrize(
    "formatter",
    [
        "name",
        "name_male",
        "name_female",
        "first_name",
        "last_name",
        "prefix",
        "province",
        "city",
        "district",
        "street",
        "street_name",
        "state",
        "company",
        "company_suffix",
        "job",
        "color_name",
        "bank_name",
        "word",
        "sentence",
        "credit_card_provider",
        "month_name",
        "day_of_week",
        "email",
        "user_name",
    ],
)
def test_formatter_returns_latin(en, formatter):
    for _ in range(REPEAT):
        assert_latin(getattr(en, formatter)(), f"en_AF.{formatter}")


def test_lorem_is_english_not_pashto(en):
    """Regression: en_AF used to serve the Pashto word list."""
    from faker.providers.lorem.en_US import Provider as EnUs

    english = set(EnUs.word_list)
    for _ in range(REPEAT):
        assert en.word() in english


def test_names_have_no_dangling_suffix(en):
    """Regression: name() glued a lowercase tribal ending on as a separate word."""
    from pashto_toolkit.providers import provider_class

    suffixes = set(provider_class("person", "en_AF").suffixes)
    for _ in range(200):
        value = en.name()
        assert value == value.strip()
        last_token = value.split()[-1]
        assert last_token not in suffixes, f"dangling suffix token in {value!r}"
        assert last_token[0].isupper(), f"lowercase final token in {value!r}"


def test_months_are_afghan_solar_calendar(en):
    from pashto_toolkit.providers import provider_class

    months = set(m for m in provider_class("date_time", "en_AF").month_names if m)
    for _ in range(REPEAT):
        assert en.month_name() in months


def test_date_time_is_not_gregorian_english(en):
    """The Afghan calendar months must not be January..December."""
    gregorian = {"January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"}
    produced = {en.month_name() for _ in range(200)}
    assert not (produced & gregorian), f"Gregorian month names leaked: {produced & gregorian}"


def test_country_code_is_afghanistan(en):
    assert en.current_country_code() == "AF"
    assert en.current_country() == "Afghanistan"


def test_postcode_is_five_digits(en):
    for _ in range(REPEAT):
        assert re.fullmatch(r"\d{5}", en.postcode())
