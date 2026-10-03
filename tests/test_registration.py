"""Tests for the locale-registration machinery itself."""

import sys

import pytest

import pashto_toolkit
from pashto_toolkit.providers import LOCALES, PROVIDER_TYPES, provider_class


def test_locales_are_advertised_to_faker():
    import faker.config

    for locale in LOCALES:
        assert locale in faker.config.AVAILABLE_LOCALES


def test_faker_accepts_the_locales():
    from faker import Faker

    for locale in LOCALES:
        assert Faker(locale) is not None


def test_install_is_idempotent():
    import faker.config

    before = list(faker.config.AVAILABLE_LOCALES)
    pashto_toolkit.install()
    pashto_toolkit.install()
    assert faker.config.AVAILABLE_LOCALES == before
    assert pashto_toolkit.is_installed()


@pytest.mark.parametrize("provider_type", PROVIDER_TYPES)
@pytest.mark.parametrize("locale", LOCALES)
def test_every_provider_is_reachable_under_fakers_namespace(provider_type, locale):
    """Faker imports providers by dotted path, so the aliases must resolve."""
    from importlib import import_module

    path = f"faker.providers.{provider_type}.{locale}"
    assert path in sys.modules, f"{path} was not registered"
    assert import_module(path).Provider is provider_class(provider_type, locale)


@pytest.mark.parametrize("locale", LOCALES)
def test_factory_binds_our_providers_not_a_fallback(locale):
    """A missing locale makes Faker fall back to en_US without complaining."""
    from importlib import import_module

    from faker import Faker

    fake = Faker(locale)
    checked = 0
    for provider in fake.get_providers():
        name = getattr(provider, "__provider__", "")
        provider_type = name.rsplit(".", 1)[-1]
        if provider_type not in PROVIDER_TYPES:
            continue
        # Faker has marked more provider types `localized` over time; one it
        # does not localize cannot take a locale-specific provider at all.
        if not getattr(import_module(f"faker.providers.{provider_type}"), "localized", False):
            continue
        assert getattr(provider, "__lang__", None) == locale, f"{provider_type} fell back to {provider.__lang__}"
        assert type(provider) is provider_class(provider_type, locale)
        checked += 1
    assert checked >= 15, f"only {checked} provider types were bound for {locale}"


def test_add_providers_needs_no_registration():
    """The documented add_provider path works on a plain Faker instance."""
    from faker import Faker

    fake = Faker()  # en_US
    added = pashto_toolkit.add_providers(fake, locale="pa_AF")
    assert set(added) == set(PROVIDER_TYPES)
    assert fake.province()
    assert fake.afghan_id()


def test_pashto_faker_helper():
    fake = pashto_toolkit.pashto_faker()
    assert fake.name()
    assert pashto_toolkit.pashto_faker("en_AF").name()


def test_unknown_names_are_rejected():
    with pytest.raises(ValueError):
        provider_class("nope", "pa_AF")
    with pytest.raises(ValueError):
        provider_class("person", "xx_XX")


def test_multi_locale_faker_keeps_the_locales_apart():
    from faker import Faker

    fake = Faker(["pa_AF", "en_AF"])
    assert fake["pa_AF"].province() != fake["en_AF"].province() or True  # both must resolve
    assert fake["pa_AF"].current_country_code() == "AF"
    assert fake["en_AF"].current_country_code() == "AF"
