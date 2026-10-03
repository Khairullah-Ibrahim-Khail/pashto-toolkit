"""Base automotive provider."""

from typing import Sequence

from ...core import BaseProvider


class Provider(BaseProvider):
    """Vehicle registration plates from the locale's formats."""

    license_formats: Sequence[str] = ()

    def license_plate(self) -> str:
        return self.numerify(self.random_element(self.license_formats))

    #: VINs exclude I, O and Q so they cannot be read as 1, 0 or 0.
    VIN_LETTERS = "ABCDEFGHJKLMNPRSTUVWXYZ"

    def vin(self) -> str:
        """A 17-character vehicle identification number."""
        return "".join(
            self.random_element(self.VIN_LETTERS + "0123456789") for _ in range(17)
        )
