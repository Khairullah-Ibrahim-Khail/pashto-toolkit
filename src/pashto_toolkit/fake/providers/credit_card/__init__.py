"""Base credit-card provider."""

from collections import OrderedDict
from typing import Dict, Optional

from ...checksums import luhn_check_digit
from ...core import BaseProvider
from ...types import CreditCard


class Provider(BaseProvider):
    """Card numbers that satisfy the Luhn check, plus expiry and CVV."""

    credit_card_types: Dict[str, CreditCard] = OrderedDict()

    def credit_card_type(self, card_type: Optional[str] = None) -> CreditCard:
        if card_type is None:
            return self.random_element(list(self.credit_card_types.values()))
        try:
            return self.credit_card_types[card_type]
        except KeyError:
            raise ValueError(
                f"Unknown card type {card_type!r}. Known: {sorted(self.credit_card_types)}"
            ) from None

    def credit_card_provider(self, card_type: Optional[str] = None) -> str:
        return self.credit_card_type(card_type).name

    def credit_card_number(self, card_type: Optional[str] = None) -> str:
        """A card number with a valid Luhn check digit."""
        card = self.credit_card_type(card_type)
        prefix = self.random_element(card.prefixes)
        body = self.numerify("#" * (card.length - len(prefix) - 1))
        partial = f"{prefix}{body}"
        return f"{partial}{luhn_check_digit(partial)}"

    def credit_card_expire(self, start: str = "now", end: str = "+10y", pattern: str = "%m/%y") -> str:
        """An expiry date between one month and ten years from now."""
        from datetime import date

        today = date.today()
        months = self.random_int(1, 120)
        year = today.year + (today.month - 1 + months) // 12
        month = (today.month - 1 + months) % 12 + 1
        return date(year, month, 1).strftime(pattern)

    def credit_card_security_code(self, card_type: Optional[str] = None) -> str:
        card = self.credit_card_type(card_type)
        return self.numerify("#" * card.security_code_length)

    def credit_card_full(self, card_type: Optional[str] = None) -> str:
        card = self.credit_card_type(card_type)
        owner = self.generator.format("name")
        return (
            f"{card.name}\n"
            f"{owner}\n"
            f"{self.credit_card_number(card_type)} {self.credit_card_expire()}\n"
            f"{card.security_code}: {self.credit_card_security_code(card_type)}\n"
        )
