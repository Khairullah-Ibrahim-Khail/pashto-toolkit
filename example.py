"""Try the library out. In VS Code press the Run button (or F5) on this file."""

from pashto_toolkit import PashtoFaker

# No seed, so every run gives different data.
# Pass seed=42 if you want the SAME data every run (useful in tests).
pa = PashtoFaker("pa_AF")   # Pashto script
en = PashtoFaker("en_AF")   # Latin transliteration

print("=" * 60)
print("PASHTO (pa_AF)")
print("=" * 60)
print("name        :", pa.name())
print("father name :", pa.first_name_male())
print("job         :", pa.job())
print("province    :", pa.province())
print("city        :", pa.city())
print("district    :", pa.district())
print("address     :", pa.address())
print("postcode    :", pa.postcode())
print("phone       :", pa.phone_number())
print("tazkira ID  :", pa.afghan_id())
print("passport    :", pa.passport_number())
print("bank        :", pa.bank_name())
print("IBAN        :", pa.iban())
print("company     :", pa.company(), pa.company_suffix())
print("price       :", pa.pricetag())
print("month       :", pa.month_name())
print("weekday     :", pa.day_of_week())
print("colour      :", pa.color_name())
print("sentence    :", pa.sentence())
print("email       :", pa.email())
print("plate       :", pa.license_plate())
print("coordinates :", pa.local_latlng())

print()
print("=" * 60)
print("ENGLISH TRANSLITERATION (en_AF)")
print("=" * 60)
print("name        :", en.name())
print("province    :", en.province())
print("address     :", en.address())
print("phone       :", en.phone_number())
print("tazkira ID  :", en.afghan_id())
print("bank        :", en.bank_name())
print("month       :", en.month_name())
print("sentence    :", en.sentence())

print()
print("=" * 60)
print("A TABLE OF FAKE PEOPLE")
print("=" * 60)
people = PashtoFaker("pa_AF")           # no seed: different every run
for _ in range(8):
    print(f"{people.name():<28} {people.province():<12} {people.phone_number():<18} {people.afghan_id()}")

print()
print("=" * 60)
print("SEEDING: the same seed gives the same data")
print("=" * 60)
print("unseeded :", PashtoFaker('pa_AF').name(), "/", PashtoFaker('pa_AF').name(), " <- different")
print("seed=7   :", PashtoFaker('pa_AF', seed=7).name(), "/", PashtoFaker('pa_AF', seed=7).name(), " <- identical")

print()
print(f"{len(pa.formatters())} formatters available.")
print("Full list:", ", ".join(pa.formatters()))
