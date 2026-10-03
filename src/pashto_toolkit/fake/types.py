"""Small value types shared by the providers."""

from typing import Any, Literal, Sequence

#: Passport/ID gender marker: male, female or unspecified.
SexLiteral = Literal["M", "F", "X"]


class CreditCard:
    """One card scheme: its display name, accepted prefixes and number length."""

    __slots__ = ("name", "prefixes", "length", "security_code", "security_code_length")

    def __init__(
        self,
        name: str,
        prefixes: Sequence[str],
        length: int = 16,
        security_code: str = "CVC",
        security_code_length: int = 3,
    ) -> None:
        self.name = name
        self.prefixes = list(prefixes)
        self.length = length
        self.security_code = security_code
        self.security_code_length = security_code_length

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CreditCard):
            return NotImplemented
        return (self.name, self.prefixes, self.length) == (other.name, other.prefixes, other.length)

    def __repr__(self) -> str:
        return f"CreditCard(name={self.name!r}, length={self.length})"
