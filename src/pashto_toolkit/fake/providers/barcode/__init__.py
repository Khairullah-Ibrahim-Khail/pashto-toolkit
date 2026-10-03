"""Base barcode provider."""

from typing import Sequence, Tuple

from ...checksums import ean_check_digit
from ...core import BaseProvider


class Provider(BaseProvider):
    """EAN-8, EAN-13 and UPC-A codes with correct GS1 check digits."""

    #: (prefix, length) pairs this locale may use for localized codes.
    local_prefixes: Sequence[Tuple[int, int]] = ()

    def _ean(self, length: int = 13, prefix: str = "") -> str:
        if length not in (8, 13):
            raise ValueError("An EAN is either 8 or 13 digits long.")
        if prefix and not prefix.isdigit():
            raise ValueError("prefix must contain only digits")
        body = prefix + self.numerify("#" * (length - 1 - len(prefix)))
        return f"{body}{ean_check_digit(body)}"

    def ean(self, length: int = 13, prefix: str = "") -> str:
        return self._ean(length, prefix)

    def ean8(self, prefix: str = "") -> str:
        return self._ean(8, prefix)

    def ean13(self, prefix: str = "") -> str:
        return self._ean(13, prefix)

    def upc_a(self, prefix: str = "") -> str:
        """UPC-A is an EAN-13 whose leading digit is zero, written as 12 digits."""
        return self._ean(13, prefix="0" + prefix)[1:]

    def localized_ean(self, length: int = 13) -> str:
        """An EAN carrying one of this locale's own GS1 prefixes."""
        if not self.local_prefixes:
            return self._ean(length)
        prefix = self.random_element([str(p[0]) for p in self.local_prefixes])
        return self._ean(length, prefix=prefix)

    def localized_ean8(self) -> str:
        return self.localized_ean(8)

    def localized_ean13(self) -> str:
        return self.localized_ean(13)

    def upc_e(self) -> str:
        """An 8-digit UPC-E: number system, six digits and a check digit."""
        body = "0" + self.numerify("######")
        return f"{body}{ean_check_digit(body)}"
