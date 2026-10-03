"""A seed must reproduce a run exactly; that is the point of the package."""

import pytest

from pashto_toolkit import PashtoFaker
from pashto_toolkit.fake.providers import LOCALES, PROVIDER_TYPES, provider_module

FORMATTERS = [
    "name", "first_name", "last_name", "prefix", "job",
    "province", "city", "district", "street", "street_name", "street_address",
    "postcode", "address", "building_number",
    "company", "company_suffix", "catch_phrase", "bs",
    "bank_name", "swift", "iban", "account_number",
    "afghan_id", "ssn", "license_plate", "passport_number", "passport_gender",
    "email", "user_name", "url", "ipv4", "ipv6", "mac_address",
    "phone_number", "word", "sentence", "paragraph",
    "color_name", "color", "credit_card_number", "credit_card_provider",
    "month_name", "day_of_week", "ean13", "upc_a", "isbn13", "isbn10",
    "local_latlng", "currency_code", "currency_name", "pricetag",
]


def _run(locale, seed):
    fake = PashtoFaker(locale, seed=seed)
    return {name: [str(fake.format(name)) for _ in range(5)] for name in FORMATTERS}


@pytest.mark.parametrize("locale", LOCALES)
def test_same_seed_gives_the_same_run(locale):
    first, second = _run(locale, 4242), _run(locale, 4242)
    differing = [name for name in FORMATTERS if first[name] != second[name]]
    assert not differing, f"{locale}: not reproducible under a fixed seed: {differing}"


@pytest.mark.parametrize("locale", LOCALES)
def test_different_seeds_give_different_runs(locale):
    assert _run(locale, 1) != _run(locale, 2), f"{locale}: output ignores the seed"


@pytest.mark.parametrize("locale", LOCALES)
def test_reseeding_an_existing_generator_restarts_the_sequence(locale):
    fake = PashtoFaker(locale, seed=11)
    first = [fake.name() for _ in range(5)]
    fake.seed(11)
    assert [fake.name() for _ in range(5)] == first


@pytest.mark.parametrize("locale", LOCALES)
def test_no_provider_calls_the_global_random_module(locale):
    """A static guard, so a future edit cannot quietly reintroduce the bug."""
    import inspect

    offenders = []
    for provider_type in PROVIDER_TYPES:
        source = inspect.getsource(provider_module(provider_type, locale))
        for lineno, line in enumerate(source.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#") or "generator.random." in stripped:
                continue
            if re.search(r"(?<![\w.])random\.", stripped):
                offenders.append(f"{provider_type}/{locale}:{lineno}: {stripped}")
    assert not offenders, "global random usage breaks seeding:\n" + "\n".join(offenders)


import re  # noqa: E402  (used by the guard above)
