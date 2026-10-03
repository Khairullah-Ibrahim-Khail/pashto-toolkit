"""The public surface: PashtoFaker, Generator and provider access."""

import pytest

import pashto_toolkit
from pashto_toolkit import Generator, PashtoFaker, UnknownFormatter
from pashto_toolkit.fake.providers import LOCALES, PROVIDER_TYPES, provider_class


@pytest.mark.parametrize("locale", LOCALES)
def test_every_locale_builds(locale):
    fake = PashtoFaker(locale)
    assert isinstance(fake, Generator)
    assert fake.locale == locale


def test_unknown_locale_is_rejected():
    with pytest.raises(ValueError, match="Unknown locale"):
        PashtoFaker("xx_XX")


@pytest.mark.parametrize("locale", LOCALES)
def test_every_provider_type_is_registered(locale):
    fake = PashtoFaker(locale)
    registered = {type(provider) for provider in fake.providers}
    for provider_type in PROVIDER_TYPES:
        assert provider_class(provider_type, locale) in registered, f"{provider_type} not registered"


@pytest.mark.parametrize("locale", LOCALES)
def test_the_locale_provider_wins_over_its_base(locale):
    """A base provider must never shadow the locale's own data."""
    fake = PashtoFaker(locale)
    assert fake.province() is not None
    # person/pa_AF overrides name(); the base version would raise on empty tables.
    assert fake.name()


def test_unknown_formatter_raises_a_clear_error():
    fake = PashtoFaker()
    with pytest.raises(UnknownFormatter, match="no_such_thing"):
        fake.no_such_thing()
    with pytest.raises(UnknownFormatter):
        fake.format("no_such_thing")


def test_formatters_are_discoverable():
    fake = PashtoFaker()
    names = fake.formatters()
    for expected in ("name", "province", "afghan_id", "bank_name", "ean13", "month_name"):
        assert expected in names
        assert fake.has_formatter(expected)
    assert "name" in dir(fake)


def test_add_providers_onto_a_bare_generator():
    generator = Generator("pa_AF", seed=1)
    added = pashto_toolkit.add_providers(generator, "pa_AF")
    assert set(added) == set(PROVIDER_TYPES)
    assert generator.province()
    assert generator.afghan_id()


def test_parse_expands_tokens():
    fake = PashtoFaker("en_AF", seed=3)
    out = fake.parse("{{first_name}} of {{province}}")
    assert " of " in out
    assert "{{" not in out


def test_available_locales_and_version():
    assert pashto_toolkit.available_locales() == sorted(LOCALES)
    assert pashto_toolkit.__version__


def test_unknown_provider_names_are_rejected():
    with pytest.raises(ValueError):
        provider_class("nope", "pa_AF")
    with pytest.raises(ValueError):
        provider_class("person", "xx_XX")
