"""World reference data: countries and languages.

Kept small and factual. Country names are in English; the Pashto locale
reports Afghanistan through ``current_country()`` in the address provider.
"""

from typing import List, Sequence, Tuple

from ...core import BaseProvider

#: (English name, alpha-2, alpha-3). Afghanistan and its region first, then
#: the rest of the world in alphabetical order.
COUNTRIES: Tuple[Tuple[str, str, str], ...] = (
    ("Afghanistan", "AF", "AFG"), ("Pakistan", "PK", "PAK"), ("Iran", "IR", "IRN"),
    ("Tajikistan", "TJ", "TJK"), ("Turkmenistan", "TM", "TKM"), ("Uzbekistan", "UZ", "UZB"),
    ("China", "CN", "CHN"), ("India", "IN", "IND"),
    ("Albania", "AL", "ALB"), ("Algeria", "DZ", "DZA"), ("Argentina", "AR", "ARG"),
    ("Armenia", "AM", "ARM"), ("Australia", "AU", "AUS"), ("Austria", "AT", "AUT"),
    ("Azerbaijan", "AZ", "AZE"), ("Bahrain", "BH", "BHR"), ("Bangladesh", "BD", "BGD"),
    ("Belarus", "BY", "BLR"), ("Belgium", "BE", "BEL"), ("Bolivia", "BO", "BOL"),
    ("Bosnia and Herzegovina", "BA", "BIH"), ("Brazil", "BR", "BRA"), ("Bulgaria", "BG", "BGR"),
    ("Cambodia", "KH", "KHM"), ("Cameroon", "CM", "CMR"), ("Canada", "CA", "CAN"),
    ("Chad", "TD", "TCD"), ("Chile", "CL", "CHL"), ("Colombia", "CO", "COL"),
    ("Croatia", "HR", "HRV"), ("Cuba", "CU", "CUB"), ("Cyprus", "CY", "CYP"),
    ("Czechia", "CZ", "CZE"), ("Denmark", "DK", "DNK"), ("Ecuador", "EC", "ECU"),
    ("Egypt", "EG", "EGY"), ("Estonia", "EE", "EST"), ("Ethiopia", "ET", "ETH"),
    ("Finland", "FI", "FIN"), ("France", "FR", "FRA"), ("Georgia", "GE", "GEO"),
    ("Germany", "DE", "DEU"), ("Ghana", "GH", "GHA"), ("Greece", "GR", "GRC"),
    ("Hungary", "HU", "HUN"), ("Iceland", "IS", "ISL"), ("Indonesia", "ID", "IDN"),
    ("Iraq", "IQ", "IRQ"), ("Ireland", "IE", "IRL"), ("Israel", "IL", "ISR"),
    ("Italy", "IT", "ITA"), ("Japan", "JP", "JPN"), ("Jordan", "JO", "JOR"),
    ("Kazakhstan", "KZ", "KAZ"), ("Kenya", "KE", "KEN"), ("Kuwait", "KW", "KWT"),
    ("Kyrgyzstan", "KG", "KGZ"), ("Latvia", "LV", "LVA"), ("Lebanon", "LB", "LBN"),
    ("Libya", "LY", "LBY"), ("Lithuania", "LT", "LTU"), ("Malaysia", "MY", "MYS"),
    ("Maldives", "MV", "MDV"), ("Mali", "ML", "MLI"), ("Mexico", "MX", "MEX"),
    ("Mongolia", "MN", "MNG"), ("Morocco", "MA", "MAR"), ("Myanmar", "MM", "MMR"),
    ("Nepal", "NP", "NPL"), ("Netherlands", "NL", "NLD"), ("New Zealand", "NZ", "NZL"),
    ("Nigeria", "NG", "NGA"), ("North Macedonia", "MK", "MKD"), ("Norway", "NO", "NOR"),
    ("Oman", "OM", "OMN"), ("Peru", "PE", "PER"), ("Philippines", "PH", "PHL"),
    ("Poland", "PL", "POL"), ("Portugal", "PT", "PRT"), ("Qatar", "QA", "QAT"),
    ("Romania", "RO", "ROU"), ("Russia", "RU", "RUS"), ("Saudi Arabia", "SA", "SAU"),
    ("Senegal", "SN", "SEN"), ("Serbia", "RS", "SRB"), ("Singapore", "SG", "SGP"),
    ("Slovakia", "SK", "SVK"), ("Slovenia", "SI", "SVN"), ("Somalia", "SO", "SOM"),
    ("South Africa", "ZA", "ZAF"), ("South Korea", "KR", "KOR"), ("Spain", "ES", "ESP"),
    ("Sri Lanka", "LK", "LKA"), ("Sudan", "SD", "SDN"), ("Sweden", "SE", "SWE"),
    ("Switzerland", "CH", "CHE"), ("Syria", "SY", "SYR"), ("Tanzania", "TZ", "TZA"),
    ("Thailand", "TH", "THA"), ("Tunisia", "TN", "TUN"), ("Turkey", "TR", "TUR"),
    ("Uganda", "UG", "UGA"), ("Ukraine", "UA", "UKR"),
    ("United Arab Emirates", "AE", "ARE"), ("United Kingdom", "GB", "GBR"),
    ("United States", "US", "USA"), ("Uruguay", "UY", "URY"), ("Venezuela", "VE", "VEN"),
    ("Vietnam", "VN", "VNM"), ("Yemen", "YE", "YEM"), ("Zambia", "ZM", "ZMB"),
    ("Zimbabwe", "ZW", "ZWE"),
)

