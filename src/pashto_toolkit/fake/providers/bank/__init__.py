"""Base bank provider: BBAN, IBAN, SWIFT/BIC."""

from typing import Sequence

from ...core import BaseProvider

#: 'A' -> 10 ... 'Z' -> 35, as ISO 13616 requires for the IBAN check digits.
_LETTER_VALUES = {chr(ord("A") + i): str(10 + i) for i in range(26)}


class Provider(BaseProvider):
    """Account identifiers for the locale's banks."""

    country_code = "AF"
    bban_format = "################"
    banks: Sequence[str] = ()

    swift_bank_codes: Sequence[str] = ()
    swift_location_codes: Sequence[str] = ()
    swift_branch_codes: Sequence[str] = ()

    def bank_country(self) -> str:
        return self.country_code

    def bank_name(self) -> str:
        return self.random_element(self.banks)

    def bban(self) -> str:
        return self.bothify(self.bban_format, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def iban(self) -> str:
        """An IBAN with correct mod-97 check digits (ISO 13616)."""
        bban = self.bban()
        rearranged = f"{bban}{self.country_code}00"
        numeric = "".join(_LETTER_VALUES.get(c, c) for c in rearranged)
        check = 98 - (int(numeric) % 97)
        return f"{self.country_code}{check:02d}{bban}"

    def swift8(self) -> str:
        """An 8-character BIC: bank, country, location."""
        bank = self.random_element(self.swift_bank_codes) if self.swift_bank_codes else self.lexify(
            "????", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        location = self.random_element(self.swift_location_codes) if self.swift_location_codes else self.bothify(
            "?#", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        return f"{bank}{self.country_code}{location}"

    def swift11(self) -> str:
        """An 11-character BIC: the 8-character form plus a branch code."""
        branch = self.random_element(self.swift_branch_codes) if self.swift_branch_codes else self.bothify(
            "?##", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        return f"{self.swift8()}{branch}"

    def swift(self, length: int = 8) -> str:
        if length not in (8, 11):
            raise ValueError("A BIC is either 8 or 11 characters long.")
        return self.swift8() if length == 8 else self.swift11()

    def bank(self) -> str:
        """Alias of :meth:`bank_name`."""
        return self.bank_name()
