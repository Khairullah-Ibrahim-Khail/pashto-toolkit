"""Plain Python values: numbers, strings and containers."""

from decimal import Decimal
from typing import Any, Dict, List, Optional, Set, Tuple

from ...core import BaseProvider


class Provider(BaseProvider):
    """Builds Python primitives and containers of them."""

    def pybool(self, truth_probability: int = 50) -> bool:
        return self.random_int(1, 100) <= truth_probability

    def pyint(self, min_value: int = 0, max_value: int = 9999, step: int = 1) -> int:
        if min_value > max_value:
            raise ValueError("min_value cannot exceed max_value")
        count = (max_value - min_value) // step
        return min_value + self.random_int(0, count) * step

    def pyfloat(
        self,
        left_digits: Optional[int] = None,
        right_digits: Optional[int] = None,
        positive: bool = False,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ) -> float:
        if min_value is not None and max_value is not None and min_value > max_value:
            raise ValueError("min_value cannot exceed max_value")
        left = left_digits if left_digits is not None else self.random_int(1, 5)
        right = right_digits if right_digits is not None else self.random_int(1, 5)

        if min_value is not None or max_value is not None:
            low = min_value if min_value is not None else (0.0 if positive else -(10**left))
            high = max_value if max_value is not None else 10**left
            value = low + self.generator.random.random() * (high - low)
        else:
            whole = self.random_int(0, 10**left - 1)
            value = float(f"{whole}.{self.numerify('#' * right)}")
            if not positive and self.pybool():
                value = -value
        return round(value, right)

    def pydecimal(
        self,
        left_digits: Optional[int] = None,
        right_digits: Optional[int] = None,
        positive: bool = False,
    ) -> Decimal:
        return Decimal(str(self.pyfloat(left_digits, right_digits, positive)))

    def pystr(self, min_chars: int = 20, max_chars: int = 20) -> str:
        length = self.random_int(min_chars, max_chars)
        return "".join(self.random_letter() for _ in range(length))

    def pystr_format(self, string_format: str = "?#-###{{word}}") -> str:
        return self.bothify(self.parse(string_format))

    def _value(self) -> Any:
        """One value of a randomly chosen simple type."""
        kind = self.random_element(("str", "int", "float", "bool", "decimal", "word", "none"))
        if kind == "str":
            return self.pystr()
        if kind == "int":
            return self.pyint()
        if kind == "float":
            return self.pyfloat()
        if kind == "bool":
            return self.pybool()
        if kind == "decimal":
            return self.pydecimal()
        if kind == "word":
            return self.generator.format("word")
        return None

    def pylist(self, nb_elements: int = 10, variable_nb_elements: bool = True) -> List[Any]:
        count = self._count(nb_elements, variable_nb_elements)
        return [self._value() for _ in range(count)]

    def pytuple(self, nb_elements: int = 10, variable_nb_elements: bool = True) -> Tuple[Any, ...]:
        return tuple(self.pylist(nb_elements, variable_nb_elements))

    def pyset(self, nb_elements: int = 10, variable_nb_elements: bool = True) -> Set[Any]:
        # A set drops duplicates and unhashable values, so it may come back
        # shorter than nb_elements.
        return {value for value in self.pylist(nb_elements, variable_nb_elements) if value is not None}

    def pydict(self, nb_elements: int = 10, variable_nb_elements: bool = True) -> Dict[str, Any]:
        count = self._count(nb_elements, variable_nb_elements)
        keys = self.random_elements(self.generator.format("get_words_list"), length=count, unique=False)
        return {f"{key}_{index}": self._value() for index, key in enumerate(keys)}

    def pyiterable(self, nb_elements: int = 10, variable_nb_elements: bool = True) -> Any:
        builder = self.random_element((self.pylist, self.pytuple, self.pyset, self.pydict))
        return builder(nb_elements, variable_nb_elements)

    def _count(self, nb_elements: int, variable: bool) -> int:
        if not variable:
            return nb_elements
        spread = max(1, nb_elements // 2)
        return max(1, nb_elements + self.random_int(-spread, spread))

    def pyobject(self, object_type: Optional[type] = None) -> Any:
        """A value of ``object_type``, or of a randomly chosen simple type."""
        if object_type is None:
            return self._value()
        builders = {
            bool: self.pybool, str: self.pystr, float: self.pyfloat, int: self.pyint,
            tuple: self.pytuple, list: self.pylist, set: self.pyset, dict: self.pydict,
            Decimal: self.pydecimal,
        }
        if object_type not in builders:
            raise ValueError(f"Cannot build a {object_type!r}. Known: {sorted(t.__name__ for t in builders)}")
        return builders[object_type]()

    def pystruct(self, count: int = 10) -> Tuple[List[Any], Dict[str, Any], Set[Any]]:
        """A ``(list, dict, set)`` triple of the same length."""
        return self.pylist(count, False), self.pydict(count, False), self.pyset(count, False)

    def pytimezone(self) -> str:
        """An IANA timezone name."""
        return self.generator.format("timezone")
