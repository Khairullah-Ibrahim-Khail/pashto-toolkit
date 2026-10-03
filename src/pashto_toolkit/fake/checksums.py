"""Check-digit algorithms used by the generated identifiers."""

from typing import Sequence


def luhn_check_digit(digits: str) -> int:
    """Return the Luhn check digit for a string of digits."""
    total = 0
    for position, char in enumerate(reversed(digits)):
        value = int(char)
        if position % 2 == 0:
            value *= 2
            if value > 9:
                value -= 9
        total += value
    return (10 - total % 10) % 10


def luhn_is_valid(digits: str) -> bool:
    """True when the final digit is a correct Luhn check digit."""
    if len(digits) < 2 or not digits.isdigit():
        return False
    return luhn_check_digit(digits[:-1]) == int(digits[-1])


def ean_check_digit(digits: str) -> int:
    """Return the GS1 check digit for an EAN-8/EAN-13/UPC-A body.

    Weights alternate 3 and 1 from the rightmost body digit leftwards.
    """
    total = 0
    for position, char in enumerate(reversed(digits)):
        total += int(char) * (3 if position % 2 == 0 else 1)
    return (10 - total % 10) % 10


def isbn10_check_digit(digits: Sequence[str]) -> str:
    """Return the ISBN-10 check character, which may be ``X``."""
    total = sum((10 - index) * int(char) for index, char in enumerate(digits))
    remainder = (11 - total % 11) % 11
    return "X" if remainder == 10 else str(remainder)


def isbn13_check_digit(digits: Sequence[str]) -> str:
    """Return the ISBN-13 check digit."""
    total = sum(int(char) * (1 if index % 2 == 0 else 3) for index, char in enumerate(digits))
    return str((10 - total % 10) % 10)
