"""Base phone-number provider."""

from typing import Sequence

from ...core import BaseProvider


class Provider(BaseProvider):
    """Telephone numbers from the locale's dialling formats."""

    formats: Sequence[str] = ()

    def phone_number(self) -> str:
        return self.numerify(self.random_element(self.formats))

    #: Afghanistan's E.164 country calling code.
    calling_code = "93"

    def country_calling_code(self) -> str:
        return f"+{self.calling_code}"

    def basic_phone_number(self) -> str:
        """Digits only, no spaces or punctuation."""
        return "".join(c for c in self.phone_number() if c.isdigit())

    def msisdn(self) -> str:
        """A 13-digit MSISDN: country code, mobile number, no plus sign."""
        return f"{self.calling_code}7{self.numerify('#########')}"

    def e164(self) -> str:
        """The number in E.164 form, e.g. ``+93701234567``."""
        return f"+{self.basic_phone_number().lstrip('0')}"
