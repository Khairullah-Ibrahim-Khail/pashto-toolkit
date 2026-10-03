"""Base person provider: given names, family names, honorifics."""

from typing import List, Sequence

from ...core import BaseProvider


class Provider(BaseProvider):
    """Composes personal names from the locale's name tables."""

    formats: Sequence[str] = ("{{first_name}} {{last_name}}",)

    first_names: Sequence[str] = ()
    first_names_male: Sequence[str] = ()
    first_names_female: Sequence[str] = ()
    first_names_nonbinary: Sequence[str] = ()
    last_names: Sequence[str] = ()
    prefixes: Sequence[str] = ()
    prefixes_male: Sequence[str] = ()
    prefixes_female: Sequence[str] = ()
    suffixes: Sequence[str] = ()

    # --- helpers ---------------------------------------------------------
    def _pool(self, *candidates: Sequence[str]) -> List[str]:
        """First non-empty table among ``candidates``, as a list."""
        for candidate in candidates:
            if candidate:
                return list(candidate)
        return []

    # --- names -----------------------------------------------------------
    def name(self) -> str:
        return self.parse(self.random_element(self.formats))

    def first_name(self) -> str:
        return self.random_element(
            self._pool(self.first_names, tuple(self.first_names_male) + tuple(self.first_names_female))
        )

    def first_name_male(self) -> str:
        return self.random_element(self._pool(self.first_names_male, self.first_names))

    def first_name_female(self) -> str:
        return self.random_element(self._pool(self.first_names_female, self.first_names))

    def first_name_nonbinary(self) -> str:
        """A given name with no gender marker.

        Afghan given names are strongly gendered, so unless a locale supplies
        its own list this falls back to :meth:`first_name`, which draws from
        both.
        """
        pool = self._pool(
            self.first_names_nonbinary,
            self.first_names,
            tuple(self.first_names_male) + tuple(self.first_names_female),
        )
        return self.random_element(pool) if pool else self.first_name()

    def last_name(self) -> str:
        return self.random_element(self.last_names)

    def name_male(self) -> str:
        return f"{self.first_name_male()} {self.last_name()}"

    def name_female(self) -> str:
        return f"{self.first_name_female()} {self.last_name()}"

    # --- honorifics ------------------------------------------------------
    def prefix(self) -> str:
        return self.random_element(
            self._pool(self.prefixes, tuple(self.prefixes_male) + tuple(self.prefixes_female))
        )

    def prefix_male(self) -> str:
        return self.random_element(self._pool(self.prefixes_male, self.prefixes))

    def prefix_female(self) -> str:
        return self.random_element(self._pool(self.prefixes_female, self.prefixes))

    def suffix(self) -> str:
        return self.random_element(self.suffixes) if self.suffixes else ""

    def name_nonbinary(self) -> str:
        return f"{self.first_name_nonbinary()} {self.last_name()}"

    def last_name_male(self) -> str:
        """Afghan family names do not inflect for gender."""
        return self.last_name()

    def last_name_female(self) -> str:
        return self.last_name()

    def last_name_nonbinary(self) -> str:
        return self.last_name()

    def prefix_nonbinary(self) -> str:
        return self.prefix()

    def suffix_male(self) -> str:
        return self.suffix()

    def suffix_female(self) -> str:
        return self.suffix()

    def suffix_nonbinary(self) -> str:
        return self.suffix()
