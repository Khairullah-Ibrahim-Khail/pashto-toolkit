# Pashto Toolkit

Afghanistan locales for [Faker](https://github.com/joke2k/faker): **`pa_AF`** (Pashto script) and **`en_AF`** (English transliteration).

Faker ships no Afghanistan locale, so `Faker("pa_AF")` raises `AttributeError` and `Faker()` gives you American names, US ZIP codes and dollar price tags. This package adds 18 localized providers for both locales and registers them with Faker so its normal API just works.

```python
import pashto_toolkit
from faker import Faker

pashto_toolkit.install()

fake = Faker("pa_AF")
fake.name()         # 'الحاج کبیر سور'
fake.province()     # 'کندهار'
fake.address()      # 'سړک پل محمود خان, پغمان ولسوالی, کابل ښار, کابل, 78192'
fake.afghan_id()    # '6768-223-117-276'  (valid Luhn check digit)
fake.bank_name()    # 'بانک ملي افغان'
fake.month_name()   # 'غويی'

Faker("en_AF").name()   # 'Tahir Dawlatzai'
```

## Install

```bash
pip install pashto-toolkit
```

Requires Python 3.9+ and `Faker>=24.5`.

Faker has marked more of its provider types as localizable over successive releases. On older Faker versions a type it does not localize — `isbn` before Faker 30, for example — keeps Faker's default provider, and the Afghanistan one for that type is simply unused. Everything else is unaffected. CI runs the suite against Faker 24.5, 28, 33, 39 and latest.

## The two locales

| | `pa_AF` | `en_AF` |
|---|---|---|
| Script | Pashto (Arabic script) | Latin transliteration |
| `name()` | `سيد دريا مومند` | `Khor Jamilah Maimana` |
| `province()` | `پنجشېر` | `Maidan Wardak` |
| `word()` | `پوښتنه` | English (Faker's `en_US` corpus) |
| `month_name()` | `مرغومی` | `Qaws` |

Machine-readable values stay Latin in both locales, because that is what they are in real life: email addresses, usernames, domains, SWIFT codes, licence plates, IBANs, barcodes and card numbers.

## Providers

`address` · `automotive` · `bank` · `barcode` · `color` · `company` · `credit_card` · `currency` · `date_time` · `geo` · `internet` · `isbn` · `job` · `lorem` · `passport` · `person` · `phone_number` · `ssn`

Notable locale-specific formatters:

- **`afghan_id(separator="-")`** — Afghan national ID (tazkira), `XXXX-XXX-XXX-XXX`, twelve digits plus a Luhn check digit. Also available as `ssn()`.
- **`province()` / `district()`** — all 34 provinces, with districts and provincial capitals mapped per province, so `city(province)` and `district(province)` stay internally consistent.
- **`month_name()` / `day_of_week()`** — Afghan solar calendar months (Hamal…Hut) and a week starting Saturday, not Gregorian names.
- **`license_plate()`** — plates built from Afghan province codes (31 of the 34 provinces).
- **`passport_number()` / `passport_dates()`** — Afghan passport formats with age-dependent validity.
- **`pricetag()`** — amounts in AFN.

## Two ways to use it

### Registered as a Faker locale (recommended)

```python
import pashto_toolkit
from faker import Faker

pashto_toolkit.install()
fake = Faker("pa_AF")
```

Or in one step:

```python
from pashto_toolkit import pashto_faker

fake = pashto_faker()           # pa_AF
fake = pashto_faker("en_AF")
```

This works with everything Faker does with locales, including multi-locale instances:

```python
fake = Faker(["pa_AF", "en_AF"])
fake["pa_AF"].name()
```

### Without touching Faker's internals

If you would rather not have the locales registered, attach the providers to a Faker instance directly. This is Faker's documented `add_provider` path and patches nothing:

```python
from faker import Faker
from pashto_toolkit import add_providers

fake = Faker()
add_providers(fake, locale="pa_AF")
fake.province()
```

## Seeding

Seeding is reproducible, which is the point of using Faker in tests:

```python
Faker.seed(4242)
fake = Faker("pa_AF")
fake.name()   # the same value on every run
```

## How the locale registration works

Faker resolves a locale by looking inside its own installed package: it checks `faker.config.AVAILABLE_LOCALES`, lists the directories under `faker/providers/<type>/`, then imports `faker.providers.<type>.<locale>`. A separate distribution cannot add directories there, so `install()` makes those same three lookups succeed from the outside — it appends to the `AVAILABLE_LOCALES` list (which `faker.factory` holds by reference), wraps `faker.factory.list_module` so the locales are reported, and registers the modules in `sys.modules` under the paths Faker will import.

Nothing is patched until you call `install()`, it is idempotent, and `pashto_toolkit.uninstall()` reverses it. If a future Faker release ships its own `pa_AF` or `en_AF`, that one wins — `install()` leaves any locale Faker already provides alone.

## Relationship to the upstream pull request

This started as [joke2k/faker#2293](https://github.com/joke2k/faker/pull/2293), which is still unmerged. Packaging it separately also meant fixing defects that the original branch carried:

- `afghan_id()` emitted 14 base digits instead of 12, so the Luhn check digit was computed and then sliced off — no generated ID validated.
- Every provider called the global `random` module, so `Faker.seed()` did not reproduce a run.
- The `lorem` locales were swapped: `en_AF` served the Pashto word list.
- The `address` providers subclassed the generic `BaseProvider` instead of Faker's address provider, so `postcode()`, `state()`, `street_name()`, `street_address()` and `country()` all raised `AttributeError`.
- `en_AF.month_name()` returned an empty string for one month in twelve, and `Hut` was unreachable.
- `name()` left a trailing space (`pa_AF`) and appended a lowercase tribal ending as a separate word (`en_AF`, `'Yahya amir'`).
- Honorific lists contained plain given names, so `prefix()` returned first names.
- Four name entries were two spelling variants joined by a double space; both spellings are kept, as separate entries.
- `username()` tested `self.first_names` against a Pashto string, so its `gender` argument was ignored; `user_name()` fell through to Faker's generic version.

The upstream branch also deleted `faker/providers/passport/__init__.py`, the base class the `de_AT`, `en_US` and `ru_RU` passport locales inherit from. That does not affect this package, which depends on an unmodified Faker.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

The tests assert the script and shape of generated values rather than just `isinstance(value, str)` — a provider that silently falls back to Faker's `en_US` data fails the suite instead of passing it.

## License

MIT — see [LICENSE](LICENSE).

Locale data is drawn from public knowledge of Afghan provinces, districts, institutions, names and calendar.
