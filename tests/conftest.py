import re

import pytest

import pashto_toolkit

# Arabic script blocks, which is what Pashto is written in.
ARABIC_SCRIPT = re.compile(r"[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")
LATIN_LETTERS = re.compile(r"[A-Za-z]")


@pytest.fixture(scope="session", autouse=True)
def _registered():
    """Register the Afghanistan locales once for the whole test session."""
    pashto_toolkit.install()


@pytest.fixture
def pa():
    from faker import Faker

    return Faker("pa_AF")


@pytest.fixture
def en():
    from faker import Faker

    return Faker("en_AF")


def assert_pashto(value, label=""):
    """Assert ``value`` is Pashto text: Arabic script and no Latin letters."""
    assert isinstance(value, str), f"{label}: expected str, got {type(value).__name__}"
    assert value.strip() == value, f"{label}: leading/trailing whitespace in {value!r}"
    assert value, f"{label}: empty"
    assert ARABIC_SCRIPT.search(value), f"{label}: no Arabic-script characters in {value!r}"
    assert not LATIN_LETTERS.search(value), f"{label}: unexpected Latin letters in {value!r}"


def assert_latin(value, label=""):
    """Assert ``value`` is Latin text with no Arabic-script characters."""
    assert isinstance(value, str), f"{label}: expected str, got {type(value).__name__}"
    assert value.strip() == value, f"{label}: leading/trailing whitespace in {value!r}"
    assert value, f"{label}: empty"
    assert not ARABIC_SCRIPT.search(value), f"{label}: unexpected Arabic script in {value!r}"
