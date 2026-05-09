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
