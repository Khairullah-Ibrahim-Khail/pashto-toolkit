"""Base ISBN provider."""

from typing import Dict, List, Sequence, Tuple

from ...checksums import isbn10_check_digit, isbn13_check_digit
from ...core import BaseProvider

#: An ISBN-13 is 13 digits, the last of which is the check digit.
MAX_LENGTH = 13

#: Registrant rules: (lower bound, upper bound, registrant length).
RuleList = List[Tuple[str, str, int]]


class Provider(BaseProvider):
    """ISBNs built from the locale's registration-group rules."""

    rules: Dict[str, Dict[str, RuleList]] = {}

    def _body(self) -> List[str]:
        """Return ``[ean, group, registrant, publication]``."""
        ean = self.random_element(list(self.rules.keys()))
        group = self.random_element(list(self.rules[ean].keys()))
        # Leave room for the check digit.
        reg_pub_len = MAX_LENGTH - len(ean) - len(group) - 1
        reg_pub = self.numerify("#" * reg_pub_len)
        registrant, publication = self._split(reg_pub, self.rules[ean][group])
        return [ean, group, registrant, publication]

    @staticmethod
    def _split(reg_pub: str, rules: Sequence[Tuple[str, str, int]]) -> Tuple[str, str]:
        """Split registrant from publication at the width its range dictates."""
        for low, high, length in rules:
            if int(low[:length]) <= int(reg_pub[:length]) <= int(high[:length]):
                return reg_pub[:length], reg_pub[length:]
        raise ValueError(f"No registrant rule matched {reg_pub!r}.")

    def isbn13(self, separator: str = "-") -> str:
        ean, group, registrant, publication = self._body()
        check = isbn13_check_digit(f"{ean}{group}{registrant}{publication}")
        return separator.join((ean, group, registrant, publication, check))

    def isbn10(self, separator: str = "-") -> str:
        """An ISBN-10: nine digits plus a check character, which may be ``X``.

        The EAN prefix is dropped, which leaves exactly the nine digits an
        ISBN-10 needs before its check character.
        """
        _, group, registrant, publication = self._body()
        body = f"{group}{registrant}{publication}"
        if len(body) != 9:
            raise ValueError(f"ISBN-10 body must be 9 digits, got {len(body)}: {body!r}")
        return separator.join((group, registrant, publication, isbn10_check_digit(body)))
