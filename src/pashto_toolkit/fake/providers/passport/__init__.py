"""Base passport provider."""

from datetime import date
from typing import Sequence, Tuple

from ...core import BaseProvider
from ...types import SexLiteral


class Provider(BaseProvider):
    """Passport numbers and holder details."""

    passport_number_formats: Sequence[str] = ()

    def passport_number(self) -> str:
        """Expand a format where ``?`` is a letter and ``#`` a digit."""
        return self.bothify(
            self.random_element(self.passport_number_formats),
            letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        )

    def passport_dob(self) -> date:
        return self.generator.format("date_of_birth")

    def passport_owner(self, gender: SexLiteral = "X") -> Tuple[str, str]:
        """A ``(given_name, surname)`` pair for the stated gender marker."""
        if gender == "M":
            given = self.generator.format("first_name_male")
        elif gender == "F":
            given = self.generator.format("first_name_female")
        else:
            given = self.generator.format("first_name_nonbinary")
        return given, self.generator.format("last_name")
