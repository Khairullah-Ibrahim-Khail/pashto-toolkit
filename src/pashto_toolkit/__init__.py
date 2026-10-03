"""Pashto Toolkit — Pashto and Afghan language tooling.

Currently ships :mod:`pashto_toolkit.fake`, a generator of realistic Afghan
test data in Pashto script (``pa_AF``) and Latin transliteration (``en_AF``).

    from pashto_toolkit import PashtoFaker

    fake = PashtoFaker()
    fake.name()       # 'الحاج کبیر سور'
    fake.province()   # 'کندهار'

The package has no third-party dependencies.
"""

from .fake import (
    DEFAULT_LOCALE,
    LOCALES,
    PROVIDER_TYPES,
    Generator,
    PashtoFaker,
    UnknownFormatter,
    add_providers,
    available_locales,
    provider_class,
    provider_classes,
)

__version__ = "0.1.0"

__all__ = [
    "DEFAULT_LOCALE",
    "Generator",
    "LOCALES",
    "PROVIDER_TYPES",
    "PashtoFaker",
    "UnknownFormatter",
    "__version__",
    "add_providers",
    "available_locales",
    "provider_class",
    "provider_classes",
]
