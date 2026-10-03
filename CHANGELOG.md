# Changelog

## 0.1.0

First release: Afghan test data in Pashto script (`pa_AF`) and Latin transliteration (`en_AF`), with **no runtime dependencies**.

- 18 provider types, 144 formatters, per locale.
- Own generator core: seeded RNG, provider registration and dispatch, `{{token}}` template expansion, and `numerify`/`lexify`/`bothify` placeholder expansion.
- Own check-digit implementations, all verified against reference values: Luhn (national ID, card numbers), GS1 (EAN-13, EAN-8, UPC-A), ISBN-10, ISBN-13, and ISO 13616 mod-97 (IBAN).
- Seeding reproduces a run exactly.

### Origin

The locale data began as [joke2k/faker#2293](https://github.com/joke2k/faker/pull/2293). That pull request went unreviewed for nine months, so this is a standalone library with its own generator rather than a Faker plugin.

### Defects fixed relative to that branch

- `afghan_id()` generated 14 base digits instead of 12, so the Luhn check digit was computed and then discarded by the grouping slice. No generated ID validated; now all do.
- Every provider used the global `random` module, which seeding does not control, so runs were not reproducible.
- The `lorem` providers were inverted: the English locale carried the Pashto word list. `pa_AF` now holds the Pashto corpus and `en_AF` has its own English one.
- The `address` providers subclassed a generic base rather than an address provider, so `postcode()`, `state()`, `street_name()`, `street_address()`, `building_number()` and `country()` raised `AttributeError`.
- `en_AF.month_names` had two leading empty entries, so `month_name()` returned `""` for one month in twelve and never produced `Hut`.
- `pa_AF.name()` returned a trailing space; `en_AF.name()` appended a lowercase tribal ending as a separate word even though the family names already carry those endings. An honorific was also applied to every name, and now appears on about a quarter.
- Honorific lists included plain given names (`نجيب`, `غلام`, `ظاهر`, `Aziz`, `Karim`, `Dost`), so `prefix()` returned first names. `Jan`, described in its own comment as a suffix, was listed as a prefix.
- `username()` compared an internal name table against a Pashto string, so its `gender` argument was silently ignored, and `user_name()` was missing entirely.
- Two-word names such as "Bakht Awar" left a space inside generated email addresses.
- Four `pa_AF` given-name entries were two spelling variants joined by a double space (`'روشان  روښان'`), emitted verbatim by `name()`. Split into separate entries, keeping both spellings.
- The `بدغيس` districts key was spelled differently from the provinces entry, so `district("بدغيس")` returned the province name.
- `pa_AF.bank_name()` returned English bank names, `company_suffix()` returned `Inc`, and `currency_name()` returned English names in the Pashto locale.
- `passport_dates()` took `birthday: date = date.today()`, freezing the default at import time, and `passport_gender(seed=...)` seeded the global RNG.
- Stray whitespace in several data entries, and a Latin-acronym company name in the Pashto list.
