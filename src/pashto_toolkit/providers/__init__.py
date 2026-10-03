"""Afghanistan (``pa_AF`` / ``en_AF``) providers for Faker.

Each provider type mirrors Faker's own layout, so
``pashto_toolkit.providers.person.pa_AF`` holds the same ``Provider`` class
that Faker would look for at ``faker.providers.person.pa_AF``.
"""

from importlib import import_module
from types import ModuleType
from typing import Dict, List, Tuple, Type

from faker.providers import BaseProvider

#: Locales shipped by this package.
LOCALES: Tuple[str, ...] = ("pa_AF", "en_AF")

#: Faker provider types this package localizes, in Faker's own naming.
PROVIDER_TYPES: Tuple[str, ...] = (
    "address",
    "automotive",
    "bank",
    "barcode",
    "color",
    "company",
    "credit_card",
    "currency",
    "date_time",
    "geo",
    "internet",
    "isbn",
    "job",
    "lorem",
    "passport",
    "person",
    "phone_number",
    "ssn",
)


def provider_module(provider_type: str, locale: str) -> ModuleType:
    """Import this package's provider module for ``provider_type``/``locale``."""
    if provider_type not in PROVIDER_TYPES:
        raise ValueError(f"Unknown provider type `{provider_type}`. Expected one of {PROVIDER_TYPES}.")
    if locale not in LOCALES:
        raise ValueError(f"Unknown locale `{locale}`. Expected one of {LOCALES}.")
    return import_module(f"{__name__}.{provider_type}.{locale}")


def provider_class(provider_type: str, locale: str) -> Type[BaseProvider]:
    """Return the ``Provider`` class for ``provider_type``/``locale``."""
    return provider_module(provider_type, locale).Provider


def provider_classes(locale: str = "pa_AF") -> Dict[str, Type[BaseProvider]]:
    """Return every provider class for ``locale``, keyed by provider type."""
    return {provider_type: provider_class(provider_type, locale) for provider_type in PROVIDER_TYPES}


def __getattr__(name: str) -> ModuleType:
    # Allow `from pashto_toolkit.providers import person` without eagerly
    # importing all 36 provider modules at package import time.
    if name in PROVIDER_TYPES:
        return import_module(f"{__name__}.{name}")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> List[str]:
    return sorted({*globals(), *PROVIDER_TYPES})
