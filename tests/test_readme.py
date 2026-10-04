"""The README must stay true as the package changes.

It is also the PyPI project page, so a stale claim there is published. These
tests read it and check it against the code rather than trusting it.
"""

import pathlib
import re

import pytest

from pashto_toolkit import PashtoFaker
from pashto_toolkit.fake.providers import LOCALES

README = pathlib.Path(__file__).resolve().parent.parent / "README.md"


@pytest.fixture(scope="module")
def readme():
    assert README.exists(), f"{README} is missing"
    return README.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def formatters():
    return set(PashtoFaker().formatters())


def test_every_formatter_the_readme_names_exists(readme, formatters):
    """A renamed or dropped formatter must not be left documented."""
    # `name()` in backticks, and fake.name() / gen.name() in the samples
    mentioned = set(re.findall(r"`([a-z_][a-z0-9_]*)\(\)`", readme))
    mentioned |= set(re.findall(r"\b(?:fake|gen|en|pa)\.([a-z_][a-z0-9_]*)\(", readme))
    # methods of the generator itself, not formatters
    mentioned -= {
        "formatters", "has_formatter", "format", "parse", "seed", "add_provider",
        "PashtoFaker", "Generator", "add_providers", "current_locale",
    }
    # formatters the README's own sample providers define, which are
    # illustrations rather than something the package ships
    mentioned -= set(re.findall(r"def ([a-z_][a-z0-9_]*)\(self", readme))
    assert mentioned, "no formatters found in the README; has its format changed?"
    missing = sorted(mentioned - formatters)
    assert not missing, f"the README documents formatters that do not exist: {missing}"


def test_the_readme_states_no_formatter_count(readme):
    """Counts go stale on the next release, so the README tells the reader to
    ask the package instead."""
    counts = re.findall(r"\b\d{2,4}\s+formatters\b", readme)
    assert not counts, f"remove the hardcoded counts and let formatters() answer: {counts}"
    types = re.findall(r"\b\d+\s+provider types\b", readme)
    assert not types, f"remove the hardcoded provider-type counts: {types}"


def test_the_readme_pins_no_version(readme):
    """The version lives in pyproject.toml; two places drift apart."""
    versions = re.findall(r"\b\d+\.\d+\.\d+\b", readme)
    allowed = {"13616"}          # the ISO standard number, not a version
    stray = [v for v in versions if v not in allowed]
    assert not stray, f"the README pins a version: {stray}"


def test_the_readme_links_are_absolute(readme):
    """PyPI renders the README outside the repository, so a relative link 404s."""
    relative = re.findall(r"\]\((?!https?://|#)([^)]+)\)", readme)
    assert not relative, f"these links break on the PyPI page: {relative}"


def test_the_locales_the_readme_names_are_the_ones_shipped(readme):
    for locale in LOCALES:
        assert f"`{locale}`" in readme, f"{locale} is not documented"
    claimed = set(re.findall(r"`([a-z]{2}_[A-Z]{2})`", readme))
    assert claimed == set(LOCALES), f"README documents {claimed}, package ships {set(LOCALES)}"


def test_the_us_formatters_the_readme_calls_absent_really_are(readme, formatters):
    named = set(re.findall(r"`(zipcode|state_abbr|ein|itin|aba)`", readme))
    assert named, "the README no longer lists the deliberately absent formatters"
    present = sorted(named & formatters)
    assert not present, f"the README says these are absent but they exist: {present}"


def test_the_python_floor_matches_pyproject(readme):
    pyproject = (README.parent / "pyproject.toml").read_text(encoding="utf-8")
    floor = re.search(r'requires-python\s*=\s*"[^0-9]*(\d+\.\d+)"', pyproject)
    assert floor, "requires-python not found in pyproject.toml"
    major_minor = floor.group(1)
    assert f"Python {major_minor}" in readme, (
        f"pyproject requires Python {major_minor}; the README should say so"
    )
