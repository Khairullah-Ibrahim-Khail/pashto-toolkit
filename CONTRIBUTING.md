# Contributing

Corrections to the Pashto data are the most valuable kind of contribution. The
code was written by someone who can read Pashto but is not a linguist, and a
native speaker will spot things the tests cannot.

## Getting set up

```bash
git clone https://github.com/Khairullah-Ibrahim-Khail/pashto-toolkit
cd pashto-toolkit
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
.venv/bin/ruff check .
```

There are no runtime dependencies and there is nothing to configure. If the
tests pass, you are ready.

## Correcting the data

This is the part that needs outside eyes. If a name is misspelled, a district
is in the wrong province, a surname is really a given name, or a word is not
how Afghans actually write it, please say so — an issue is enough, a pull
request is better.

The data lives in one file per provider type and locale:

```
src/pashto_toolkit/fake/providers/person/pa_AF/__init__.py     Pashto script
src/pashto_toolkit/fake/providers/person/en_AF/__init__.py     transliteration
src/pashto_toolkit/fake/providers/address/pa_AF/__init__.py    provinces, districts
```

### The rules the data follows

These are enforced by the tests, so a change that breaks one will fail CI.

**Letter forms.** Standard Afghan Pashto orthography:

| use | not | note |
|---|---|---|
| `ی` U+06CC | `ي` U+064A | `ي` only word-finally, where it is grammatical: احمدزي, اسلامي |
| `ک` U+06A9 | `ك` U+0643 | the Arabic kaf is never correct here |
| `ګ` U+06AB | `گ` U+06AF | the Persian gaf is never correct here |
| `ه` U+0647 | `ہ` U+06C1 | the Urdu heh is never correct here |

`آ` is preserved, never folded to `ا`. Place names carry it: فيض آباد,
اسدآباد, دوآب, آقچه.

**Name pools are separated by gender.** A women's name does not belong in the
male list. Words Afghans genuinely use for either sex stay in both, and that
list is pinned in the tests — add to it deliberately, with a note, rather than
to make a failure go away.

**Surnames are surnames.** Not female given names, not place names in the
wrong form (`قندهاري`, not `قندهار`), not common nouns.

**No duplicates.** The same entry twice makes that value twice as likely. If
two spellings are both current, keep both as separate entries, not merged into
one string.

**No stray whitespace**, and no double spaces inside an entry.

**Provinces, capitals and districts agree.** `province()`, `city(province)`
and `district(province)` key off the same spelling, so all three tables must
use it.

### If a test blocks a change you believe is right

Say so in the pull request. The tests encode one person's judgement about
Pashto, and that judgement can be wrong. Change the test and explain why,
rather than working around it.

## Adding a formatter

Put it on the base provider for its type if the behaviour is not
language-specific, and on the locale provider if it is. Draw randomness from
`self.random_element`, `self.random_int` and the other `BaseProvider` helpers.
Never use the `random` module directly — seeding stops working for your
provider, and a test will catch it.

Anything with a check digit gets a correct one. The algorithms are in
`src/pashto_toolkit/fake/checksums.py`.

## Adding a locale

The package is not limited to Afghanistan by design, only by what has been
written. Dari (`fa_AF`) would be the obvious next one. A locale is a
subpackage per provider type holding the data; the base providers supply the
behaviour.

## Pull requests

- One change per pull request.
- `pytest` and `ruff check .` pass. CI runs them on every Python version the
  package supports.
- New behaviour comes with a test. A data correction comes with a sentence on
  why the old value was wrong.
- No runtime dependencies. A test walks every module and fails on any
  non-standard-library import.

## Reporting something without fixing it

An issue naming the wrong value and what it should be is genuinely useful. You
do not need to write code.
