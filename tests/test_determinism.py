"""Faker's core promise is that a seed reproduces a run.

The providers originally called the global ``random`` module, which Faker's
seeding does not control, so these locales were not reproducible.
"""

import pytest

from pashto_toolkit.providers import LOCALES, PROVIDER_TYPES

FORMATTERS = [
    "name", "first_name", "last_name", "prefix", "job",
    "province", "city", "district", "street", "street_name", "postcode", "address",
    "company", "company_suffix", "bank_name", "swift", "account_number",
    "afghan_id", "ssn", "license_plate", "passport_number", "passport_gender",
    "email", "user_name", "phone_number", "word", "sentence",
    "color_name", "credit_card_number", "credit_card_provider",
    "month_name", "day_of_week", "ean13", "isbn13", "local_latlng",
]


def _run(locale, seed):
    from faker import Faker

    Faker.seed(seed)
    fake = Faker(locale)
    return {name: [str(getattr(fake, name)()) for _ in range(5)] for name in FORMATTERS}


@pytest.mark.parametrize("locale", LOCALES)
def test_same_seed_gives_the_same_run(locale):
    first, second = _run(locale, 4242), _run(locale, 4242)
    differing = [name for name in FORMATTERS if first[name] != second[name]]
    assert not differing, f"{locale}: not reproducible under a fixed seed: {differing}"


@pytest.mark.parametrize("locale", LOCALES)
def test_different_seeds_give_different_runs(locale):
    first, second = _run(locale, 1), _run(locale, 2)
    assert first != second, f"{locale}: output does not depend on the seed at all"


@pytest.mark.parametrize("locale", LOCALES)
def test_no_provider_calls_the_global_random_module(locale):
    """A static guard, so a future edit cannot quietly reintroduce the bug."""
    import inspect

    from pashto_toolkit.providers import provider_module

    offenders = []
    for provider_type in PROVIDER_TYPES:
        source = inspect.getsource(provider_module(provider_type, locale))
        for lineno, line in enumerate(source.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#") or "generator.random." in stripped:
                continue
            if "random." in stripped and "self." not in stripped:
                offenders.append(f"{provider_type}/{locale}:{lineno}: {stripped}")
    assert not offenders, "global random usage breaks Faker.seed():\n" + "\n".join(offenders)
