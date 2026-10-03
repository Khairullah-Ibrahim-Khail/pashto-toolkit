"""The Afghan national ID is the one value here with a checkable invariant."""

import re

import pytest

from pashto_toolkit import PashtoFaker
from pashto_toolkit.fake.checksums import luhn_check_digit
from pashto_toolkit.fake.providers import LOCALES


@pytest.fixture(params=LOCALES)
def fake(request):
    return PashtoFaker(request.param)


def test_shape_is_four_three_three_three(fake):
    for _ in range(200):
        assert re.fullmatch(r"\d{4}-\d{3}-\d{3}-\d{3}", fake.afghan_id())


def test_check_digit_validates_under_luhn(fake):
    """Regression: the format emitted 14 digits, so the check digit was sliced off."""
    for _ in range(500):
        digits = fake.afghan_id().replace("-", "")
        assert len(digits) == 13, f"expected 13 digits, got {len(digits)} in {digits!r}"
        assert luhn_check_digit(digits[:-1]) == int(digits[-1]), f"bad check digit: {digits}"


def test_separator_is_configurable(fake):
    assert re.fullmatch(r"\d{13}", fake.afghan_id(separator=""))
    assert re.fullmatch(r"\d{4}/\d{3}/\d{3}/\d{3}", fake.afghan_id(separator="/"))


def test_ssn_is_the_same_number(fake):
    for _ in range(50):
        digits = fake.ssn().replace("-", "")
        assert len(digits) == 13
        assert luhn_check_digit(digits[:-1]) == int(digits[-1])


def test_does_not_start_with_zero(fake):
    for _ in range(200):
        assert not fake.afghan_id().startswith("0")
