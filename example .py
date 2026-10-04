"""Try the library out. In VS Code press the Run button (or F5) on this file."""

from pashto_toolkit import PashtoFaker

# No seed, so every run gives different data.
# Pass seed=42 if you want the SAME data every run (useful in tests).
pa = PashtoFaker("en_AF")   # Pashto script
print(pa.name())
print(pa.address())
print(pa.email())
print(pa.phone_number())