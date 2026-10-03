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
    # A BIC branch code is exactly 3 characters; XXX means the primary office.
    swift_branch_codes = ("001", "002", "003", "004", "005", "ATM", "XXX", "BR1", "BR2")

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
        """An 11-character BIC. Alias of ``swift(11)``.

        A BIC is 4 bank characters, 2 country, 2 location and an optional 3
        for the branch, so the country code cannot be left out.
        """
        return self.swift(11)
