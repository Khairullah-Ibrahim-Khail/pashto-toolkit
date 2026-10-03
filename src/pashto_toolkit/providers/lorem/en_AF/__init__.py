from faker.providers.lorem.en_US import Provider as EnUsLoremProvider


class Provider(EnUsLoremProvider):
    """Lorem provider for Afghanistan (``en_AF``).

    ``en_AF`` is the English-transliteration locale, so prose stays English and
    reuses Faker's ``en_US`` corpus. The Pashto word list lives in ``pa_AF``.
    """
