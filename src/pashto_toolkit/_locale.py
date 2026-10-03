"""Register the Afghanistan locales inside Faker's own locale namespace.

Faker resolves ``Faker("pa_AF")`` in three steps, all of which assume the
locale lives physically inside the installed ``faker`` package:

1. :func:`faker.factory.Factory.create` rejects any locale that is not in
   ``faker.config.AVAILABLE_LOCALES``.
2. :func:`faker.factory.Factory._find_provider_class` lists the subpackages
   that sit on disk under ``faker/providers/<type>/`` and silently falls back
   to the default locale when the requested one is missing.
3. It then imports ``faker.providers.<type>.<locale>`` and reads ``Provider``.

A separate distribution cannot add directories to Faker's installed tree, so
:func:`install` makes those same three lookups succeed from the outside:

1. ``AVAILABLE_LOCALES`` is a plain :class:`list` that ``faker.factory`` binds
   by reference, so appending to it in place is visible to the factory.
2. ``faker.factory.list_module`` is wrapped to also report the Afghanistan
   locales for the provider types this package ships.
3. ``sys.modules`` is seeded with ``faker.providers.<type>.<locale>`` entries
   pointing at this package's modules; :func:`importlib.import_module` returns
   a cached entry without touching the filesystem.

Nothing is monkeypatched until :func:`install` is called, and calling it more
than once is a no-op.
"""

import sys
from importlib import import_module
from importlib.util import find_spec
from types import ModuleType
from typing import Callable, List, Optional

from .providers import LOCALES, PROVIDER_TYPES, provider_module

_installed = False
_original_list_module: Optional[Callable[[ModuleType], List[str]]] = None


def _faker_ships_locale(provider_type: str, locale: str) -> bool:
    """True when the installed Faker already provides this locale itself.

    Should the upstream pull request land one day, Faker's own providers take
    precedence over this package's copies.
    """
    try:
        return find_spec(f"faker.providers.{provider_type}.{locale}") is not None
    except (ImportError, AttributeError, ValueError):
        return False


def _make_list_module(original: Callable[[ModuleType], List[str]]) -> Callable[[ModuleType], List[str]]:
    def list_module(module: ModuleType) -> List[str]:
        locales = original(module)
        name = getattr(module, "__name__", "")
        if name.startswith("faker.providers."):
            provider_type = name[len("faker.providers.") :]
            if provider_type in PROVIDER_TYPES:
                return sorted(set(locales) | set(LOCALES))
        return locales

    list_module.__wrapped__ = original  # type: ignore[attr-defined]
    return list_module


def _clear_provider_cache(faker_factory) -> None:
    """Drop any locale decisions the factory made before registration.

    ``Factory._find_provider_class`` is ``lru_cache``-wrapped in recent Faker
    releases and a plain function in older ones.
    """
    cache_clear = getattr(faker_factory.Factory._find_provider_class, "cache_clear", None)
    if cache_clear is not None:
        cache_clear()


def install(prefer_upstream: bool = True) -> None:
    """Make ``Faker("pa_AF")`` and ``Faker("en_AF")`` work.

    :param prefer_upstream: when the installed Faker already ships a locale of
        its own for a provider type, leave it alone instead of shadowing it.
    """
    global _installed, _original_list_module
    if _installed:
        return

    import faker.config
    import faker.factory

    # 3. Seed the module aliases Faker will import.
    for provider_type in PROVIDER_TYPES:
        parent = import_module(f"faker.providers.{provider_type}")
        for locale in LOCALES:
            target = f"faker.providers.{provider_type}.{locale}"
            if target in sys.modules:
                continue
            if prefer_upstream and _faker_ships_locale(provider_type, locale):
                continue
            module = provider_module(provider_type, locale)
            sys.modules[target] = module
            # So that `from faker.providers.person import pa_AF` also resolves.
            setattr(parent, locale, module)

    # 2. Teach the factory's locale listing about the aliases.
    if _original_list_module is None:
        _original_list_module = faker.factory.list_module
        faker.factory.list_module = _make_list_module(_original_list_module)

    # 1. Let the factory accept the locale names at all. Mutated in place
    #    because faker.factory holds a reference to this same list.
    for locale in LOCALES:
        if locale not in faker.config.AVAILABLE_LOCALES:
            faker.config.AVAILABLE_LOCALES.append(locale)
    faker.config.AVAILABLE_LOCALES.sort()

    _clear_provider_cache(faker.factory)

    _installed = True


def uninstall() -> None:
    """Undo :func:`install`. Mainly useful for tests."""
    global _installed, _original_list_module
    if not _installed:
        return

    import faker.config
    import faker.factory

    for provider_type in PROVIDER_TYPES:
        parent = sys.modules.get(f"faker.providers.{provider_type}")
        for locale in LOCALES:
            target = f"faker.providers.{provider_type}.{locale}"
            if sys.modules.get(target) is not None and sys.modules[target].__name__.startswith("pashto_toolkit."):
                del sys.modules[target]
                if parent is not None and getattr(parent, locale, None) is not None:
                    delattr(parent, locale)

    if _original_list_module is not None:
        faker.factory.list_module = _original_list_module
        _original_list_module = None

    for locale in LOCALES:
        if locale in faker.config.AVAILABLE_LOCALES and not any(
            _faker_ships_locale(provider_type, locale) for provider_type in PROVIDER_TYPES
        ):
            faker.config.AVAILABLE_LOCALES.remove(locale)

    _clear_provider_cache(faker.factory)
    _installed = False


def is_installed() -> bool:
    """True when :func:`install` has run in this interpreter."""
    return _installed
