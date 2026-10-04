# Pashto Toolkit

Realistic Afghan test data, in Pashto script and in Latin transliteration.

No dependencies. Nothing to configure. Seed it and a run repeats exactly.

```python
from pashto_toolkit import PashtoFaker

fake = PashtoFaker()                  # pa_AF, Pashto script

fake.name()                           # 'بی بی نجیبه افغان'
fake.province()                       # 'لغمان'
fake.phone_number()                   # '+93 40 872 510'
fake.afghan_id()                      # '3041-575-087-425'
fake.bank_name()                      # 'پښتني بانک'
fake.pricetag()                       # '19,540 ؋'
```

The same data transliterated, for systems that cannot store Pashto script:

```python
fake = PashtoFaker("en_AF")

fake.name()                           # 'Nia Kalsoom Nimruz'
fake.province()                       # 'Laghman'
fake.city()                           # 'Sar-e Pol'
```

## Install

```bash
pip install pashto-toolkit
```

Python 3.9 or newer. There are no runtime dependencies — the generator, the
check-digit algorithms and all the data are part of the package.

## Why this exists

Reach for a general-purpose faker and an Afghan record comes out looking
American: a US ZIP code, a dollar price tag, Gregorian month names, a name
drawn from a census of Ohio. That is no use for testing a system that will
hold Afghan data.

Everything here is Afghan: the 34 provinces with their real districts and
capitals, the mobile ranges the networks actually use, the banks that
actually operate, the solar calendar, the afghani, and the national ID with a
check digit that validates.

## The two locales

| | `pa_AF` | `en_AF` |
|---|---|---|
| Script | Pashto, Arabic script | Latin transliteration |
| For | Afghan-facing systems, Pashto UI, right-to-left rendering | systems that cannot store Pashto script, logs, URLs, legacy databases |

They share one data set, so the same province list, bank list and calendar
back both. Side by side:

| | `pa_AF` | `en_AF` |
|---|---|---|
| `name()` | بی بی نجیبه افغان | Nia Kalsoom Nimruz |
| `province()` | لغمان | Laghman |
| `city()` | سرپل | Sar-e Pol |
| `street_name()` | سړک دارالامان | Darulaman Road |
| `bank_name()` | پښتني بانک | Pashtany Bank |
| `company()` | بیات بریښنا شرکت | Bayat Power |
| `job()` | د هټۍ مرستیال | Firefighter |
| `month_name()` | وری | Saratān |
| `day_of_week()` | یونۍ | Manznay |
| `color_name()` | شیرشکري | Slate Gray |
| `currency_name()` | پاکستانۍ کلدارې | Indian rupee |
| `word()` | له | person |
| `pricetag()` | 19,540 ؋ | AFN 19,540,733 |

Values that are machine-readable in real life stay Latin in both locales,
because that is what they are: email addresses, usernames, domains,
SWIFT/BIC codes, IBANs, licence plates, barcodes, card numbers.

| | both locales |
|---|---|
| `email()` | khialay.davlat87@mail.com |
| `afghan_id()` | 3041-575-087-425 |
| `phone_number()` | +93 40 872 510 |
| `iban()` | AF489698142841487463 |
| `license_plate()` | FA 02 958 |
| `postcode()` | 56673 |

## Afghanistan-specific formatters

- **`afghan_id()`** — national ID, the tazkira number. `XXXX-XXX-XXX-XXX`:
  twelve digits and a Luhn check digit. Also reachable as `ssn()`.
  `afghan_id(separator="")` gives bare digits.
- **`province()`, `city()`, `district()`** — all 34 provinces, each with its
  capital and its districts. Pass a province and the rest follows it:
  `district("کابل")` returns a district of Kabul, not of somewhere else.
- **`month_name()`, `day_of_week()`** — the Afghan solar calendar,
  Hamal through Hut, and a week that starts on Saturday.
- **`phone_number()`** — the mobile ranges in use, +93 70x to 79x, and
  provincial landline codes. `msisdn()` for the bare E.164 form,
  `e164()` with the plus.
- **`license_plate()`** — Afghan province plate codes.
- **`bank_name()`, `iban()`, `swift()`** — banks that operate in
  Afghanistan. IBANs carry correct ISO 13616 check digits; a BIC is a valid
  8 or 11 characters.
- **`passport_number()`, `passport_dates()`** — Afghan passport formats,
  with validity that depends on the holder's age.
- **`pricetag()`** — afghani, with the sign where Afghan prices put it.
- **`local_latlng()`** — a coordinate inside Afghanistan.

Every value with a check digit has a correct one: Luhn for IDs and card
numbers, GS1 for EAN-8, EAN-13, UPC-A and UPC-E, mod-11 for ISBN-10, mod-10
for ISBN-13, mod-97 for IBAN.

## Everything else

Alongside the Afghan data are the general-purpose formatters any test suite
needs, so you should not need a second library: people and addresses,
internet and network values, dates and times, files and MIME types, hashes
and UUIDs and passwords, Python values, browser user agents, whole-person
profiles, and serialised output in JSON, CSV, TSV, XML, ZIP and tar.

Rather than trust a list in a README, ask:

