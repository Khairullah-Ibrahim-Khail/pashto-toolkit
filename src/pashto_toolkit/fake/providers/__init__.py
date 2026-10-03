"""Afghanistan providers for the ``pa_AF`` and ``en_AF`` locales.

Each provider type is a package holding a base ``Provider`` with the generic
behaviour, and one subpackage per locale carrying the Afghan data.
"""

from importlib import import_module
from types import ModuleType
from typing import Dict, List, Tuple, Type

from ..core import BaseProvider

#: Locales this package provides.
LOCALES: Tuple[str, ...] = ("pa_AF", "en_AF")

#: Provider types, in the order they are registered on a generator.
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


def _check(provider_type: str, locale: str) -> None:
    if provider_type not in PROVIDER_TYPES:
        raise ValueError(f"Unknown provider type {provider_type!r}. Expected one of {PROVIDER_TYPES}.")
    if locale not in LOCALES:
        raise ValueError(f"Unknown locale {locale!r}. Expected one of {LOCALES}.")


def provider_module(provider_type: str, locale: str) -> ModuleType:
    """Import the provider module for ``provider_type``/``locale``."""
    _check(provider_type, locale)
    return import_module(f"{__name__}.{provider_type}.{locale}")


def base_module(provider_type: str) -> ModuleType:
    """Import the locale-independent base module for ``provider_type``."""
    if provider_type not in PROVIDER_TYPES:
        raise ValueError(f"Unknown provider type {provider_type!r}.")
    return import_module(f"{__name__}.{provider_type}")


def provider_class(provider_type: str, locale: str) -> Type[BaseProvider]:
    """Return the ``Provider`` class for ``provider_type``/``locale``."""
    return provider_module(provider_type, locale).Provider


def provider_classes(locale: str = "pa_AF") -> Dict[str, Type[BaseProvider]]:
    """Every provider class for ``locale``, keyed by provider type."""
    return {provider_type: provider_class(provider_type, locale) for provider_type in PROVIDER_TYPES}


def __getattr__(name: str) -> ModuleType:
    # Lets `from pashto_toolkit.fake.providers import person` work without
    # importing all 36 locale modules at package import time.
    if name in PROVIDER_TYPES:
        return import_module(f"{__name__}.{name}")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> List[str]:
    return sorted({*globals(), *PROVIDER_TYPES})
