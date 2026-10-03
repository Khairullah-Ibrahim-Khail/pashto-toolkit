from ..en_AF import Provider as EnAfBankProvider


class Provider(EnAfBankProvider):
    """Afghan bank provider in Pashto.

    IBAN/SWIFT/account formats are shared with ``en_AF`` because they are not
    language-dependent; only the bank names are localized.
    """

    banks = (
        "د افغانستان بانک",
        "عزیزي بانک",
        "کابل بانک",
        "میوند بانک",
        "پښتني بانک",
        "افغان یونایټد بانک",
        "لومړنی مایکروفاینانس بانک",
        "سټنډرډ چارټرډ بانک افغانستان",
        "بانک ملي افغان",
        "غضنفر بانک",
        "د افغانستان نړیوال بانک",
        "نیو کابل بانک",
        "اسلامي بانک افغانستان",
    )
