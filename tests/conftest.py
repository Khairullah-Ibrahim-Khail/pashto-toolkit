import re

import pytest

from pashto_toolkit import PashtoFaker

# Arabic script blocks, which is what Pashto is written in.
ARABIC_SCRIPT = re.compile(r"[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")
LATIN_LETTERS = re.compile(r"[A-Za-z]")


@pytest.fixture
def pa():
    return PashtoFaker("pa_AF")


@pytest.fixture
def en():
    return PashtoFaker("en_AF")


def assert_pashto(value, label=""):
    """Assert ``value`` is Pashto text: Arabic script and no Latin letters."""
    assert isinstance(value, str), f"{label}: expected str, got {type(value).__name__}"
    assert value, f"{label}: empty"
    assert value.strip() == value, f"{label}: leading/trailing whitespace in {value!r}"
    assert ARABIC_SCRIPT.search(value), f"{label}: no Arabic-script characters in {value!r}"
    assert not LATIN_LETTERS.search(value), f"{label}: unexpected Latin letters in {value!r}"


def assert_latin(value, label=""):
    """Assert ``value`` is Latin text with no Arabic-script characters."""
    assert isinstance(value, str), f"{label}: expected str, got {type(value).__name__}"
    assert value, f"{label}: empty"
    assert value.strip() == value, f"{label}: leading/trailing whitespace in {value!r}"
    assert not ARABIC_SCRIPT.search(value), f"{label}: unexpected Arabic script in {value!r}"
