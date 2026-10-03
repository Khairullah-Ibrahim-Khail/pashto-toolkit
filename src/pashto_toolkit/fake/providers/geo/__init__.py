"""Base geo provider."""

from decimal import Decimal
from typing import Tuple

from ...core import BaseProvider


class Provider(BaseProvider):
    """Coordinates. The locale restricts them to its own bounding box."""

    def _degrees(self, low: int, high: int) -> Decimal:
        """A coordinate to six decimal places, inclusive of both bounds."""
        micro = self.random_int(low, high)
        return Decimal(micro).scaleb(-6).quantize(Decimal("0.000001"))

    def latitude(self) -> Decimal:
        return self._degrees(-90_000_000, 90_000_000)

    def longitude(self) -> Decimal:
        return self._degrees(-180_000_000, 180_000_000)

    def coordinate(self) -> Tuple[Decimal, Decimal]:
        return self.latitude(), self.longitude()

    def latlng(self) -> Tuple[Decimal, Decimal]:
        return self.coordinate()

    def local_latlng(self) -> Tuple[str, str]:
        """Coordinates inside the locale's area."""
        return str(self.latitude()), str(self.longitude())
