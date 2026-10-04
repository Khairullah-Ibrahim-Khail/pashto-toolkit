"""Afghanistan Pashto locale (``pa_AF``).

Personal names in Pashto script: male and female given names, family names,
honorifics, plus Latin-transliterated pools used to build usernames and email
addresses.
"""

import re

from .. import Provider as PersonProvider


class Provider(PersonProvider):
    # ------------------------ PREFIXES ------------------------
    # Pashto honorifics / titles for male and female names
    # د نارینه او ښځینه نومونو لپاره پښتو لقبونه / احترامتي ټکي

    prefixes_male = [
        "مولوي", "الحاج", "قاري", "سردار", "خان",
        "حاجي", "ملا", "استاد", "امیر", "سید", "ملک",
    ]

    # Pashto family-name endings, used by suffix(). Written separately here;
    # in a full name they are normally joined to the stem.
    suffixes = [
        "زی", "خېل", "وال", "زاده", "مل", "یار", "ګل", "الدین",
    ]

    prefixes_female = [
        "آغلې", "محترمه", "بی بی", "میرمنه",
        "ډاکټرې", "محترمه بي بي",
    ]

    pashto_male_first_names = [
        "احمد", "محمد", "عبدالله", "نورالله", "خالد", "رحیم",
        "فرید", "ناصر", "جمال", "طارق", "ولي", "یوسف",
        "ظاهر", "بشیر", "داود", "فیصل", "ګل", "حمید",
        "اسماعیل", "جاوید", "کریم", "لطیف", "مسعود", "نور",
        "عمر", "قادر", "رشید", "صافی", "طالب", "واحد",
        "بریالی", "سپین", "تور", "زمرد", "خوستی", "وزیر",
        "میران", "سنجر", "شینواری", "غلجی", "امان الله", "عزیز",
        "داوود", "احسان", "فهیم", "غلام", "حبیب", "ابراهیم",
        "جلال", "کبیر", "لطف الله", "منصور", "نعیم", "عبید",
        "پاچا", "قیس", "رحمت", "ستار", "تواب", "ویس",
        "یعقوب", "ذبی", "عبدال", "عطاالله", "بسم الله", "چمن",
        "دستګیر", "عزت", "فروز", "غوث", "حافظ", "عنایت",
        "جهان", "خلیل", "لال", "متین", "نظر", "پیر",
        "قربان", "سامی", "طاهر", "وکیل", "یار", "زمان",
        "امین", "باز", "چنار", "دلور", "احسان الله", "فضل",
        "ګلزار", "حاجی", "الیاس", "جمعه", "خال", "لاله",
        "ملا", "نیک", "امید", "رحمن", "صادق", "وفادار",
        "یونس", "زبیر", "عاشق", "بدر", "چراغ", "دریا",
        "عید", "فیض", "ګوهر", "حکیم", "اقبال", "جمیل",
        "خان", "لیاقت", "مؤمن", "نواب", "عبیدالله", "پیمان",
        "قاسم", "رفیق", "صاحب", "تاج", "عثمان", "وطن",
        "یفتلی", "زرداد", "اسد", "بهرام", "دوست", "ایباد",
        "فتح", "غوث الدین", "هدایت", "اسحاق", "جواد", "کمال",
        "لطف", "پرویز", "قدرت", "رحیم الله", "صابر", "توفیق",
        "وداد", "وهاب", "یحیی", "زلمی", "ایمل", "بابر",
        "دل", "فرهاد", "ګلب الدین", "عرفان", "جهانګیر", "رحمت الله",
        "ساحل", "وسیف", "ولي الله", "زکی", "عارف", "بلال",
        "چمن الله", "فضل الله", "جمشید", "خلیل الله", "لطیف الله", "نظیر",
        "سمیع الله", "تاج الدین", "وارث", "یاسین", "ذبیح", "اسلم",
        "خیرالله", "سپین ګل", "تور ګل", "سپین زر", "ګلبهار", "اباسین",
        "عبد ال", "اېمل", "علي", "عالم", "عالم زیب", "امېل",
        "امو", "اندام", "انګار", "ارمغان", "ارمان", "ارسلان",
        "آرئین", "اسفند", "اسفندیار", "اتل", "اتڅک", "اورنګ",
        "اول میر", "ازلان", "ازمرې", "بابک", "بابرک", "باچا",
        "بادام", "بهره مند", "بهرور", "بخت", "بخت روان", "ختور",
        "بلاڅ", "بلی", "برلاس", "بریال", "بریالې", "بصیر",
        "باټور", "بازګر", "بازیر", "بهروذ", "بېلتون", "چارګل",
        "ډګر", "دراب", "درمان", "دروېش", "دریاب", "دولت",
        "دوړ", "دیار", "دلاور", "درون", "ایلام", "فرهنګ",
        "فریدون", "ګهېز", "ګېډئ", "غېرت", "غښتالې", "غلجي",
        "غمې", "غرڅنې", "غټول", "غزن", "غزین", "غورزنګ",
        "غونچه ګل", "غورغشت", "ګوګل", "غوربت", "ګران", "ګلباز",
        "ګل جان", "ګل مست", "ګل رنګ", "ګل یار", "ګل زمان", "ګلاب",
        "هسک", "هېلمند", "هېواد", "حکم", "جانان", "جنت ګل",
        "جنډول", "کاکې", "کرلاڼي", "کارمل", "کاروان", "ښاغلې",
        "ښائسته", "خاک", "خالو", "خاندور", "خیالې", "خوږ",
        "خوشال", "خوش دل", "خوزون", "خیبر", "کوچې", "کوشان",
        "لاجبر", "لښکر", "لعل", "لؤنګ", "لونګین", "لمر",
        "لېوال", "میړانې", "میوند", "ملنګ", "ملوک", "مالیار",
        "منان", "منګل", "مرغوز", "مرجان", "مړوند", "مشال",
        "مهتر", "منت بار", "میر ویس", "میرزل", "موهمبر", "محمود",
        "ننګ", "ننګیالې", "نومیالې", "نفېل", "اولس", "اولس یار",
        "اولسیار", "پېمان", "پامیر", "پشتون", "پاڅون", "پتنګ",
        "پاتمن", "پټوال", "پتیال", "پیوستون", "پېلابو", "پېرزو",
        "پوهاند", "پور دل", "پونده", "سپرلې", "قجیر ګل", "قلندر",
        "رحم دل", "رنګین", "ړیدې", "ریشتین", "روشان", "روښان",
        "رستم", "سباون", "سادین", "سحر", "سحر ګل", "سهیم",
        "سېفور", "سالار", "سمندر", "سمون", "سمسور", "سنګر",
        "سنګین", "سنګرېز", "سنوبر", "سرابن", "سرباز", "سردار",
        "سرتور", "سائل", "سیلاب", "سېلاني", "شاه سوار", "شاه زر",
        "شمال", "شمشاد", "شیر", "شیر دل", "شېرین", "شین ګل",
        "شیندي ګل", "شینو", "شپول", "شپون", "شجاء", "صبغت الله",
        "صفت", "سکندر", "سهراب", "سپېڅلې", "ستورې", "سور ګل",
        "سوئېل", "تعبان", "تنیم", "تړون", "تاؤس", "ټیري",
        "طوفان", "ټولواک", "توریال", "طوطي", "توران", "توریالې",
        "ودان", "وېس", "واکدار", "واکمن", "یمه", "یون",
        "زعفران", "ځلان", "ځلند", "ځلاند", "زلمې", "زپران",
        "زر ګل", "زرولي", "زرک", "زرم", "زرنګ", "زربت",
        "زرداب", "زرګر", "زرغون", "زړور", "زړګې", "زرین",
        "زرکاڼې", "زرلېش", "زرمست", "زرنوش", "زریاب", "زوار",
        "ژور", "زږرد", "زیار", "زیار مل", "زیګر", "زمرک",
        "زمرې", "زورک", "زورور", "ځواک", "ژوندون",
    ]

    pashto_female_first_names = [
        "مریم", "فاطمه", "زهرا", "لیلی", "نادیه", "صبرینه",
        "ثریا", "پروین", "شکریه", "فرشته", "هادیه", "جمیله",
        "کمیله", "نرګس", "رضیه", "صافیه", "تمنا", "وجیهه",
        "یاسمین", "زرمنه", "ګل الای", "میرمن", "سپین ګل", "تور پیکۍ",
        "وږمه", "شمسیه", "نغمه", "مشعل", "سنګه", "زرغونه",
        "عایشه", "بی بی", "چمن", "دل افروز", "ایمان", "فرحناز",
        "ګل", "هدیه", "ارم", "جهان آرا", "خدیجه", "لال زری",
        "مهناز", "نبیله", "عذرا", "پروانه", "قمر", "رحیله",
        "سحر", "تبسم", "عظمی", "ویدا", "وحیده", "یلدا",
        "زینب", "افسانه", "بخت", "دردانه", "فوزیه", "ګلشن",
        "حوا", "عفت", "کلثوم", "معصومه", "نجیبه", "عمره",
        "پلوشه", "قبره", "رحیمه", "سکینه", "طاهره", "عروج",
        "وجمه", "یاسره", "زرقه", "عقیله", "بشری", "چنار",
        "دل ربا", "ایشل", "فریال", "ګلنار", "هینا", "عنایت",
        "جوهره", "کاوش", "لمر", "منیره", "نسرین", "امید",
        "پریسا", "قدسیه", "صدف", "تسلیمه", "امیره", "وسیله",
        "وزیره", "یمنه", "ذبیحه", "انیسه", "بهر", "چین",
        "دریا", "الهام", "فرخنده", "ګلرخ", "هرا", "اقراء",
        "جوید", "کیران", "لیلما", "مهره", "نازیه", "اورانه",
        "پری", "قرات", "رحمت", "صائمه", "ورثه", "ذولفقه",
        "بانو", "چمن آرا", "دلشاد", "فرزانه", "ګلبانو", "هما",
        "جنت", "کشمله", "مهوش", "امیمه", "پیمان", "قمریه",
        "روشنه", "صغری", "تارا", "علفت", "زاره", "عالیه",
        "دلبر", "ایما", "فهیمه", "ګلبهار", "هینه", "جویریه",
        "خالده", "مهیره", "نسیم", "امیده", "پری زاد", "رخساره",
        "صبا", "تسنیم", "عروسه", "وسیمه", "وجدان", "زارین",
        "امینه", "عفیه", "اغله", "عمبرین", "انګېزه", "آپانه",
        "اریانه", "بدري", "بختوره", "بلبله", "بنفشه", "برساله",
        "بي بي", "روښانه", "بریښنا", "ډیوه", "درخانیي", "ګبینه",
        "ګلې", "غټوله", "غوټې", "غونچه", "ګرانه", "بانو ګل",
        "لښته", "ګل مکي", "مینه", "ګل پاڼه", "څانګه", "ورین",
        "ګلالي", "ګلچین", "هاله", "هیلي", "هلیه", "حنه",
        "هوسي", "کشماله", "ښایسته", "ښاپېري", "ښارو", "خاټول",
        "ښکلې", "خوږه", "کوچې", "کونتره", "لیلۍ", "لیلومه",
        "لخته", "للمه", "لال", "زاري", "لمبه", "لونګه",
        "لیمه", "ماه جبین", "ماه نور", "نور ماه", "ځاله", "ملالي",
        "ملغلره", "مکیي", "مرچکې", "مسکا", "ننګیالي", "نارنجه",
        "نتکې", "نؤیاته", "نازنینه", "نازدانه", "نازو", "نیازمینه",
        "اوربخته", "اورژاله", "پاڼه", "پرغونډه", "پشمینه", "پتاسه",
        "پېغره", "پرخه", "پوخله", "رڼا", "رایان", "ریښمینه",
        "ریښتینه", "روشینه", "سندره", "سنګینه", "سینزله", "شاغلې",
        "شاهې", "لالیي", "شمیره", "شمله", "شاندانه", "شانزي",
        "شاپېري", "شاستیي", "شازمینه", "شېرین", "شینکي", "شینوګیي",
        "شوغله", "سیلي", "سپرغي", "سپوږمي", "سپوژمي", "ستوري",
        "تعبانه", "تلوسه", "تورپیکي", "اوګي", "ودانه", "وجیه",
        "ورده", "واورینه", "وړنګه", "ورېشمین", "زېن", "زېتونه",
        "زکیه", "ژاله", "ځالنده", "زمده", "بي بي زره", "زره بي بي",
        "زر", "مسته", "زرمینه", "زرورین", "زره", "باحه",
        "زرینه", "زریش", "زرکه", "زرلښته", "زرسانګه", "زرتاج",
        "ژالي", "زهل", "زفاش", "انار", "آرا", "بله نشته",
        "بزیره", "نېنظیره", "بي بي روښانه", "درخانئي", "غورشکه", "ګورګوره",
        "ګل بانو", "ګل غوټې", "ګل لښته", "ګل مکئ", "ګل مینه", "ګل څانګه",
        "ګل ورین", "ګلالئ", "هیلئ", "هوسئ", "ښائسته", "ښاپېرئ",
        "خوش بخته", "لال زاري", "ماه ځاله", "ملالئ", "مینا", "مکئي",
        "منؤره", "ننګیالئ", "اوربله", "پریورش", "سلګئ", "سیلئ",
        "شاه لالئي", "شانزئ", "شاپېرئ", "شاستئي", "شینکئ", "شینوګئي",
        "سپلمئ", "سپرغئ", "سپېځله", "سپوژمئ", "سپوږمئ", "ستورئ",
        "تل وسه", "تنیمه", "تور پیکائ", "اوګئ", "زېن با", "ځلوبه",
        "زر بي بي", "زر مسته", "زر باحه", "زرشاله", "ژالئ",
    ]

    last_names = [
        "دراني", "پوپلزي", "بارکزي", "الکوزي", "اڅکزي", "غلجي",
        "هوتک", "توخي", "ناصر", "خروټي", "سولېمان خېل", "علي خېل",
        "ابراهیم خېل", "یوسفزي", "مومند", "افریدي", "شینواري", "محسود",
        "وزیر", "داور", "بانوڅي", "خټک", "اورکزي", "ترین",
        "کاکړ", "ماندر", "شرني", "منګل", "زدران", "چمکني",
        "تاني", "احمدزي", "نورزي", "لودهي", "مروټ", "نیازي",
        "سور", "اندړ", "ګګیاڼي", "خلیل", "داؤدزي", "بابي",
        "ګدون", "ملاګوري", "اتمان خېل", "توري", "بنګښ", "ساپي",
        "جاجي", "خوګیاڼي", "وتر", "پڼي", "ستوري", "مرکي",
        "لوني", "احمدي", "رحیمي", "عزیزي", "نورزاي", "تاجک",
        "زیارت", "افغان", "نورستاني", "زند", "پښتون", "میوند",
        "کوچی", "اڅکزی", "هزاره", "اشرف", "کندهاري", "یوسفزی",
        "زمر", "شینواری", "میر", "قریشي", "سعید", "ګل",
        "صافي", "شیراني", "کریم", "احمدزاده", "شاه", "بهادر",
        "مرتضي", "حکیم", "جهانګیر", "ظاهر", "جلال", "لطیف",
        "بابر", "فاروق", "عمر", "قاسم", "جمال", "فرید",
        "لاله", "ګوهر", "ګلزار", "بشیر", "غلام", "نور",
        "شیرزاد", "مومن", "طالب", "امین", "فقیر", "امیر",
        "زمان", "یوسف", "احمدشاه",
    ]

    # ================ Email section =====================

    last_names_email = [
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

    male_first_names = [
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

    female_first_names = [
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

    domains = [
        "gmail.com", "yahoo.com", "outlook.com", "afghanmail.com", "mail.com"
    ]

    # ---------- BASIC PARTS ----------
    @staticmethod
    def _slug(value: str) -> str:
        """Strip a name down to the characters an address may contain.

        Several names are two words ("Bakht Awar"), which previously left a
        space inside the generated email address.
        """
        return re.sub(r"[^a-z0-9]+", "", value.lower())

    def username(self, gender=None):
        """Random Afghan-style username, transliterated for use in an address."""
        if gender in ("F", "female", "ښځينه"):
            pool = self.female_first_names
        elif gender in ("M", "male", "نارينه"):
            pool = self.male_first_names
        else:
            pool = self.male_first_names + self.female_first_names

        first = self._slug(self.generator.random.choice(pool))

        last = self._slug(self.generator.random.choice(self.last_names_email))
        number = str(self.generator.random.randint(1, 999))
        return f"{first}.{last}{number}"

    def user_name(self, gender=None):
        """Standard formatter name for :meth:`username`."""
        return self.username(gender)

    def email(self, gender=None):
        """Full email address"""
        return f"{self.username(gender)}@{self.generator.random.choice(self.domains)}"

        # =================End of the email section ==============

    def first_name_male(self):
        first = self.generator.random.choice(self.pashto_male_first_names)
        return first

    def first_name_female(self):
        firstFemale = self.generator.random.choice(self.pashto_female_first_names)
        return firstFemale

    def last_name(self):
        last = self.generator.random.choice(self.last_names)
        return last

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
