from .. import Provider as CurrencyProvider


class Provider(CurrencyProvider):
    """Currency provider for English Afghanistan locale (en_AF)."""

    # The leading digit is `%` (1-9); `#` would allow "AFN 012,228".
    price_formats = ["%##,###", "%,###,###", "%#,###,###", "%##,###,###"]

    def pricetag(self) -> str:
        price = self.numerify(self.random_element(self.price_formats))
        return f"AFN {price}"
