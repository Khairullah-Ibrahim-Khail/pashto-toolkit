# Pashto Toolkit

Realistic Afghan test data in Pashto script and Latin transliteration. **No dependencies.**

```python
from pashto_toolkit import PashtoFaker

fake = PashtoFaker()              # pa_AF — Pashto script
fake.name()                       # 'شوغله ملا'
fake.province()                   # 'بدغيس'
fake.address()                    # 'جاده احمد شاه بابا, ازره ولسوالی, پل علم ښار, لوګر, 87236'
fake.afghan_id()                  # '4021-573-681-931'  (valid Luhn check digit)
fake.phone_number()               # '+93 703 642 621'
fake.bank_name()                  # 'اسلامي بانک افغانستان'
fake.month_name()                 # 'وری'
fake.pricetag()                   # '64,139 ؋'

english = PashtoFaker("en_AF")    # Latin transliteration
english.name()                    # 'Elham Fars'
english.province()                # 'Khost'
```

## Install

```bash
pip install pashto-toolkit
```

Python 3.9+. Nothing else — no runtime dependencies at all.

## The two locales

| | `pa_AF` | `en_AF` |
|---|---|---|
| Script | Pashto (Arabic script) | Latin transliteration |
| `name()` | `سيد دريا مومند` | `Tahir Dawlatzai` |
| `province()` | `پنجشېر` | `Maidan Wardak` |
| `bank_name()` | `بانک ملي افغان` | `Bank-e-Millie Afghan` |
| `currency_name()` | `افغانۍ` | `Afghan afghani` |
| `word()` | `لار` | `settle` |
| `month_name()` | `مرغومی` | `Qaws` |

Machine-readable values stay Latin in both locales, because that is what they are in real life: email addresses, usernames, domains, SWIFT/BIC codes, IBANs, licence plates, barcodes and card numbers.

## What it generates

18 provider types, 133 formatters. The Afghanistan-specific ones:

- **`afghan_id()`** — national ID (tazkira), `XXXX-XXX-XXX-XXX`: twelve digits plus a Luhn check digit. Also `ssn()`.
- **`province()` / `city()` / `district()`** — all 34 provinces, each with its capital and its districts. `city(province)` and `district(province)` stay consistent with the province you pass.
- **`month_name()` / `day_of_week()`** — Afghan solar calendar (Hamal…Hut) and a week starting Saturday, not Gregorian names.
- **`phone_number()`** — real Afghan mobile ranges (+93 70x–79x) and provincial landline codes.
- **`license_plate()`** — Afghan province plate codes.
- **`bank_name()` / `iban()` / `swift()`** — Afghan banks; IBANs carry correct ISO 13616 mod-97 check digits.
- **`passport_number()` / `passport_dates()`** — Afghan passport formats with age-dependent validity.
- **`pricetag()`** — amounts in afghani, with the sign where Afghan prices put it.
- **`local_latlng()`** — coordinates inside Afghanistan's bounding box.

Everything with a check digit has a correct one: Luhn for IDs and card numbers, GS1 for EAN-13/EAN-8/UPC-A, mod-11 for ISBN-10, mod-10 for ISBN-13, mod-97 for IBAN.

## Seeding

A seed reproduces a run exactly:

```python
fake = PashtoFaker("pa_AF", seed=4242)
fake.name()          # same value on every run, on every machine

fake.seed(4242)      # restart the sequence
```

## Using the generator directly

`PashtoFaker()` is a thin wrapper that builds a `Generator` and registers every provider on it. You can do that yourself and mix in providers of your own:

```python
from pashto_toolkit import Generator, add_providers
from pashto_toolkit.fake import BaseProvider

class MyProvider(BaseProvider):
    def ticket_id(self):
        return self.bothify("TKT-####-??")

gen = Generator("pa_AF", seed=1)
add_providers(gen, "pa_AF")
gen.add_provider(MyProvider)      # added last, so it wins any name clash

gen.ticket_id()                   # 'TKT-2914-hF'
gen.province()                    # 'کندهار'
gen.parse("{{first_name}} — {{province}}")
```

Useful generator methods: `formatters()` lists every available name, `has_formatter(name)` checks one, `format(name, ...)` calls one by name, and `parse(template)` expands `{{token}}` placeholders.

## Writing your own provider

Subclass `BaseProvider`. Put the data in class attributes and draw from it with `self.random_element`; never use the `random` module directly, or seeding stops working.

```python
from pashto_toolkit.fake import BaseProvider

class TeaProvider(BaseProvider):
    teas = ("شین چای", "تور چای", "قیماق چای")

    def tea(self):
        return self.random_element(self.teas)
```

`BaseProvider` gives you `random_element`, `random_elements`, `random_int`, `random_digit`, `numerify` (`#` → digit, `%` → 1-9, `$` → 2-9, `!` → digit or nothing), `lexify` (`?` → letter), `bothify` and `parse`.

## Layout

```
pashto_toolkit/
├── fake/
│   ├── core.py        Generator, BaseProvider, seeded RNG, {{token}} parsing
│   ├── checksums.py   Luhn, GS1/EAN, ISBN-10, ISBN-13
│   ├── types.py       CreditCard, SexLiteral
│   └── providers/
│       ├── person/            base provider + the generic behaviour
│       │   ├── pa_AF/         Pashto data
│       │   └── en_AF/         transliterated data
│       └── … 17 more types
```

Each provider type is a package: the base `Provider` holds behaviour that is not language-specific, and each locale subpackage holds the Afghan data.

## Background

This began as [joke2k/faker#2293](https://github.com/joke2k/faker/pull/2293), a pull request adding Afghanistan locales to Faker. It sat unreviewed for nine months, so the work is now a library in its own right, with its own generator and no dependency on Faker.

Becoming standalone also meant fixing defects the original branch carried:

- `afghan_id()` produced 14 base digits instead of 12, so the Luhn check digit was computed and then sliced off. No generated ID validated. Now every one does.
- Every provider used the global `random` module, which seeding does not control, so runs were not reproducible.
- The `lorem` locales were inverted: the English locale served the Pashto word list.
- The `address` providers were missing the whole standard address contract — `postcode()`, `state()`, `street_name()`, `street_address()` all raised `AttributeError`.
- `en_AF.month_name()` returned an empty string for one month in twelve, and `Hut` was unreachable.
- `name()` left a trailing space in `pa_AF`, and in `en_AF` appended a lowercase tribal ending as a separate word even though the family names already carry those endings.
- Honorific lists contained plain given names, so `prefix()` returned first names.
- `username()` tested an internal name table against a Pashto string, so its `gender` argument was ignored.
- Two-word names such as "Bakht Awar" left a space inside generated email addresses.
- Four Pashto given-name entries were two spelling variants joined by a double space. Both spellings are kept, as separate entries.
- The `بدغيس` districts key was spelled differently from the provinces entry, so `district("بدغيس")` returned the province name.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

The tests assert the script and shape of generated values and verify every check digit, rather than just checking a string came back. A provider that silently returns the wrong language fails the suite.

## Scope

`pashto_toolkit.fake` is the first module. The name leaves room for the other Pashto tooling to join it later.

## License

MIT — see [LICENSE](LICENSE).

Locale data reflects public knowledge of Afghan provinces, districts, institutions, names and the Afghan calendar.
