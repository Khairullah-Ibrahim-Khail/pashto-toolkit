"""Pashto Toolkit — Afghanistan locales for Faker.

Two ways in. Register the locales with Faker and use its normal API::

    import pashto_toolkit
    from faker import Faker

    pashto_toolkit.install()
    fake = Faker("pa_AF")
    fake.name()      # 'نجيب الله احمدزی'
    fake.province()  # 'کندهار'

...or skip the registration and attach the providers to a Faker instance you
already have::

    from faker import Faker
    from pashto_toolkit import add_providers

    fake = Faker()
    add_providers(fake, locale="pa_AF")
    fake.afghan_id()

:func:`pashto_faker` is shorthand for the first form.
"""

from typing import Any, Dict, List, Type

from faker.providers import BaseProvider

from ._locale import install, is_installed, uninstall
from .providers import LOCALES, PROVIDER_TYPES, provider_class, provider_classes

__version__ = "0.1.0"

DEFAULT_LOCALE = "pa_AF"

__all__ = [
    "LOCALES",
    "PROVIDER_TYPES",
    "DEFAULT_LOCALE",
    "__version__",
    "add_providers",
    "install",
    "is_installed",
    "pashto_faker",
    "provider_class",
    "provider_classes",
    "uninstall",
]


def pashto_faker(locale: str = DEFAULT_LOCALE, **kwargs: Any) -> Any:
    """Return a :class:`faker.Faker` bound to an Afghanistan locale.

    Equivalent to calling :func:`install` and then ``Faker(locale)``.
    """
    from faker import Faker

    install()
    return Faker(locale, **kwargs)


def add_providers(fake: Any, locale: str = DEFAULT_LOCALE) -> Dict[str, Type[BaseProvider]]:
    """Attach every Afghanistan provider for ``locale`` to ``fake`` in place.

    This needs no changes to Faker's internals: it is the documented
    ``Faker.add_provider`` path. The Afghanistan formatters win over the ones
    already on ``fake``, because Faker resolves the most recently added
    provider first.

    :param fake: a :class:`faker.Faker` or :class:`faker.Generator` instance.
    :param locale: ``"pa_AF"`` or ``"en_AF"``.
    :returns: the provider classes that were added, keyed by provider type.
    """
    classes = provider_classes(locale)
    for provider_cls in classes.values():
        fake.add_provider(provider_cls)
    return classes


def available_locales() -> List[str]:
    """The locale names this package can register."""
    return sorted(LOCALES)
