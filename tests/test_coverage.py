"""Every formatter must be callable, and the surface must stay broad."""

import inspect

import pytest

from pashto_toolkit import PashtoFaker
from pashto_toolkit.fake.providers import ALL_PROVIDER_TYPES, LOCALES


def _zero_arg_formatters(fake):
    """Formatter names that can be called with no arguments."""
    for name in fake.formatters():
        function = getattr(fake, name)
        try:
            parameters = inspect.signature(function).parameters
        except (TypeError, ValueError):
            parameters = {}
        required = any(
            parameter.default is inspect.Parameter.empty
            and parameter.kind in (parameter.POSITIONAL_ONLY, parameter.POSITIONAL_OR_KEYWORD)
            for parameter in parameters.values()
        )
        if not required:
            yield name, function


@pytest.mark.parametrize("locale", LOCALES)
def test_every_zero_argument_formatter_runs(locale):
    fake = PashtoFaker(locale, seed=11)
    failures = []
    checked = 0
    for name, function in _zero_arg_formatters(fake):
        checked += 1
        try:
            for _ in range(8):
                function()
        except Exception as exc:  # noqa: BLE001 - the point is to catch anything
            failures.append(f"{name}: {type(exc).__name__}: {exc}")
    assert not failures, "formatters that raise:\n" + "\n".join(failures)
    assert checked > 250, f"only {checked} formatters were exercised"


@pytest.mark.parametrize("locale", LOCALES)
def test_the_surface_stays_broad(locale):
    """A guard against a provider quietly dropping out of registration."""
    fake = PashtoFaker(locale)
    assert len(fake.formatters()) >= 285
    assert len(fake.providers) == len(ALL_PROVIDER_TYPES)


@pytest.mark.parametrize("locale", LOCALES)
def test_the_formatters_people_expect_are_present(locale):
    """The names a Faker user would reach for, by area."""
    expected = {
        "person": ("name", "first_name", "last_name", "prefix", "suffix", "name_male", "name_female",
                   "name_nonbinary", "first_name_nonbinary"),
        "address": ("address", "city", "street_name", "street_address", "postcode", "state",
                    "building_number", "secondary_address", "country", "country_code"),
        "internet": ("email", "safe_email", "free_email", "ascii_email", "user_name", "url", "uri",
                     "domain_name", "ipv4", "ipv6", "mac_address", "slug", "http_method",
                     "http_status_code", "port_number"),
        "misc": ("uuid4", "boolean", "null_boolean", "md5", "sha1", "sha256", "password", "binary",
                 "emoji", "image", "image_url", "locale", "hexify"),
        "python": ("pyint", "pyfloat", "pystr", "pybool", "pylist", "pydict", "pytuple", "pyset",
                   "pydecimal", "pyiterable", "pyobject", "pystruct"),
        "datetime": ("date", "time", "date_time", "date_object", "iso8601", "timezone", "am_pm",
                     "century", "unix_time", "date_of_birth", "past_datetime", "future_datetime",
                     "time_object", "time_delta", "date_this_century"),
        "files": ("file_name", "file_path", "file_extension", "mime_type", "unix_device"),
        "serialisation": ("json", "json_bytes", "csv", "tsv", "psv", "dsv", "xml", "fixed_width",
                          "zip", "tar", "time_series"),
        "profile": ("profile", "simple_profile", "blood_group"),
        "web": ("user_agent", "chrome", "firefox", "safari", "opera", "internet_explorer"),
        "afghan": ("afghan_id", "ssn", "province", "district", "license_plate", "vin",
                   "passport_number", "passport_full", "bank_name", "iban", "swift", "pricetag"),
        "codes": ("ean13", "ean8", "upc_a", "upc_e", "isbn10", "isbn13", "sbn9", "doi",
                  "credit_card_number", "credit_card_provider", "cryptocurrency_code"),
    }
    available = set(PashtoFaker(locale).formatters())
    missing = {area: sorted(set(names) - available) for area, names in expected.items()}
    missing = {area: names for area, names in missing.items() if names}
    assert not missing, f"missing formatters by area: {missing}"
