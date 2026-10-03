"""Fake Afghan data: names, addresses, banks, IDs and more.

No third-party dependency; the generator core lives in :mod:`.core`.

    from pashto_toolkit.fake import PashtoFaker

    fake = PashtoFaker()            # pa_AF, Pashto script
    fake.name()                     # 'الحاج کبیر سور'
    fake.province()                 # 'کندهار'
    fake.afghan_id()                # '6768-223-117-276'

    english = PashtoFaker("en_AF")  # Latin transliteration
    english.name()                  # 'Tahir Dawlatzai'
"""

from typing import Any, Dict, List, Optional, Type

from .core import BaseProvider, Generator, UnknownFormatter
from .providers import (
    LOCALES,
    PROVIDER_TYPES,
    base_module,
    provider_class,
    provider_classes,
    provider_module,
)
from .types import CreditCard, SexLiteral

DEFAULT_LOCALE = "pa_AF"

__all__ = [
    "BaseProvider",
    "CreditCard",
    "DEFAULT_LOCALE",
    "Generator",
    "LOCALES",
    "PROVIDER_TYPES",
    "PashtoFaker",
    "SexLiteral",
    "UnknownFormatter",
    "add_providers",
    "available_locales",
    "base_module",
    "provider_class",
    "provider_classes",
    "provider_module",
]


def PashtoFaker(locale: str = DEFAULT_LOCALE, seed: Optional[int] = None) -> Generator:
    """Return a generator with every Afghanistan provider for ``locale``.

    :param locale: ``"pa_AF"`` (Pashto script) or ``"en_AF"`` (transliteration).
    :param seed: seeds the generator, so a run is reproducible.
    """
    if locale not in LOCALES:
        raise ValueError(f"Unknown locale {locale!r}. Expected one of {LOCALES}.")
    generator = Generator(locale=locale, seed=seed)
    add_providers(generator, locale)
    return generator


def add_providers(generator: Generator, locale: str = DEFAULT_LOCALE) -> Dict[str, Type[BaseProvider]]:
    """Attach every Afghanistan provider for ``locale`` to ``generator``.

    Useful for adding Afghan data to a generator that already carries
    providers of your own.

    :returns: the provider classes added, keyed by provider type.
    """
    classes = provider_classes(locale)
    for provider_cls in classes.values():
        generator.add_provider(provider_cls)
    return classes


def available_locales() -> List[str]:
    """The locales this package provides."""
    return sorted(LOCALES)


def __getattr__(name: str) -> Any:
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
