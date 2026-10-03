# Changelog

## 0.1.0

First release. Afghanistan locales `pa_AF` (Pashto) and `en_AF` (English transliteration) for Faker, covering 18 provider types.

Packaged from [joke2k/faker#2293](https://github.com/joke2k/faker/pull/2293), with these defects in that branch fixed:

- `afghan_id()` generated 14 base digits instead of 12, so the Luhn check digit was computed and then discarded by the grouping slice. No generated ID validated. Now 13 digits with a valid check digit, and exposed as `ssn()` too.
- Every provider used the global `random` module, which `Faker.seed()` does not control, so runs were not reproducible. All randomness now goes through `self.generator.random`, and a test guards against regressions.
- The `lorem` providers were inverted: `en_AF` carried the Pashto word list and `pa_AF` inherited it. `pa_AF` now holds the Pashto corpus; `en_AF` uses Faker's English one.
- The `address` providers subclassed the generic `BaseProvider` rather than Faker's address provider, so `postcode()`, `state()`, `street_name()`, `street_address()`, `building_number()` and `country()` raised `AttributeError`. The standard contract is now wired to the Afghan data, with `current_country_code()` returning `AF`.
- `en_AF.month_names` had two leading empty entries, so `month_name()` returned `""` for one month in twelve and never produced `Hut`.
- `pa_AF.name()` returned a trailing space; `en_AF.name()` appended a lowercase tribal ending as a separate word (`'Yahya amir'`) even though the family names already carry those endings. Both now compose cleanly, and an honorific appears on roughly a quarter of names instead of every one.
- Honorific lists included plain given names (`نجيب`, `غلام`, `ظاهر`, `Aziz`, `Karim`, `Dost`), so `prefix()` returned first names. `Jan`, documented in its own comment as a suffix, was listed as a prefix.
- `pa_AF.username()` compared `self.first_names` — Faker's own name table — against a Pashto string, so its `gender` argument was silently ignored. `user_name()` was also missing, so Faker's standard formatter fell through to the generic version.
- Four `pa_AF` given-name entries were two spelling variants joined by a double space (`'روشان  روښان'`), which `name()` emitted verbatim. Split into separate entries, keeping both spellings.
- The `بدغيس` districts key was spelled differently from the provinces entry, so `district("بدغيس")` returned the province name.
- `pa_AF.bank_name()` returned English bank names; `company_suffix()` returned `Inc` in both locales.
- `passport_dates()` took `birthday: date = date.today()`, freezing the default at import time, and `passport_gender(seed=...)` seeded the global RNG rather than Faker's.
- Stray whitespace in several data entries, and a Latin-acronym company name in the Pashto list.
