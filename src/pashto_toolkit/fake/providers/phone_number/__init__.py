"""Base phone-number provider."""

from typing import Sequence

from ...core import BaseProvider


class Provider(BaseProvider):
    """Telephone numbers from the locale's dialling formats."""

    formats: Sequence[str] = ()

    def phone_number(self) -> str:
        return self.numerify(self.random_element(self.formats))
