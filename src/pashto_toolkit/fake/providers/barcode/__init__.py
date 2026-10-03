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
