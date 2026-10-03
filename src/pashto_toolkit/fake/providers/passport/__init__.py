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

    def passport_full(self) -> str:
        """A whole passport data page as text."""
        gender = self.generator.format("passport_gender")
        given, surname = self.passport_owner(gender)
        birthday = self.generator.format("date_of_birth", minimum_age=18, maximum_age=80)
        issued, expires = self.generator.format("passport_dates", birthday=birthday)
        return (
            f"{surname}\n{given}\n{gender} {birthday:%d %b %Y}\n"
            f"{self.passport_number()}\n{issued:%d %b %Y}\n{expires:%d %b %Y}\n"
        )
