"""Base automotive provider."""

from typing import Sequence

from ...core import BaseProvider


class Provider(BaseProvider):
    """Vehicle registration plates from the locale's formats."""

    license_formats: Sequence[str] = ()

    def license_plate(self) -> str:
        return self.numerify(self.random_element(self.license_formats))