```python
fake = PashtoFaker()

len(fake.formatters())                # how many there are
fake.formatters()                     # every name, sorted
fake.has_formatter("afghan_id")       # True
[n for n in fake.formatters() if "mail" in n]
```

US-specific formatters are deliberately absent — `zipcode`, `state_abbr`,
`ein`, `itin`, `aba`, the military post codes. They describe American postal
and tax systems and have no Afghan meaning.

## Seeding

A seed makes a run repeat, which is what makes generated data usable in a
test you expect to pass twice:

```python
fake = PashtoFaker("pa_AF", seed=4242)
fake.name()                 # the same value on every run, on every machine

fake.seed(4242)             # start the sequence again
```

Formatters that read the clock — `past_datetime()`, `future_datetime()`,
`time_series()` — repeat their offset from now rather than an absolute
moment, since "now" moves between runs.

## Building records

A record should describe one person, so take it from `profile()` rather than
calling the formatters separately. Called separately they are independent,
and a row ends up with one person's name beside another's email.

```python
fake.simple_profile()
# {'username': 'mirzal.umar739',
#  'name': 'Mirzal Umar',
#  'sex': 'M',
#  'address': ...,
#  'mail': 'mirzal.umar739@afghanmail.af',
#  'birthdate': datetime.date(1974, 3, 9)}

fake.profile()                      # the full record
fake.profile(sex="F")               # a woman
fake.profile(fields=["name", "job", "mail"])
```

The name, username and email agree. In `en_AF` the email is built from the
name. In `pa_AF` the display name is in Pashto script and there is no
transliteration table here, so the username is drawn from the Latin pools; it
still matches the email, and the gender still matches the record.

For a table, the serialisation formatters take the columns you want:

```python
import json

rows = json.loads(fake.json(
    data_columns=[("name", "name"), ("province", "province"),
                  ("phone", "phone_number"), ("id", "afghan_id")],
    num_rows=50,
))

fake.csv(num_rows=50)               # also tsv, psv, dsv, xml, fixed_width
fake.zip(num_files=3)               # a real archive, as bytes
```

## Using the generator directly

`PashtoFaker()` builds a `Generator` and registers every provider on it. Do
that yourself when you want to mix in providers of your own:

```python
from pashto_toolkit import Generator, add_providers
from pashto_toolkit.fake import BaseProvider

class TicketProvider(BaseProvider):
    def ticket_id(self):
        return self.bothify("TKT-####-??")

gen = Generator("pa_AF", seed=1)
add_providers(gen, "pa_AF")
gen.add_provider(TicketProvider)     # added last, so it wins any name clash

gen.ticket_id()                      # 'TKT-2914-hF'
gen.province()                       # 'کندهار'
gen.parse("{{first_name}} — {{province}}")
```

A generator exposes `formatters()`, `has_formatter(name)`,
`format(name, ...)` to call one by name, `parse(template)` to expand
`{{token}}` placeholders, and `seed(n)`.

## Writing a provider

Subclass `BaseProvider`, keep the data in class attributes, and draw from it
with `self.random_element`. Never use the `random` module directly, or
seeding stops working for your provider.

```python
from pashto_toolkit.fake import BaseProvider

class TeaProvider(BaseProvider):
    teas = ("شین چای", "تور چای", "قیماق چای")

    def tea(self):
        return self.random_element(self.teas)
```

`BaseProvider` gives you `random_element`, `random_elements`, `random_int`,
`random_number`, `random_digit`, `random_letter`, and three template helpers:
`numerify` (`#` a digit, `%` 1-9, `$` 2-9, `!` a digit or nothing), `lexify`
(`?` a letter) and `bothify` (both).

To localise an existing type instead, subclass its provider and replace the
data. Each provider type is a package: the base `Provider` holds the
behaviour that is not language-specific, and each locale subpackage holds the
Afghan data.

```
pashto_toolkit/
└── fake/
    ├── core.py        Generator, BaseProvider, the seeded RNG, {{token}} parsing
    ├── checksums.py   Luhn, GS1, ISBN-10, ISBN-13
    └── providers/
        ├── person/
        │   ├── __init__.py   the base provider
        │   ├── pa_AF/        Pashto data
        │   └── en_AF/        transliterated data
        └── …
```

## About the data

Written in standard Afghan Pashto orthography, and tested for it: Pashto
`ی` rather than Arabic `ي` except word-finally where it is grammatical,
Pashto `ک` and `ګ` rather than the Arabic and Persian forms, and `آ`
preserved in the place names that carry it.

The data is checked, not just present. Tests assert the script and shape of
what each formatter returns, verify every check digit, hold the province,
district and capital tables in agreement, keep the men's and women's name
pools separate, and reject duplicate entries, which would quietly make some
names likelier than others.

Place names, institutions, the calendar and personal names come from public
knowledge of Afghanistan.

## Scope

`pashto_toolkit.fake` is the first module. The package name leaves room for
the rest of the Pashto tooling to join it, which is why the generator lives
under `.fake` rather than at the top level. Importing `PashtoFaker` from
`pashto_toolkit` will keep working either way.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

## License

MIT. See [LICENSE](https://github.com/Khairullah-Ibrahim-Khail/pashto-toolkit/blob/main/LICENSE).