#: (English name, ISO 639-1 code). Afghanistan's own languages first.
LANGUAGES: Tuple[Tuple[str, str], ...] = (
    ("Pashto", "ps"), ("Dari", "fa"), ("Uzbek", "uz"), ("Turkmen", "tk"),
    ("Balochi", "bal"), ("Nuristani", "nur"), ("Pashayi", "psi"),
    ("Arabic", "ar"), ("Bengali", "bn"), ("Chinese", "zh"), ("Dutch", "nl"),
    ("English", "en"), ("French", "fr"), ("German", "de"), ("Hindi", "hi"),
    ("Indonesian", "id"), ("Italian", "it"), ("Japanese", "ja"), ("Kazakh", "kk"),
    ("Korean", "ko"), ("Kurdish", "ku"), ("Malay", "ms"), ("Persian", "fa"),
    ("Polish", "pl"), ("Portuguese", "pt"), ("Punjabi", "pa"), ("Russian", "ru"),
    ("Spanish", "es"), ("Swahili", "sw"), ("Tajik", "tg"), ("Tamil", "ta"),
    ("Thai", "th"), ("Turkish", "tr"), ("Ukrainian", "uk"), ("Urdu", "ur"),
    ("Vietnamese", "vi"),
)

#: Rough land bounding boxes, so location_on_land() never lands at sea.
#: (min latitude, max latitude, min longitude, max longitude, place, country code)
LAND_BOXES: Tuple[Tuple[float, float, float, float, str, str], ...] = (
    (29.4, 38.5, 60.5, 74.9, "Kabul", "AF"),
    (24.0, 36.9, 61.0, 77.0, "Lahore", "PK"),
    (25.1, 39.7, 44.0, 63.3, "Tehran", "IR"),
    (36.7, 41.0, 56.0, 73.1, "Tashkent", "UZ"),
    (8.1, 35.5, 68.2, 89.0, "Delhi", "IN"),
    (36.0, 43.8, 26.0, 44.8, "Ankara", "TR"),
    (16.4, 32.2, 34.5, 55.6, "Riyadh", "SA"),
    (42.0, 55.0, 5.9, 15.0, "Berlin", "DE"),
    (42.3, 51.1, -5.0, 8.2, "Paris", "FR"),
    (36.0, 43.8, -9.3, 3.3, "Madrid", "ES"),
    (50.0, 58.6, -5.7, 1.7, "London", "GB"),
    (25.8, 48.9, -124.6, -67.0, "Chicago", "US"),
    (18.0, 32.7, -117.0, -86.7, "Mexico City", "MX"),
    (-33.7, 5.2, -73.9, -34.8, "Sao Paulo", "BR"),
    (-34.8, -22.1, 16.5, 32.9, "Johannesburg", "ZA"),
    (-3.0, 13.5, 2.7, 14.6, "Lagos", "NG"),
    (18.2, 45.0, 75.0, 123.0, "Beijing", "CN"),
    (31.0, 45.5, 130.0, 145.5, "Tokyo", "JP"),
    (-43.5, -10.7, 113.3, 153.6, "Sydney", "AU"),
    (44.0, 68.0, 30.0, 135.0, "Moscow", "RU"),
)


class Provider(BaseProvider):
    """Country and language values, plus coordinates that fall on land."""

    ALPHA_2 = "alpha-2"
    ALPHA_3 = "alpha-3"

    countries: Sequence[Tuple[str, str, str]] = COUNTRIES
    languages: Sequence[Tuple[str, str]] = LANGUAGES
    land_boxes: Sequence[Tuple[float, float, float, float, str, str]] = LAND_BOXES

    def country(self) -> str:
        return self.random_element(self.countries)[0]

    def country_code(self, representation: str = ALPHA_2) -> str:
        entry = self.random_element(self.countries)
        if representation == self.ALPHA_2:
            return entry[1]
        if representation == self.ALPHA_3:
            return entry[2]
        raise ValueError("representation must be 'alpha-2' or 'alpha-3'")

    def language_name(self) -> str:
        return self.random_element(self.languages)[0]

    def language_code(self) -> str:
        return self.random_element(self.languages)[1]

    def location_on_land(self, coords_only: bool = False) -> List[str]:
        """``[latitude, longitude]``, or with the nearest place and country.

        The point is drawn from a land bounding box, so it is never at sea,
        but it is an approximation rather than a gazetteer lookup.
        """
        min_lat, max_lat, min_lon, max_lon, place, code = self.random_element(self.land_boxes)
        latitude = f"{self.generator.random.uniform(min_lat, max_lat):.5f}"
        longitude = f"{self.generator.random.uniform(min_lon, max_lon):.5f}"
        if coords_only:
            return [latitude, longitude]
        return [latitude, longitude, place, code]
