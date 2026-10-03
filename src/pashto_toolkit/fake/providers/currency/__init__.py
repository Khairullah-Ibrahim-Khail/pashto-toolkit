"""Base currency provider, centred on the Afghani."""

from typing import Sequence, Tuple

from ...core import BaseProvider


class Provider(BaseProvider):
    """Currencies that actually circulate or are traded in Afghanistan.

    This is deliberately not a world currency table: the locale's own
    currency comes first, followed by those commonly exchanged there.
    """

    #: (code, name, symbol)
    currencies: Sequence[Tuple[str, str, str]] = (
        ("AFN", "Afghan afghani", "؋"),
        ("USD", "United States dollar", "$"),
        ("EUR", "Euro", "€"),
        ("PKR", "Pakistani rupee", "₨"),
        ("IRR", "Iranian rial", "﷼"),
        ("INR", "Indian rupee", "₹"),
        ("AED", "UAE dirham", "د.إ"),
        ("SAR", "Saudi riyal", "﷼"),
        ("TRY", "Turkish lira", "₺"),
        ("CNY", "Chinese yuan", "¥"),
        ("TJS", "Tajikistani somoni", "SM"),
        ("UZS", "Uzbekistani som", "so'm"),
        ("TMT", "Turkmenistani manat", "m"),
        ("GBP", "Pound sterling", "£"),
    )

    #: The locale's own currency, which pricetag() uses.
    local_currency_code = "AFN"
    # The leading digit is `%` (1-9) so amounts never start with a zero.
    price_formats: Sequence[str] = ("%##", "%,###", "%#,###", "%##,###")

    def currency(self) -> Tuple[str, str, str]:
        return self.random_element(self.currencies)

    def currency_code(self) -> str:
        return self.currency()[0]

    def currency_name(self) -> str:
        return self.currency()[1]

    def currency_symbol(self) -> str:
        return self.currency()[2]

    def local_currency(self) -> Tuple[str, str, str]:
        for entry in self.currencies:
            if entry[0] == self.local_currency_code:
                return entry
        return self.currencies[0]

    def pricetag(self) -> str:
        price = self.numerify(self.random_element(self.price_formats))
        return f"{self.local_currency_code} {price}"

    #: (code, name)
    cryptocurrencies: Sequence[Tuple[str, str]] = (
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("USDT", "Tether"),
        ("BNB", "Binance Coin"),
        ("XRP", "Ripple"),
        ("USDC", "USD Coin"),
        ("ADA", "Cardano"),
        ("SOL", "Solana"),
        ("DOGE", "Dogecoin"),
        ("TRX", "TRON"),
    )

    def cryptocurrency(self) -> Tuple[str, str]:
        return self.random_element(self.cryptocurrencies)

    def cryptocurrency_code(self) -> str:
        return self.cryptocurrency()[0]

    def cryptocurrency_name(self) -> str:
        return self.cryptocurrency()[1]
