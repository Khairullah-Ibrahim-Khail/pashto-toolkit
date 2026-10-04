from datetime import date, timedelta
from typing import Optional, Tuple

from ....types import SexLiteral
from .. import Provider as PassportProvider


class Provider(PassportProvider):
    """Implement passport provider for ``en_AF`` locale in English."""

    # Afghan passport number formats
    passport_number_formats = (
        "A########",  # alphanumeric starting with A
        "P########",  # alphanumeric starting with P
        "########",  # numeric only
        "###-######",  # formatted with dash
    )

    # Afghan first names in English transliteration
    first_names = {
        "M": [
            "Ahmad", "Mohammad", "Abdullah", "Noorullah", "Khalid", "Rahim",
            "Farid", "Nasir", "Jamal", "Tariq", "Wali", "Yusuf",
            "Zahir", "Bashir", "Daoud", "Faisal", "Gul", "Hamid",
            "Ismail", "Javed", "Karim", "Latif", "Massoud", "Noor",
            "Omar", "Qadir", "Rashid", "Safi", "Talib", "Wahid",
            "Baryalai", "Spin", "Tor", "Zmarak", "Khostai", "Wazir",
            "Miran", "Sangar", "Shinwari", "Ghilzai", "Amanullah", "Aziz",
            "Dawood", "Ehsan", "Fahim", "Ghulam", "Habib", "Ibrahim",
            "Jalal", "Kabeer", "Lutfullah", "Mansoor", "Naim", "Obaid",
            "Pacha", "Qais", "Rahmat", "Sattar", "Tawab", "Umar",
            "Valli", "Wais", "Yaqub", "Zabi", "Abdul", "Ataullah",
            "Bismillah", "Chaman", "Dastagir", "Ezat", "Farooz", "Ghaus",
            "Hafiz", "Inayat", "Jahan", "Khalil", "Lal", "Matin",
            "Nazar", "Pir", "Qurban", "Sami", "Tahir", "Ubaid",
            "Vakil", "Yar", "Zaman", "Amin", "Baz", "Chinar",
            "Dilawar", "Ehsanullah", "Fazal", "Gulzar", "Haji", "Ilyas",
            "Juma", "Khal", "Lala", "Mullah", "Nek", "Omid",
            "Qader", "Rahman", "Sadiq", "Ustad", "Vafadar", "Younis",
            "Zubair", "Aashiq", "Badar", "Chiragh", "Darya", "Eid",
            "Faiz", "Gohar", "Hakim", "Iqbal", "Jamil", "Khan",
            "Liaqat", "Momin", "Nawab", "Obaidullah", "Paiman", "Qasim",
            "Rafiq", "Sahib", "Taj", "Usman", "Vakel", "Watan",
            "Yaftali", "Zardad", "Asad", "Bahram", "Dost", "Ebad",
            "Fateh", "Ghausuddin", "Hidayat", "Ishaq", "Jawad", "Kamal",
            "Lutf", "Nur", "Parwiz", "Qudrat", "Rahimullah", "Sabir",
            "Tawfiq", "Vedat", "Wahab", "Yahya", "Zalmai", "Aimal",
            "Babar", "Dil", "Emal", "Farhad", "Gulbuddin", "Irfan",
            "Jahangir", "Rahmatullah", "Sahil", "Ubaidullah", "Vasef", "Waliullah",
            "Zaki", "Arif", "Bilal", "Chamanullah", "Daud", "Fazlullah",
            "Jamshed", "Khalilullah", "Latifullah", "Nazir", "Samiullah", "Tajuddin",
            "Waris", "Yasin", "Zabih", "Aslam", "Hafizullah", "Inayatullah",
            "Aminullah",
        ],
        "F": [
            "Mariam", "Fatima", "Zahra", "Laila", "Nadia", "Sabrina",
            "Soraya", "Parwin", "Shukria", "Fereshta", "Hadia", "Jamila",
            "Kamila", "Nargis", "Razia", "Safia", "Tamanna", "Wajiha",
            "Yasmin", "Zarmina", "Gulalai", "Mairman", "SpinGul", "Torpekai",
            "Wazhma", "Shamsia", "Naghma", "Mishal", "Sanga", "Zarghuna",
            "Aisha", "Bibi", "Chaman", "Dilafroz", "Emaan", "Farahnaz",
            "Gul", "Hadiya", "Iram", "Jahanara", "Khadija", "Lalzari",
            "Mahnaz", "Nabila", "Ozra", "Parwana", "Qamar", "Rahila",
            "Sahar", "Tabasum", "Uzma", "Vida", "Wahida", "Yalda",
            "Zainab", "Afsana", "Bakht", "Durdana", "Eram", "Fauzia",
            "Gulshan", "Hawa", "Iffat", "Jamilah", "Kalsoom", "Masooma",
            "Najiba", "Omarah", "Palwasha", "Qubra", "Rahima", "Sakina",
            "Tahira", "Urooj", "Wajma", "Yasira", "Zarqa", "Aqila",
            "Bushra", "Chinar", "Dilruba", "Eshal", "Faryal", "Gulnar",
            "Hena", "Inayat", "Jawhara", "Kawish", "Lamar", "Munira",
            "Nasreen", "Omaid", "Parisa", "Qudsia", "Sadaf", "Taslima",
            "Umaira", "Vasila", "Wazira", "Yumna", "Zeba", "Anisa",
            "Bahar", "Cheen", "Darya", "Elham", "Farkhunda", "Gulrukh",
            "Hira", "Iqra", "Joya", "Kiran", "Lailuma", "Mahro",
            "Nazia", "Orana", "Pari", "Qirat", "Rahmat", "Saima",
            "Tahera", "Warsa", "Yasamin", "Zulekha", "Arooj", "Bano",
            "Chamanara", "Dilshad", "Eman", "Farzana", "Gulbanu", "Huma",
            "Jannat", "Kashmala", "Laili", "Mahwish", "Omaima", "Paiman",
            "Qamaria", "Roshna", "Sughra", "Tara", "Ulfat", "Yasmeen",
            "Zara", "Aalia", "Dilbar", "Ema", "Fahima", "Gulbahar",
            "Hina", "Javeria", "Khalida", "Mahira", "Naseem", "Omaidah",
            "Parizad", "Rukhsana", "Saba", "Tasneem", "Uroosa", "Vasima",
            "Wajdan", "Zareen", "Amina",
        ]
    }

    # Afghan last names in English transliteration
    last_names = [
        "Khan", "Ahmadzai", "Mohammadi", "Karimi", "Hussaini", "Rahmani",
        "Sadiqi", "Yousafzai", "Popal", "Ghilzai", "Durrani", "Barakzai",
        "Noori", "Alkozai", "Stanikzai", "Zazai", "Wardak", "Kharoti",
        "Hotak", "Taraki", "Ahmadi", "Alami", "Balkhi", "Danish",
        "Ebrahimi", "Faruqi", "Ghani", "Hakimi", "Ibrahimi", "Jami",
        "Arsalai", "Atmar", "Azizi", "Bakhtari", "Charkhi", "Dost",
        "Ehsas", "Faqiri", "Gul", "Haidari", "Ismail", "Jabarkhel",
        "Kakar", "Lodin", "Mangal", "Niazi", "Omar", "Paktin",
        "Qaderi", "Rasuli", "Safi", "Tani", "Umar", "Wafa",
        "Yaftali", "Zadran", "Achakzai", "Babrakzai", "Chamkani", "Dawlatzai",
        "Esmat", "Fahim", "Ghafor", "Habibi", "Ishaqzai", "Jalalzai",
        "Kandahari", "Lakanwal", "Mahmood", "Nazar", "Obaidullah", "Parwani",
        "Qaisrani", "Rohani", "Sangin", "Tarakai", "Usmani", "Waziri",
        "Yaqubi", "Zabuli", "Afridi", "Bangash", "Chitrali", "Daudzai",
        "Eid", "Farooz", "Ghalib", "Hassanzai", "Ibrahimkhel", "Jalalabad",
        "Khattak", "Lashkari", "Marwat", "Nangarhar", "Orakzai", "Peshawari",
        "Qandahari", "Rahim", "Shinwari", "Turi", "Uthmanzai", "Wazir",
        "Yousuf", "Zakhil", "Amin", "Babar", "Chaman", "Dawood",
        "Eidgah", "Farooq", "Ghaznavi", "Habibullah", "Ilyas", "Jamal",
        "Khalil", "Latif", "Miran", "Nek", "Obaid", "Pacha",
        "Qais", "Rahimullah", "Sahib", "Taj", "Ubaid", "Vakil",
        "Wali", "Yar", "Zaman", "Aminullah", "Baz", "Chinar",
        "Dilawar", "Ehsanullah", "Fazal", "Gulzar", "Haji", "Juma",
        "Khal", "Lala", "Mullah", "Omid", "Qader", "Rahman",
        "Sadiq", "Talib", "Ustad", "Vafadar", "Younis", "Zubair",
        "Aashiq", "Badar", "Chiragh", "Darya", "Faiz", "Gohar",
        "Hakim", "Iqbal", "Jamil", "Liaqat", "Momin", "Nawab",
        "Paiman", "Qasim", "Rafiq", "Usman", "Vakel", "Watan",
        "Zardad", "Asad", "Bahram", "Ebad", "Fateh", "Ghausuddin",
        "Hidayat", "Ishaq", "Jawad", "Kamal", "Lutf", "Nur",
        "Parwiz", "Qudrat", "Sabir", "Tawfiq", "Vedat", "Wahab",
        "Yahya", "Zalmai", "Aimal", "Dil", "Emal", "Farhad",
        "Gulbuddin", "Irfan", "Jahangir", "Khalid", "Lal", "Rahmatullah",
        "Sahil", "Tahir", "Ubaidullah", "Vasef", "Waliullah", "Zaki",
        "Arif", "Bilal", "Chamanullah", "Daud", "Ehsan", "Fazlullah",
        "Ibrahim", "Jamshed", "Khalilullah", "Latifullah", "Nazir", "Pir",
        "Qurban", "Samiullah", "Tajuddin", "Waris", "Yasin", "Zabih",
        "Aslam", "Bismillah", "Ghaus", "Hafizullah", "Inayatullah", "Jahan",
        "Matin", "Sami",
    ]

    def passport_owner(self, gender: SexLiteral = "M") -> Tuple[str, str]:
        first_name = self.generator.random.choice(self.first_names.get(gender, self.first_names["M"]))
        last_name = self.generator.random.choice(self.last_names)
        return first_name, last_name

    def passport_dates(self, birthday: Optional[date] = None) -> Tuple[date, date]:
        """Generate issue and expiry dates for an Afghan passport.

        ``birthday`` defaults to today. It is resolved per call rather than in
        the signature, where it would be frozen at import time.
        """
        today = date.today()
        if birthday is None:
            birthday = today
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

        if age < 5:
            expiry_years = 5
            issue_date = self.generator.date_between_dates(birthday, today)
        elif age < 16:
            expiry_years = 5
            min_issue = birthday + timedelta(days=5 * 365)
            issue_date = self.generator.date_between_dates(min_issue, today)
        elif age >= 26:
            expiry_years = 10
            min_issue = today - timedelta(days=expiry_years * 365)
            issue_date = self.generator.date_between_dates(min_issue, today)
        else:
            expiry_years = 26 - age
            min_issue = birthday + timedelta(days=16 * 365)
            issue_date = self.generator.date_between_dates(min_issue, today)

        expiry_date = issue_date.replace(year=issue_date.year + expiry_years)

        # Adjust Feb 29 for non-leap years
        if issue_date.month == 2 and issue_date.day == 29:
            if not self._is_leap_year(expiry_date.year):
                expiry_date = expiry_date.replace(day=28)

        return issue_date, expiry_date

    def _is_leap_year(self, year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def passport_gender(self, seed: int = 0) -> SexLiteral:
        if seed != 0:
            self.generator.random.seed(seed)
        genders: list[SexLiteral] = ["M", "F", "X"]
        return self.generator.random.choices(genders, weights=[0.493, 0.493, 0.014], k=1)[0]
