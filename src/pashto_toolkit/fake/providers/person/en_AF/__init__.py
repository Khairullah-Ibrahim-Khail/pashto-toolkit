import re

from .. import Provider as PersonProvider

"""
Afghanistan locale in English transliteration (en_AF)

This package provides Afghan Pashto and Tajik personal names written in English
transliteration, including support for male and female first names, last names,
prefixes, and suffixes.
"""


class Provider(PersonProvider):
    prefixes_male = ['Mir', 'Sardar', 'Malik', 'Khan', 'Haji', 'Mullah', 'Ustad', 'Mawlawi', 'Sheikh', 'Amir',
                     'Sultan', 'Shah', 'Padshah', 'Wazir', 'Mufti', 'Qazi', 'Hafiz', 'Maulvi', 'Al-Haj', 'Sayyid',
                     'Mirza', 'Baba', 'Pir', 'Ghazi', 'Sahib', 'Agha']
    prefixes_female = [
        "Peghla",  # Miss (used for unmarried young women)
        "Mairman",  # Mrs./Madam (formal title for a married or adult woman)
        "Aghele",  # Formal prefix equivalent to 'Lady' or 'Madam'
        "Bibi",  # Respectful title for older women or maternal figures
        "Tror",  # 'Aunt' (maternal or paternal); used respectfully for older women
        "Nia",  # 'Grandmother'; used as an honorific for elderly women
        "Khor",  # 'Sister'; a common respectful way to address a peer
        "Mor",  # 'Mother'; used to address senior women with high respect
        "Muhtarama"  # 'Respected' (feminine form); used in highly formal contexts
    ]

    suffixes = [
        "zai", "khel", "wal", "dost", "ullah", "uddin",
        "bakhsh", "yar", "jan", "dad", "pur", "zada",
        "i", "ian", "far", "niaz", "mand", "baz",
        "war", "dil", "gul", "noor", "bahar", "shah",
        "khan", "malik", "sardar", "wazir", "amir",
    ]

    pashto_male_first_names = [
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
        "Aminullah", "Abasin", "Ahmed", "Ali", "Alam", "Alamzeb",
        "Amail", "Amu", "Andam", "Angar", "Armaghan", "Arman",
        "Arsalan", "Aryan", "Asfand", "Asfandyar", "Atal", "Atsak",
        "Aurang", "Awalmir", "Azlan", "Azmaray", "Babak", "Babrak",
        "Bacha", "Badam", "Bahramand", "Bahrawar", "Bakht", "Bakht Rawan",
        "Bakht Awar", "Balach", "Balay", "Barlas", "Baryal", "Baseer",
        "Batoor", "Bazgar", "Bazir", "Behroz", "Beltoon", "Beroj",
        "Chargul", "Dagar", "Darab", "Darman", "Darwesh", "Daryab",
        "Daulat", "Dawar", "Diar", "Droon", "Elam", "Farhang",
        "Farihund", "Gahez", "Gedi", "Ghairat", "Ghakhtalay", "Ghalji",
        "Ghamay", "Gharsanay", "Ghatool", "Ghazan", "Ghazin", "Ghorzang",
        "Ghunchagul", "Ghurghusht", "Gogal", "Gorbat", "Grant", "Gul Baz",
        "Gul Jan", "Gul Mast", "Gul Rang", "Gul Yar", "Gul Zaman", "Gulab",
        "Hask", "Helmand", "Hewand", "Hukam", "Izat", "Janan",
        "Janat Gul", "Jandol", "Kakay'", "Karlani", "Karmal", "Karwan",
        "Khagalay", "Khaista", "Khak", "Khalo", "Khandawar", "Khialay",
        "Khog", "Khushal", "Khushdil", "Khwazun", "Khyber", "Kochai",
        "Kushan", "Lajbar", "Lashkar", "Lawang", "Lawangin", "Lmar",
        "Liwal", "Mairanay", "Maiwand", "Malang", "Malook", "Malyar",
        "Manan", "Mangal", "Marghoz", "Marjan", "Marwand", "Mashal",
        "Mateen", "Mehtar", "Minatbar", "Mirwais", "Mirzal", "Mohambar",
        "Muhammad", "Nang", "Nangial", "Noomyalay", "Nufail", "Olas",
        "Olasyar", "Pamir", "Pashtoon", "Pason", "Pasoon", "Patang",
        "Patman", "Patwal", "Patyal", "Paywastun", "Pelabo", "Perzo",
        "Pohand", "Pordal", "Powneda", "Psarlay", "Qajeer Gul", "Qalandar",
        "Rahamdil", "Rangeen", "Reday", "Reshteen", "Roshan", "Rustam",
        "Sabawoon", "Sadin", "Sahar", "Sahar Gul", "Sahim", "Saifur",
        "Salar", "Samandar", "Samoon", "Samsor", "Sangin", "Sangrez",
        "Sanobar", "Sarban", "Sarbaz", "Sardar", "Sartor", "Sayel",
        "Selab", "Selani", "Shahsawar", "Shahzar", "Shamal", "Shamshad",
        "Sher", "Sherdil", "Sherin", "Shin Gul", "Shindi Gul", "Shino",
        "Shpol", "Shpoon", "Shuja", "Sibghatullah", "Sifat", "Sikandar",
        "Sohrab", "Sparlay", "Spetselay", "Spin Gul", "Spinzar", "Storay",
        "Sur Gul", "Suweil", "Syal", "Taban", "Tanim", "Taroon",
        "Tawas", "Teri", "Tofan", "Tolwak", "Tor Gul", "Toryal",
        "Toti", "Turan", "Turialai", "Wadaan", "Wakdar", "Wakman",
        "Yama", "Yaqut", "Yoon", "Zafran", "Zalaan", "Zaland",
        "Zalmay", "Zapran", "Zar Gul", "Zarwali", "Zarak", "Zaram",
        "Zarang", "Zarbat", "Zardab", "Zargar", "Zarghun", "Zarhawar",
        "Zarhgay", "Zarin", "Zarkanay", "Zarlesh", "Zarmast", "Zarnosh",
        "Zaryab", "Zawaar", "Zawar", "Zgard", "Ziar", "Ziarmal",
        "Zigar", "Zmaray", "Zorak", "Zorawar", "Zwak", "Zwandun",
        "Afia", "Aghala", "Ambrin", "Angeza", "Anar", "Ara",
        "Apana", "Aryana", "Badrai", "Bakht Awara", "Bala Nashta", "Balbala",
        "Banafsha", "Barsala", "Bazira", "Benazira", "Bibi", "Bibi Rokhana",
        "Brekhna", "Diwa", "Durkhanai", "Farishta", "Gabina", "Galai",
        "Ghatola", "Ghorashka", "Ghotai", "Ghuncha", "Gorgora", "Grana",
        "Gul Bano", "Gul Ghotai", "Gul Lakhta", "Gul Makai", "Gul Mina", "Gul Panrha",
        "Gul Sangha", "Gul Warin", "Gulalai", "Gulchin", "Gulnar", "Hala",
        "Helai", "Hila", "Hina", "Husay", "Kashmala", "Khaperai",
        "Kharo", "Khatol", "Khkulay", "Khush Bakhta", "Khwaga", "Kontara",
        "Laila", "Lailuma", "Lakhta", "Lalma", "Lalzari", "Lamba",
        "Lawanga", "Lema", "Mahjabin", "Mahnur", "Mahzala", "Malalai",
        "Malghalara", "Mina", "Mukai", "Munawara", "Murchakai", "Muska",
        "Naghma", "Nangialai", "Narenja", "Natkai", "Nawyata", "Nazanina",
        "Nazdana", "Nazo", "Niazmina", "Orbakhta", "Orbala", "Orzala",
        "Palwasha", "Panra", "Parghunda", "Pariwash", "Parkha", "Pashmina",
        "Patasa", "Peghra", "Perkha", "Pokha", "Ranrha", "Rayan",
        "Rekhmina", "Reshtina", "Roshina", "Saba", "Salgay", "Sandara",
        "Sanga", "Sangina", "Selai", "Senzela", "Shahgalay", "Shahay",
        "Shahlalai", "Shamla", "Shandana", "Shanzai", "Shaperai", "Shastai",
        "Shazmina", "Shinkai", "Shinogai", "Shughla", "Spalmay", "Sparghai",
        "Spezala", "Spozmai", "Storai", "Tabana", "Talwasa", "Tanima",
        "Tor Pikai", "Ugay", "Wadaana", "Wagma", "Wahida", "Wajia",
        "Warda", "Wawrina", "Wranga", "Wreshmin", "Zainba", "Zaituna",
        "Zakia", "Zala", "Zalanda", "Zaloba", "Zamba", "Zar Bibi",
        "Zar Masta", "Zar Mina", "Zar Wareen", "Zarbaha", "Zareena", "Zareesh",
        "Zarghuna", "Zarka", "Zar Lakhta", "Zar Sanga", "Zarshala", "Zartaj",
        "Zhala", "Zhalai", "Zohal", "Zufash",
    ]

    pashto_female_first_names = [
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
        "Wajdan", "Zareen", "Amina", "Afia", "Badrai", "Diwa",
        "Farishta", "Gabina", "Hala", "Mahjabin", "Orbakhta", "Ranrha",
        "Tabana", "Ugay", "Wadaana", "Zainba",
    ]

    tajik_male_first_names = [
        "Farhad", "Rustam", "Babur", "Jamshid", "Kawoon", "Sohrab",
        "Bahram", "Khosrow", "Nadir", "Yama", "Abdul", "Ali",
        "Hassan", "Hussein", "Jafar", "Mahdi", "Mustafa", "Reza",
        "Said", "Yasin", "Farid", "Hafiz", "Iqbal", "Jalal",
        "Khalil", "Latif", "Nazar", "Qasim", "Rahim", "Samir",
        "Ahmad", "Bashir", "Davlat", "Ehsan", "Fahim", "Ghaffar",
        "Habib", "Iskandar", "Jamshed", "Kamran", "Lutfullah", "Mansur",
        "Nemat", "Omid", "Parviz", "Qodir", "Rahmat", "Safar",
        "Taj", "Umar", "Vohid", "Wahid", "Yaqub", "Zafar",
        "Anwar", "Bakhtiar", "Daler", "Eraj", "Firuz", "Gul",
        "Hamza", "Iraj", "Jawid", "Karam", "Lutf", "Matin",
        "Nur", "Otabek", "Payam", "Qais", "Rashid", "Tahir",
        "Umed", "Vali", "Wasi", "Yusuf", "Zubair", "Aslam",
        "Bismillah", "Daud", "Emon", "Fayz", "Ghiyas", "Hadi",
        "Ismoil", "Javohir", "Khalid", "Lal", "Muhsin", "Nasim",
        "Obid", "Parwaiz", "Qurban", "Rauf", "Sabur", "Tawhid",
        "Ubayd", "Vafo", "Wajid", "Yahyo", "Zayn", "Abror",
        "Bahrom", "Davron", "Elyor", "Farkhod", "Gulom", "Hikmat",
        "Ilhom", "Jahongir", "Khurshed", "Loik", "Murod", "Nizom",
        "Olim", "Pardaev", "Qobil", "Ravshan", "Tojiddin", "Ulugbek",
        "Vosil", "Wahdat", "Yorqin", "Alisher", "Bekzod", "Dilshod",
        "Eshon", "Firdavs", "Gulbahor", "Hoshim", "Ibrohim", "Jalol",
        "Komron", "Laziz", "Mirzo", "Nozim", "Qahhor", "Sardor",
        "Temur", "Uchqun", "Vahob", "Wahob", "Yodgor", "Ziyo",
        "Akmal", "Bobur", "Doston", "Erkin", "Fayoz", "Gulnazar",
        "Husan", "Isfandiyor", "Javlon", "Kamol", "Lutfi", "Muhammad",
        "Nurali", "Pahlavon", "Siroj", "Tolib", "Umid", "Vahid",
        "Yigitali", "Abdullo", "Bahodir", "Eshmurod", "Hamid", "Ixtiyor",
        "Khayot", "Olimjon", "Tohir", "Umidjon", "Akbar", "Bobojon",
        "Fayzullo",
    ]

    tajik_female_first_names = [
        "Farzana", "Shabnam", "Nahid", "Parwin", "Roxana", "Scheherazade",
        "Gohar", "Laleh", "Mahnaz", "Niloofar", "Masooma", "Nafisa",
        "Rahima", "Sakina", "Zainab", "Mursal", "Fahima", "Habiba",
        "Khadija", "Laila", "Maryam", "Nadia", "Razia", "Saida",
        "Yasmin", "Aisha", "Bibi", "Dilafruz", "Eram", "Farahnaz",
        "Gul", "Hadiya", "Iram", "Jahanara", "Khalida", "Lalzari",
        "Nabila", "Ozra", "Parwana", "Qamar", "Rahila", "Sahar",
        "Tabasum", "Uzma", "Vida", "Wahida", "Yalda", "Afsana",
        "Bakht", "Chaman", "Durdana", "Fauzia", "Gulshan", "Hawa",
        "Iffat", "Jamilah", "Kalsoom", "Najiba", "Omarah", "Palwasha",
        "Qubra", "Tahira", "Urooj", "Wajma", "Yasira", "Zarqa",
        "Aqila", "Bushra", "Chinar", "Dilruba", "Eshal", "Faryal",
        "Gulnar", "Hena", "Inayat", "Jawhara", "Kawish", "Lamar",
        "Munira", "Nasreen", "Omaid", "Parisa", "Qudsia", "Sadaf",
        "Taslima", "Umaira", "Vasila", "Wazira", "Yumna", "Zeba",
        "Anisa", "Bahar", "Cheen", "Darya", "Elham", "Farkhunda",
        "Gulrukh", "Hira", "Iqra", "Joya", "Kiran", "Lailuma",
        "Mahro", "Nazia", "Orana", "Pari", "Qirat", "Rahmat",
        "Saima", "Tahera", "Warsa", "Yasamin", "Zulekha", "Arooj",
        "Bano", "Chamanara", "Dilshad", "Eman", "Gulbanu", "Huma",
        "Jannat", "Kashmala", "Laili", "Mahwish", "Nargis", "Omaima",
        "Paiman", "Qamaria", "Roshna", "Sughra", "Tara", "Ulfat",
        "Yasmeen", "Zara", "Aalia", "Dilbar", "Ema", "Gulbahar",
        "Hina", "Javeria", "Mahira", "Naseem", "Omaidah", "Parizad",
        "Rukhsana", "Saba", "Tasneem", "Uroosa", "Vasima", "Wajdan",
        "Zareen", "Amina",
    ]

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
        "Matin", "Sami", "Herati", "Kabuli", "Mazar", "Nangarhari",
        "Panjshiri", "Samarqandi", "Wardaki", "Badakhshi", "Dari", "Farsi",
        "Ghazni", "Hazarajat", "Istalif", "Jowzjan", "Kunar", "Logar",
        "Maimana", "Nimruz", "Oruzgan", "Parwan", "Qandahar", "Rostaq",
        "Sarobi", "Takhar", "Uruzgan", "Waras", "Yawan", "Zaranj",
        "Alavi", "Bahrami", "Davlat", "Emami", "Farahi", "Gulistani",
        "Hashemi", "Jafari", "Kazemi", "Lahori", "Mahdavi", "Nasiri",
        "Omidi", "Parvizi", "Qasemi", "Rahimi", "Sadeghi", "Tavakoli",
        "Vahidi", "Wahidi", "Yazdani", "Zamani", "Abidi", "Barani",
        "Danesh", "Esfahani", "Gharibi", "Hosseini", "Izadi", "Jalali",
        "Kermani", "Lashgari", "Mashhadi", "Nadiri", "Omidvar", "Pour",
        "Qobadi", "Rashidi", "Shirazi", "Tabrizi", "Vahedi", "Wahdat",
        "Yaghoubi", "Zahedi", "Abbasi", "Bonyadi", "Chitsaz", "Dehqani",
        "Eftekhari", "Fouladi", "Gorgani", "Hamidi", "Isfandiyari", "Javan",
        "Lari", "Mojaddedi", "Nabawi", "Ostadi", "Pahlavan", "Qazvini",
        "Ranjbar", "Saberi", "Tehrani", "Vaziri", "Waseqi", "Yasini",
        "Zand", "Ashna", "Bahar", "Choubineh", "Daryaee", "Farrokh",
        "Golestani", "Iraj", "Javanmard", "Khorasani", "Lavasan", "Mirdamadi",
        "Nouri", "Ostad", "Pirzadeh", "Qomi", "Rostami", "Safavi",
        "Tousi", "Vafaei", "Wahhabi", "Yousefi", "Zarrabi", "Abrishami",
        "Bakhtiari", "Chamran", "Dolatabadi", "Eshghi", "Faramarzi", "Goudarzi",
        "Hamedani", "Imani", "Kashani", "Lahijani", "Mofidi", "Nazari",
        "Olia", "Pishva", "Qashqai", "Safari", "Taba", "Vahdati",
        "Yazdi", "Zarif", "Amini", "Bozorg", "Cheraghi", "Darvish",
        "Eskandari", "Fars", "Ghasemi", "Hekmat", "Ishraqi", "Javid",
        "Khalaj", "Moghadam", "Nazemi", "Oveisi", "Pouya", "Qahraman",
        "Rashid", "Sajjadi", "Tajik", "Wafai", "Yaghouti", "Zakeri",
        "Akbari", "Bijan", "Chooka", "Daneshvar", "Eshraghi", "Fazeli",
        "Gilan", "Haghighi", "Irani", "Jalili", "Khomeini", "Lotfi",
        "Moshiri", "Nadimi", "Parsi", "Qavami", "Salami", "Tavassoli",
        "Wafadar", "Yazdan", "Zarghami", "Ardabili", "Deilami", "Farahani",
        "Hosseinzadeh", "Jahanbin", "Mansouri", "Pahlavi", "Rahnavard", "Sadegh",
        "Tabatabaei", "Bani", "Esfandiari", "Gholami",
    ]

    # ================ Email section =====================
    domains = [
        "gmail.com", "yahoo.com", "outlook.com", "afghanmail.com", "mail.com"
    ]

    def _slug_name(self, name):
        """``"Tahir Dawlatzai"`` -> ``"tahir.dawlatzai"``, or ``""``.

        Returns empty when the name has no Latin letters to work from, which
        is the case for a name in Pashto script.
        """
        if not name:
            return ""
        parts = [self._slug(part) for part in str(name).split()]
        parts = [p for p in parts if len(p) >= 2]
        if not parts:
            return ""
        return ".".join(parts[:2]) if len(parts) > 1 else parts[0]

    @staticmethod
    def _slug(value: str) -> str:
        """Strip a name down to the characters an address may contain.

        Several names are two words ("Bakht Awar"), which previously left a
        space inside the generated email address.
        """
        return re.sub(r"[^a-z0-9]+", "", value.lower())

    def username(self, gender=None, name=None):
        """Afghan-style username.

        ``name`` ties the username to a person already generated, so a record
        can be internally consistent: "Tahir Dawlatzai" gives
        ``tahir.dawlatzai42``. ``en_AF`` names are Latin, so this always works.
        """
        from_name = self._slug_name(name)
        if from_name:
            return f"{from_name}{self.generator.random.randint(1, 999)}"

        if gender == "female":
            first = self._slug(self.generator.random.choice(self.pashto_female_first_names))
        elif gender == "male":
            first = self._slug(self.generator.random.choice(self.pashto_male_first_names))
        else:
            pool = self.pashto_male_first_names + self.pashto_female_first_names
            first = self._slug(self.generator.random.choice(pool))

        last = self._slug(self.generator.random.choice(self.last_names))
        number = str(self.generator.random.randint(1, 999))
        return f"{first}.{last}{number}"

    def user_name(self, gender=None, name=None):
        """Standard formatter name for :meth:`username`."""
        return self.username(gender, name)

    def email(self, gender=None, name=None):
        """Full email address. ``name`` ties it to a person already made."""
        return f"{self.username(gender, name)}@{self.generator.random.choice(self.domains)}"

    # =================End of the email section ==============

    # ---------- BASIC PARTS ----------

    def first_name_male(self):
        return self.generator.random.choice(self.pashto_male_first_names + self.tajik_male_first_names)

    def first_name_female(self):
        return self.generator.random.choice(self.pashto_female_first_names + self.tajik_female_first_names)

    def last_name(self):
        return self.generator.random.choice(self.last_names)

    def first_name(self):
        return self.generator.random.choice([self.first_name_male(), self.first_name_female()])

    # ---------- FULL NAME ----------

    #: Share of generated full names that carry an honorific.
    honorific_probability = 0.25

    def name(self):
        if self.generator.random.random() < 0.5:
            first, prefixes = self.first_name_male(), self.prefixes_male
        else:
            first, prefixes = self.first_name_female(), self.prefixes_female

        parts = []
        # Several words are both a title and a given name, so a name whose
        # given name is already a title must not take another one in front,
        # or it comes out as "بی بی بی بی ..." / "Agha Wazir ...".
        if self.generator.random.random() < self.honorific_probability and not self._is_honorific(first):
            parts.append(self.generator.random.choice(prefixes))
        parts += [first, self.last_name()]
        return " ".join(parts)

    def _is_honorific(self, name):
        """True when ``name`` is, or begins with, one of this locale's titles.

        Some given names are themselves two words beginning with a title,
        such as "Bibi Rokhana", so the first token is checked as well.
        """
        titles = set(self.prefixes_male) | set(self.prefixes_female)
        return name in titles or name.split()[0] in titles

    def name_male(self):
        return f"{self.first_name_male()} {self.last_name()}"

    def name_female(self):
        return f"{self.first_name_female()} {self.last_name()}"
