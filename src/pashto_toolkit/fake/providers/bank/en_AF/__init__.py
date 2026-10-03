from .. import Provider as BankProvider


class Provider(BankProvider):
    """Afghan Bank provider in English"""

    country_code = "AF"
    # The BBAN excludes the country code; iban() prepends it with the
    # check digits. Afghanistan has no registered IBAN format, so this is
    # a plausible 16-digit basic account number.
    bban_format = "################"

    swift_bank_codes = (
        "DAAF", "AZBK", "KBLK", "MWBK", "PSBK",
        "AUAF", "FMBK", "STCA", "BMIA", "GHZN",
    )
    swift_location_codes = ("KA", "HE", "LO", "PA", "KU", "BE", "FA", "ZA", "JO", "GH")
    swift_branch_codes = ("001", "002", "003", "004", "005", "ATM", "HQ", "BR1", "BR2")

    banks = (
        "Da Afghanistan Bank",
        "Azizi Bank",
        "Kabul Bank",
        "Maiwand Bank",
        "Pashtany Bank",
        "Afghan United Bank",
        "First MicroFinance Bank",
        "Standard Chartered Bank Afghanistan",
        "Bank-e-Millie Afghan",
        "Ghazanfar Bank",
    )

    def bank_name(self):
        return self.generator.random.choice(self.banks)

    def account_number(self):
        return "AF" + "".join(str(self.generator.random.randint(0, 9)) for _ in range(16))

    def swift_code(self):
        bank_code = self.generator.random.choice(self.swift_bank_codes)
        location = self.generator.random.choice(self.swift_location_codes)
        branch = self.generator.random.choice(self.swift_branch_codes)
        return f"{bank_code}{location}{branch}"
