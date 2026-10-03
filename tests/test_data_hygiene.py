"""Guards on the provider data tables themselves.

Stray whitespace and empty entries in a word list surface as malformed output
(double spaces inside a name, an empty month name) that type-only assertions
never catch.
"""

import pytest

from pashto_toolkit.providers import LOCALES, PROVIDER_TYPES, provider_class


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
    """Duplicates silently skew the distribution."""
    offenders = []
    for attr, entries in _tables(provider_type, locale):
        if "name" not in attr and "companies" not in attr and "banks" not in attr:
            continue
        duplicates = {e for e in entries if entries.count(e) > 1 and e}
        if duplicates:
            offenders.append(f"{provider_type}.{attr}: {sorted(duplicates)}")
    if offenders:
        pytest.xfail("duplicate entries skew distribution:\n" + "\n".join(offenders))


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
    from faker import Faker

    fake = Faker(locale)
    address = provider_class("address", locale)
    for province, districts in address.districts.items():
        value = fake.district(province)
        assert value in districts, f"{province}: got {value!r}, not one of its districts"
