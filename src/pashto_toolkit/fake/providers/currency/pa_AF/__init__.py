from .. import Provider as CurrencyProvider


class Provider(CurrencyProvider):
    """Currency provider for the Pashto locale (``pa_AF``)."""

    currencies = (
        ("AFN", "افغانۍ", "؋"),
        ("USD", "امریکایي ډالر", "$"),
        ("EUR", "یورو", "€"),
        ("PKR", "پاکستانۍ کلدارې", "₨"),
        ("IRR", "ایرانی ریال", "﷼"),
        ("INR", "هندي روپۍ", "₹"),
        ("AED", "اماراتي درهم", "د.إ"),
        ("SAR", "سعودي ریال", "﷼"),
        ("TRY", "ترکي لیره", "₺"),
        ("CNY", "چینايي یوان", "¥"),
        ("TJS", "تاجکي سامانی", "SM"),
        ("UZS", "ازبکي سوم", "so'm"),
        ("TMT", "ترکمني منات", "m"),
        ("GBP", "برتانوي پونډ", "£"),
    )

    price_formats = ("###", "#,###", "##,###", "###,###")

    def pricetag(self) -> str:
        """Afghan price tags put the afghani sign after the amount."""
        return f"{self.numerify(self.random_element(self.price_formats))} ؋"
