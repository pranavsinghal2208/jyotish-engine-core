"""
One-shot seed script: inserts all people from the numerology master sheet
into the numerology_profiles SQLite table.

Run from the project root (venv active):
    python seed_numerology_profiles.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.database.session import engine, init_db
from src.database.models import NumerologyProfile
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------------------------
# (gender, label, first_name, middle_name, last_name, dob_DD-MM-YYYY)
# ---------------------------------------------------------------------------
PEOPLE = [
    # ── Celebrities — India ─────────────────────────────────────────────
    ("Male",   "srk",         "Shah Rukh",  "",        "Khan",            "02-11-1965"),
    ("Male",   "aib",         "Tanmay",     "Arun",    "Bhat",            "23-06-1987"),
    ("Female", "rihanna",     "Robyn",      "Rihanna", "Fenty",           "20-02-1988"),
    ("Male",   "messi",       "Lionel",     "Andres",  "Messi",           "24-06-1987"),
    ("Male",   "neymar",      "Neymar",     "da Silva","Santos Junior",   "05-02-1992"),
    ("Male",   "mukesh_a",    "Mukesh",     "Dhirubhai","Ambani",         "19-04-1957"),
    ("Male",   "ratan_tata",  "Ratan",      "Naval",   "Tata",            "28-12-1937"),
    ("Male",   "gautam_a",    "Gautam",     "Shantilal","Adani",          "24-06-1962"),
    ("Female", "falguni_n",   "Falguni",    "Sanjay",  "Nayar",           "19-02-1963"),
    ("Male",   "raghuram_r",  "Raghuram",   "Govind",  "Rajan",           "03-02-1963"),
    ("Male",   "narendra_m",  "Narendra",   "Damodardas","Modi",          "17-09-1950"),
    ("Male",   "sachin_t",    "Sachin",     "Ramesh",  "Tendulkar",       "24-04-1973"),
    ("Male",   "virat_k",     "Virat",      "",        "Kohli",           "05-11-1988"),
    ("Male",   "ms_dhoni",    "Mahendra",   "Singh",   "Dhoni",           "07-07-1981"),
    ("Male",   "neeraj_c",    "Neeraj",     "",        "Chopra",          "24-12-1997"),
    ("Male",   "amitabh_b",   "Amitabh",    "",        "Bachchan",        "11-10-1942"),
    ("Female", "alia_b",      "Alia",       "",        "Bhatt",           "15-03-1993"),
    ("Male",   "aamir_k",     "Aamir",      "",        "Khan",            "14-03-1965"),
    ("Female", "deepika_p",   "Deepika",    "",        "Padukone",        "05-01-1986"),
    ("Male",   "sundar_p",    "Sundar",     "",        "Pichai",          "10-06-1972"),
    ("Male",   "satya_n",     "Satya",      "",        "Nadella",         "19-08-1967"),
    ("Female", "indra_n",     "Indra",      "",        "Nooyi",           "28-10-1955"),
    ("Male",   "narayana_m",  "Narayana",   "",        "Murthy",          "20-08-1946"),
    ("Male",   "azim_p",      "Azim",       "Hashim",  "Premji",          "24-07-1945"),
    ("Female", "kiran_s",     "Kiran",      "Mazumdar","Shaw",            "23-03-1953"),
    ("Male",   "ar_rahman",   "A. R.",      "",        "Rahman",          "06-01-1967"),
    ("Male",   "rahul_g",     "Rahul",      "",        "Gandhi",          "19-06-1970"),
    ("Male",   "arvind_k",    "Arvind",     "",        "Kejriwal",        "16-08-1968"),

    # ── Celebrities — Global ────────────────────────────────────────────
    ("Male",   "elon_musk",   "Elon",       "Reeve",   "Musk",            "28-06-1971"),
    ("Male",   "bill_gates",  "Bill",       "",        "Gates",           "28-10-1955"),
    ("Male",   "mark_z",      "Mark",       "Elliot",  "Zuckerberg",      "14-05-1984"),
    ("Male",   "jeff_bezos",  "Jeff",       "Preston", "Bezos",           "12-01-1964"),
    ("Male",   "sam_altman",  "Sam",        "",        "Altman",          "22-04-1985"),
    ("Male",   "tim_cook",    "Tim",        "",        "Cook",            "01-11-1960"),
    ("Male",   "jensen_h",    "Jensen",     "",        "Huang",           "17-02-1963"),
    ("Male",   "warren_b",    "Warren",     "Edward",  "Buffett",         "30-08-1930"),
    ("Male",   "jack_ma",     "Jack",       "",        "Ma",              "10-09-1964"),
    ("Male",   "obama",       "Barack",     "Hussein", "Obama II",        "04-08-1961"),
    ("Male",   "trump",       "Donald",     "John",    "Trump",           "14-06-1946"),
    ("Male",   "trudeau",     "Justin",     "",        "Trudeau",         "25-12-1971"),
    ("Male",   "macron",      "Emmanuel",   "",        "Macron",          "21-12-1977"),
    ("Male",   "putin",       "Vladimir",   "Vladimirovich","Putin",      "07-10-1952"),
    ("Male",   "xi_jinping",  "Xi",         "",        "Jinping",         "15-06-1953"),
    ("Male",   "messi_dup",   "Lionel",     "Andres",  "Messi",           "24-06-1987"),
    ("Male",   "ronaldo",     "Cristiano",  "Ronaldo", "dos Santos Aveiro","05-02-1985"),
    ("Male",   "lebron",      "LeBron",     "Raymone", "James",           "30-12-1984"),
    ("Male",   "mj",          "Michael",    "Jeffrey", "Jordan",          "17-02-1963"),
    ("Male",   "novak_d",     "Novak",      "",        "Djokovic",        "22-05-1987"),
    ("Male",   "roger_f",     "Roger",      "",        "Federer",         "08-08-1981"),
    ("Male",   "rafa_n",      "Rafael",     "",        "Nadal",           "03-06-1986"),
    ("Male",   "mbappé",      "Kylian",     "",        "Mbappé Lottin",   "20-12-1998"),
    ("Female", "taylor_s",    "Taylor",     "Alison",  "Swift",           "13-12-1989"),
    ("Female", "beyonce",     "Beyoncé",    "Giselle", "Knowles-Carter",  "04-09-1981"),
    ("Female", "ariana_g",    "Ariana",     "",        "Grande-Butera",   "26-06-1993"),
    ("Female", "adele",       "Adele",      "Laurie Blue","Adkins",       "05-05-1988"),
    ("Female", "oprah",       "Oprah",      "Gail",    "Winfrey",         "29-01-1954"),
    ("Female", "malala",      "Malala",     "",        "Yousafzai",       "12-07-1997"),
    ("Female", "greta_t",     "Greta",      "",        "Thunberg",        "03-01-2003"),
    ("Male",   "hawking",     "Stephen",    "William", "Hawking",         "08-01-1942"),
    ("Male",   "einstein",    "Albert",     "",        "Einstein",        "14-03-1879"),
    ("Female", "marie_c",     "Marie",      "",        "Curie",           "06-11-1867"),
    ("Male",   "dalai_lama",  "Tenzin",     "",        "Gyatso",          "06-07-1935"),
    ("Male",   "demis_h",     "Demis",      "",        "Hassabis",        "27-07-1976"),
    ("Male",   "tim_bl",      "Tim",        "",        "Berners-Lee",     "08-06-1955"),
    ("Male",   "linus_t",     "Linus",      "Benedict","Torvalds",        "28-12-1969"),
    ("Male",   "magnus_c",    "Magnus",     "",        "Carlsen",         "30-11-1990"),
    ("Male",   "masayoshi_s", "Masayoshi",  "",        "Son",             "11-08-1957"),
    ("Male",   "rishi_s",     "Rishi",      "",        "Sunak",           "12-05-1980"),
    ("Male",   "zelensky",    "Volodymyr",  "Oleksandrovych","Zelenskyy", "25-01-1978"),
    ("Male",   "pope_francis","Jorge",      "Mario",   "Bergoglio",       "17-12-1936"),
    ("Male",   "bernard_a",   "Bernard",    "",        "Arnault",         "05-03-1949"),

    # ── Celebrities — India (batch 2) ───────────────────────────────────
    ("Female", "priyank_c",   "Priyanka",   "",        "Chopra",          "18-07-1982"),
    ("Male",   "shah_k",      "Shah",       "",        "Rukh Khan Jr.",   "05-05-2000"),
    ("Female", "sania_m",     "Sania",      "",        "Mirza",           "15-11-1986"),
    ("Male",   "pv_sindhu",   "Pusarla",    "Venkata", "Sindhu",          "05-07-1995"),
    ("Male",   "saurav_g",    "Sourav",     "",        "Ganguly",         "08-07-1972"),
    ("Male",   "kapil_d",     "Kapil",      "",        "Dev",             "06-01-1959"),
    ("Female", "lata_m",      "Lata",       "",        "Mangeshkar",      "28-09-1929"),
    ("Male",   "kishore_k",   "Kishore",    "",        "Kumar",           "04-08-1929"),
    ("Male",   "rk_narayan",  "R. K.",      "",        "Narayan",         "10-10-1906"),
    ("Male",   "arundhati_r", "Arundhati",  "",        "Roy",             "24-11-1961"),
    ("Male",   "manmohan_s",  "Manmohan",   "",        "Singh",           "26-09-1932"),
    ("Female", "indira_g",    "Indira",     "Priyadarshini","Gandhi",     "19-11-1917"),
    ("Male",   "apj_kalam",   "A. P. J.",   "Abdul",   "Kalam",           "15-10-1931"),
    ("Male",   "swami_v",     "Swami",      "",        "Vivekananda",     "12-01-1863"),
    ("Male",   "rabindranath","Rabindranath","",        "Tagore",          "07-05-1861"),
    ("Male",   "ravi_sh",     "Ravi",       "",        "Shankar",         "07-04-1920"),
    ("Male",   "byju_r",      "Byju",       "",        "Raveendran",      "05-01-1980"),
    ("Male",   "nithin_k",    "Nithin",     "",        "Kamath",          "05-04-1983"),
    ("Male",   "rohit_sh",    "Rohit",      "",        "Sharma",          "30-04-1987"),
    ("Female", "kangana_r",   "Kangana",    "",        "Ranaut",          "23-03-1987"),
    ("Male",   "hrithik_r",   "Hrithik",    "",        "Roshan",          "10-01-1974"),

    # ── Celebrities — Global (batch 2) ──────────────────────────────────
    ("Male",   "steve_jobs",  "Steve",      "Paul",    "Jobs",            "24-02-1955"),
    ("Male",   "larry_p",     "Larry",      "",        "Page",            "26-03-1973"),
    ("Male",   "sergey_b",    "Sergey",     "",        "Brin",            "21-08-1973"),
    ("Male",   "reed_h",      "Reed",       "",        "Hastings",        "08-10-1960"),
    ("Male",   "travis_k",    "Travis",     "",        "Kalanick",        "06-08-1976"),
    ("Male",   "jack_d",      "Jack",       "",        "Dorsey",          "19-11-1976"),
    ("Male",   "peter_t",     "Peter",      "",        "Thiel",           "11-10-1967"),
    ("Male",   "richard_b",   "Richard",    "",        "Branson",         "18-07-1950"),
    ("Male",   "george_s",    "George",     "",        "Soros",           "12-08-1930"),
    ("Female", "kamala_h",    "Kamala",     "Devi",    "Harris",          "20-10-1964"),
    ("Female", "angela_m",    "Angela",     "",        "Merkel",          "17-07-1954"),
    ("Female", "jacinda_a",   "Jacinda",    "",        "Ardern",          "26-07-1980"),
    ("Male",   "volodymyr_z", "Volodymyr",  "",        "Zelensky",        "25-01-1978"),
    ("Male",   "yuval_h",     "Yuval",      "Noah",    "Harari",          "24-02-1976"),
    ("Male",   "jordan_p",    "Jordan",     "Bernt",   "Peterson",        "12-06-1962"),
    ("Male",   "neil_dt",     "Neil",       "deGrasse","Tyson",           "05-10-1958"),
    ("Male",   "elon_x",      "X",          "",        "Æ A-12 Musk",     "04-05-2020"),

    # ── Athletes — Global ────────────────────────────────────────────────
    ("Male",   "usain_b",     "Usain",      "St. Leo", "Bolt",            "21-08-1986"),
    ("Female", "serena_w",    "Serena",     "Jameka",  "Williams",        "26-09-1981"),
    ("Female", "simone_b",    "Simone",     "Arianne", "Biles",           "14-03-1997"),
    ("Male",   "michael_ph",  "Michael",    "Fred",    "Phelps",          "30-06-1985"),
    ("Male",   "tyson_f",     "Tyson",      "Luke",    "Fury",            "12-08-1988"),
    ("Male",   "floyd_m",     "Floyd",      "Joy",     "Mayweather Jr.",  "24-02-1977"),
    ("Male",   "mike_ty",     "Mike",       "",        "Tyson",           "30-06-1966"),
    ("Female", "naomi_o",     "Naomi",      "",        "Osaka",           "16-10-1997"),
    ("Male",   "rafael_n2",   "Rafael",     "Nadal",   "Parera",          "03-06-1986"),
    ("Male",   "tiger_w",     "Tiger",      "",        "Woods",           "30-12-1975"),
    ("Male",   "conor_mc",    "Conor",      "Anthony", "McGregor",        "14-07-1988"),

    # ── Music & Entertainment — Global ──────────────────────────────────
    ("Male",   "eminem",      "Marshall",   "Bruce",   "Mathers III",     "17-10-1972"),
    ("Male",   "kanye_w",     "Kanye",      "Omari",   "West",            "08-06-1977"),
    ("Male",   "drake",       "Aubrey",     "Drake",   "Graham",          "24-10-1986"),
    ("Male",   "ed_sheeran",  "Edward",     "Christopher","Sheeran",      "17-02-1991"),
    ("Male",   "justin_b",    "Justin",     "Drew",    "Bieber",          "01-03-1994"),
    ("Female", "lady_gaga",   "Stefani",    "Joanne",  "Germanotta",      "28-03-1986"),
    ("Female", "madonna",     "Madonna",    "Louise",  "Ciccone",         "16-08-1958"),
    ("Male",   "mick_jagger", "Michael",    "Philip",  "Jagger",          "26-07-1943"),
    ("Male",   "elton_j",     "Elton",      "Hercules","John",            "25-03-1947"),
    ("Female", "celine_d",    "Céline",     "Marie",   "Dion",            "30-03-1968"),
    ("Male",   "will_smith",  "Willard",    "Carroll", "Smith II",        "25-09-1968"),
    ("Female", "angelina_j",  "Angelina",   "",        "Jolie",           "04-06-1975"),
    ("Male",   "leo_dicap",   "Leonardo",   "Wilhelm", "DiCaprio",        "11-11-1974"),
    ("Male",   "tom_hanks",   "Thomas",     "Jeffrey", "Hanks",           "09-07-1956"),

    # ── Scientists & Thinkers ────────────────────────────────────────────
    ("Male",   "nikola_t",    "Nikola",     "",        "Tesla",           "10-07-1856"),
    ("Male",   "darwin_c",    "Charles",    "Robert",  "Darwin",          "12-02-1809"),
    ("Male",   "freud_s",     "Sigmund",    "",        "Freud",           "06-05-1856"),
    ("Male",   "carl_j",      "Carl",       "Gustav",  "Jung",            "26-07-1875"),
    ("Male",   "noam_c",      "Noam",       "",        "Chomsky",         "07-12-1928"),
    ("Male",   "eckhart_t",   "Eckhart",    "",        "Tolle",           "16-02-1948"),
    ("Male",   "napoleon_h",  "Napoleon",   "",        "Hill",            "26-10-1883"),
    ("Male",   "alan_m",      "Alan",       "Mathison","Turing",          "23-06-1912"),
]

# ---------------------------------------------------------------------------

def seed():
    init_db()
    Session = sessionmaker(bind=engine)
    db = Session()

    inserted = 0
    skipped = 0

    for gender, label, first_name, middle_name, last_name, dob in PEOPLE:
        exists = db.query(NumerologyProfile).filter(NumerologyProfile.label == label).first()
        if exists:
            skipped += 1
            continue
        db.add(NumerologyProfile(
            label=label,
            gender=gender,
            first_name=first_name,
            middle_name=middle_name or None,
            last_name=last_name or None,
            dob=dob,
        ))
        inserted += 1

    db.commit()
    db.close()
    print(f"Done — {inserted} inserted, {skipped} already existed.")

if __name__ == "__main__":
    seed()
