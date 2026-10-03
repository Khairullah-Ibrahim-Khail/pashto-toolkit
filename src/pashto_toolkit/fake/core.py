"""The generator core: a seeded RNG, a provider base class, and dispatch.

Replaces the generic machinery the providers need, so that the
package has no third-party dependency.
"""

import builtins
import random as _random
import re
import string
from datetime import date, datetime, timedelta
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Type, TypeVar, Union

T = TypeVar("T")

_TOKEN = re.compile(r"\{\{\s*(\w+)\s*\}\}")


class UnknownFormatter(AttributeError):
    """Raised when a formatter is requested that no provider supplies."""


class BaseProvider:
    """Base class for every provider.

    A provider holds data tables as class attributes and exposes formatters as
    methods. All randomness goes through ``self.generator.random`` so that
    seeding the generator reproduces a run exactly.
    """

    def __init__(self, generator: "Generator") -> None:
        self.generator = generator

    # --- randomness -----------------------------------------------------
    @property
    def random(self) -> _random.Random:
        return self.generator.random

    def random_element(self, elements: Sequence[T]) -> T:
        """Pick one element uniformly.

        A mapping of element to weight is also accepted, in which case the
        pick is weighted by those values.
        """
        if isinstance(elements, dict):
            keys = list(elements.keys())
            weights = list(elements.values())
            return self.generator.random.choices(keys, weights=weights, k=1)[0]
        return self.generator.random.choice(list(elements))

    def random_elements(self, elements: Sequence[T], length: int = 1, unique: bool = False) -> List[T]:
        """Pick ``length`` elements, with or without replacement."""
        pool = list(elements)
        if unique:
            if length > len(pool):
                raise ValueError(f"cannot take {length} unique elements from {len(pool)}")
            return self.generator.random.sample(pool, length)
        return [self.generator.random.choice(pool) for _ in range(length)]

    def random_int(self, min: int = 0, max: int = 9999) -> int:
        return self.generator.random.randint(min, max)

    def random_digit(self) -> int:
        return self.generator.random.randint(0, 9)

    def random_digit_not_zero(self) -> int:
        return self.generator.random.randint(1, 9)

    def random_digit_not_null(self) -> int:
        """Older name for :meth:`random_digit_not_zero`."""
        return self.random_digit_not_zero()

    def random_digit_not_null_or_empty(self) -> Union[int, str]:
        """Older name for :meth:`random_digit_not_zero_or_empty`."""
        return self.random_digit_not_zero_or_empty()

    def random_digit_above_two(self) -> int:
        return self.generator.random.randint(2, 9)

    def random_digit_or_empty(self) -> Union[int, str]:
        """A digit half the time, an empty string the rest."""
        return self.random_digit() if self.generator.random.random() < 0.5 else ""

    def random_digit_not_zero_or_empty(self) -> Union[int, str]:
        return self.random_digit_not_zero() if self.generator.random.random() < 0.5 else ""

    def random_number(self, digits: Optional[int] = None, fix_len: bool = False) -> int:
        """A number of ``digits`` digits; ``fix_len`` forbids a leading zero."""
        if digits is None:
            digits = self.random_int(1, 9)
        if digits < 0:
            raise ValueError("digits cannot be negative")
        if digits == 0:
            return 0
        if fix_len:
            return self.random_int(10 ** (digits - 1), 10**digits - 1)
        return self.random_int(0, 10**digits - 1)

    def random_letter(self) -> str:
        return self.generator.random.choice(string.ascii_letters)

    def random_letters(self, length: int = 16) -> List[str]:
        return [self.random_letter() for _ in range(length)]

    def random_lowercase_letter(self) -> str:
        return self.generator.random.choice(string.ascii_lowercase)

    def random_choices(self, elements: Sequence[T], length: Optional[int] = None) -> List[T]:
        """Pick with replacement, so values may repeat."""
        return self.random_elements(elements, length=1 if length is None else length, unique=False)

    def random_sample(self, elements: Sequence[T], length: Optional[int] = None) -> List[T]:
        """Pick without replacement, so values are distinct."""
        pool = list(elements)
        return self.random_elements(pool, length=len(pool) if length is None else length, unique=True)

    def randomize_nb_elements(
        self,
        number: int = 10,
        le: bool = False,
        ge: bool = False,
        min: Optional[int] = None,
        max: Optional[int] = None,
    ) -> int:
        """Jitter ``number`` by up to 40%, optionally clamped to one side."""
        if le and ge:
            return number
        low, high = (100, 140) if ge else (60, 100) if le else (60, 140)
        value = int(number * self.random_int(low, high) / 100) + 1
        if min is not None:
            value = builtins.max(value, min)
        if max is not None:
            value = builtins.min(value, max)
        return value

    def random_uppercase_letter(self) -> str:
        return self.generator.random.choice(string.ascii_uppercase)

    # --- string templates -----------------------------------------------
    def numerify(self, text: str) -> str:
        """Expand digit placeholders, leaving every other character alone.

        ``#`` becomes any digit, ``%`` a digit from 1-9, ``$`` a digit from
        2-9 and ``!`` either a digit or nothing. Spaces and punctuation are
        preserved, because the phone and plate formats depend on them.
        """
        out = []
        for char in text:
            if char == "#":
                out.append(str(self.random_digit()))
            elif char == "%":
                out.append(str(self.random_digit_not_zero()))
            elif char == "$":
                out.append(str(self.random_int(2, 9)))
            elif char == "!":
                out.append(self.generator.random.choice("0123456789") if self.random_int(0, 1) else "")
            else:
                out.append(char)
        return "".join(out)

    def lexify(self, text: str, letters: str = string.ascii_letters) -> str:
        """Replace every ``?`` with a letter from ``letters``."""
        return "".join(self.generator.random.choice(letters) if c == "?" else c for c in text)

    def bothify(self, text: str, letters: str = string.ascii_letters) -> str:
        """Apply :meth:`numerify` then :meth:`lexify`."""
        return self.lexify(self.numerify(text), letters=letters)

    def parse(self, template: str) -> str:
        """Expand ``{{formatter}}`` tokens in ``template``."""
        return self.generator.parse(template)


#: Provider attributes that are plumbing rather than callable formatters.
_NOT_FORMATTERS = frozenset({"generator", "random"})


class Generator:
    """Holds a locale's providers and dispatches formatter calls.

    Formatters are reached as attributes::

        gen = Generator("pa_AF")
        gen.name()
        gen.province()

    The most recently added provider wins when two supply the same formatter.
    """

    #: The locale this generator was built for. Named ``current_locale``
    #: because ``locale`` is itself a formatter, from the misc provider.
    current_locale: str

    def __init__(self, locale: str = "pa_AF", seed: Optional[int] = None) -> None:
        self.current_locale = locale
        self.random = _random.Random(seed)
        self._formatters: Dict[str, Callable[..., Any]] = {}
        self._providers: List[BaseProvider] = []

    # --- provider registration -------------------------------------------
    def add_provider(self, provider: Union[BaseProvider, Type[BaseProvider]]) -> BaseProvider:
        """Register a provider instance or class and expose its formatters.

        Every public method becomes a formatter, including the helpers from
        :class:`BaseProvider` such as ``numerify`` and ``random_element``,
        which are useful directly on the generator.
        """
        instance = provider(self) if isinstance(provider, type) else provider
        self._providers.insert(0, instance)
        for name in dir(instance):
            if name.startswith("_") or name in _NOT_FORMATTERS:
                continue
            attribute = getattr(instance, name)
            if callable(attribute):
                self._formatters[name] = attribute
        return instance

    @property
    def providers(self) -> List[BaseProvider]:
        return list(self._providers)

    def formatters(self) -> List[str]:
        """Every formatter name available on this generator, sorted."""
        return sorted(self._formatters)

    def has_formatter(self, name: str) -> bool:
        return name in self._formatters

    # --- use --------------------------------------------------------------
    def seed(self, seed: Optional[int] = None) -> "Generator":
        """Reseed the generator. Returns self so calls can be chained."""
        self.random.seed(seed)
        return self

    def format(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """Call a formatter by name."""
        try:
            formatter = self._formatters[name]
        except KeyError:
            raise UnknownFormatter(
                f"No provider supplies a formatter named {name!r} for locale {self.current_locale!r}."
            ) from None
        return formatter(*args, **kwargs)

    def parse(self, template: str) -> str:
        """Expand ``{{formatter}}`` tokens in ``template``."""
        return _TOKEN.sub(lambda match: str(self.format(match.group(1))), template)

    def __getattr__(self, name: str) -> Callable[..., Any]:
        # Only consulted for attributes not found normally, so the real
        # attributes above are never shadowed.
        try:
            return self.__dict__["_formatters"][name]
        except KeyError:
            raise UnknownFormatter(
                f"No provider supplies a formatter named {name!r} for locale {self.current_locale!r}."
            ) from None

    def __dir__(self) -> List[str]:
        return sorted({*super().__dir__(), *self._formatters})

    def __repr__(self) -> str:
        return f"<Generator locale={self.current_locale!r} providers={len(self._providers)}>"


def date_between(rng: _random.Random, start: date, end: date) -> date:
    """A uniformly random date in ``[start, end]``."""
    if end < start:
        start, end = end, start
    return start + timedelta(days=rng.randint(0, (end - start).days))


def datetime_between(rng: _random.Random, start: datetime, end: datetime) -> datetime:
    """A uniformly random datetime in ``[start, end]``."""
    if end < start:
        start, end = end, start
    return start + timedelta(seconds=rng.randint(0, int((end - start).total_seconds())))


def flatten(values: Iterable[Any]) -> List[Any]:
    """One level of flattening, for data tables built from grouped lists."""
    out: List[Any] = []
    for value in values:
        if isinstance(value, (list, tuple)):
            out.extend(value)
        else:
            out.append(value)
    return out
