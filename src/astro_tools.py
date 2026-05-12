"""
Advanced Jyotish calculation tools.
Yogas, Sade Sati, Mangal Dosha, Ashtakavarga, Divisional Charts, Varshaphal, Muhurta.
"""

import swisseph as swe
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional

SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
         "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
SIGN_IDX = {s: i for i, s in enumerate(SIGNS)}

SIGN_LORDS = {
    "Aries":"Mars","Taurus":"Venus","Gemini":"Mercury","Cancer":"Moon",
    "Leo":"Sun","Virgo":"Mercury","Libra":"Venus","Scorpio":"Mars",
    "Sagittarius":"Jupiter","Capricorn":"Saturn","Aquarius":"Saturn","Pisces":"Jupiter"
}
OWN_SIGNS = {
    "Sun":["Leo"],"Moon":["Cancer"],"Mars":["Aries","Scorpio"],
    "Mercury":["Gemini","Virgo"],"Jupiter":["Sagittarius","Pisces"],
    "Venus":["Taurus","Libra"],"Saturn":["Capricorn","Aquarius"],
    "Rahu":[],"Ketu":[]
}
EXALTATION   = {"Sun":"Aries","Moon":"Taurus","Mars":"Capricorn","Mercury":"Virgo",
                 "Jupiter":"Cancer","Venus":"Pisces","Saturn":"Libra"}
DEBILITATION = {"Sun":"Libra","Moon":"Scorpio","Mars":"Cancer","Mercury":"Pisces",
                 "Jupiter":"Capricorn","Venus":"Virgo","Saturn":"Aries"}


def _house(planet_sign: str, lagna_sign: str) -> int:
    return ((SIGN_IDX.get(planet_sign, 0) - SIGN_IDX.get(lagna_sign, 0)) % 12) + 1

def _is_kendra(h): return h in [1, 4, 7, 10]
def _is_trikona(h): return h in [1, 5, 9]
def _is_upachaya(h): return h in [3, 6, 10, 11]
def _is_dusthana(h): return h in [6, 8, 12]

def _lords_of(lagna_sign: str, house_nums: List[int]) -> List[str]:
    li = SIGN_IDX[lagna_sign]
    seen, out = set(), []
    for h in house_nums:
        lord = SIGN_LORDS.get(SIGNS[(li + h - 1) % 12], "")
        if lord and lord not in seen:
            seen.add(lord)
            out.append(lord)
    return out


# ─── 1. YOGA DETECTION ───────────────────────────────────────────────────────

def detect_yogas(planets: Dict, lagna: Dict) -> List[Dict]:
    ls = lagna.get("sign", "")
    if not ls:
        return []

    yogas: List[Dict] = []

    def ps(n): return planets.get(n, {}).get("sign", "")
    def pd(n): return planets.get(n, {}).get("degree_in_sign", 0)
    def ph(n): s = ps(n); return _house(s, ls) if s else None

    # Gaja Kesari — Jupiter kendra from Moon
    if ps("Jupiter") and ps("Moon"):
        h_jup_from_moon = ((SIGN_IDX.get(ps("Jupiter"),0) - SIGN_IDX.get(ps("Moon"),0)) % 12) + 1
        if h_jup_from_moon in [1, 4, 7, 10]:
            yogas.append({
                "name": "Gaja Kesari", "type": "Raj Yoga", "strength": "Strong",
                "planets": ["Jupiter", "Moon"],
                "description": "Jupiter in kendra from Moon — wisdom, reputation, institutional authority.",
                "business_impact": "Rise through merit. Trusted advisor status. Wealth through knowledge and networks."
            })

    # Budha-Aditya — Sun + Mercury same sign, within 15°
    if ps("Sun") and ps("Mercury") and ps("Sun") == ps("Mercury"):
        orb = abs(pd("Sun") - pd("Mercury"))
        if orb <= 15:
            yogas.append({
                "name": "Budha-Aditya", "type": "Intelligence Yoga",
                "strength": "Very Strong" if orb <= 5 else "Strong",
                "planets": ["Sun", "Mercury"],
                "description": f"Sun and Mercury conjunct ({orb:.1f}° orb). Sharp intellect aligned with identity.",
                "business_impact": "Excellence in negotiation, strategy, and communication-led authority roles."
            })

    # Pancha Mahapurusha — planet in own/exalted sign in kendra
    MAHA = {
        "Mars":    ("Ruchaka",  "Warrior-Commander. Drive, courage, decisive execution."),
        "Mercury": ("Bhadra",   "Strategist. Systems thinking and articulate leadership."),
        "Jupiter": ("Hamsa",    "Philosopher-Advisor. Wisdom, ethics, expansive vision."),
        "Venus":   ("Malavya",  "Aesthetic-Diplomat. Refined taste, strategic partnerships."),
        "Saturn":  ("Shasha",   "Institutional Builder. Discipline, endurance, legacy."),
    }
    for planet, (yname, desc) in MAHA.items():
        p_s = ps(planet); p_h = ph(planet)
        if not p_s or not p_h: continue
        in_own   = p_s in OWN_SIGNS.get(planet, [])
        in_exalt = p_s == EXALTATION.get(planet, "")
        if (in_own or in_exalt) and _is_kendra(p_h):
            yogas.append({
                "name": f"{yname} Yoga", "type": "Mahapurusha",
                "strength": "Very Strong" if in_exalt else "Strong",
                "planets": [planet],
                "description": f"{planet} in {'exaltation' if in_exalt else 'own sign'} ({p_s}), house {p_h}. {desc}",
                "business_impact": f"Signature archetype of the chart — exceptional prominence in {planet}'s domains."
            })

    # Raj Yoga — kendra lord + trikona lord in conjunction
    k_lords = _lords_of(ls, [1, 4, 7, 10])
    t_lords = _lords_of(ls, [1, 5, 9])
    seen_raj: set = set()
    for kl in k_lords:
        for tl in t_lords:
            if kl == tl or not ps(kl) or not ps(tl): continue
            pair = tuple(sorted([kl, tl]))
            if pair in seen_raj: continue
            if ps(kl) == ps(tl):
                seen_raj.add(pair)
                pair_key = tuple(sorted([kl, tl]))
                _RAJ_IMPACTS = {
                    ("Mars", "Sun"):     "Frontline authority — courage and executive drive in the same house. Built for leadership under pressure.",
                    ("Mars", "Venus"):   "Creative force meets ambition — excellence in design, brand, and performance roles.",
                    ("Mars", "Jupiter"): "Ethical warrior — strategic expansion backed by the discipline to execute without compromise.",
                    ("Mars", "Mercury"): "Sharp tactical mind — wins through precision analysis and rapid decisive action.",
                    ("Mars", "Moon"):    "Instinctive leader — reads the room faster than anyone and acts before others have decided.",
                    ("Mars", "Saturn"):  "Iron will — slow to rise but near-impossible to displace once in position.",
                    ("Sun", "Venus"):    "Charisma and authority — public-facing leadership that also builds loyalty and aesthetic trust.",
                    ("Sun", "Jupiter"):  "The king's advisor — natural statesperson combining vision with legitimacy.",
                    ("Sun", "Mercury"):  "Intellectual authority — commands through clarity of thought and persuasive communication.",
                    ("Sun", "Moon"):     "Public presence with emotional intelligence — people trust both your competence and your character.",
                    ("Sun", "Saturn"):   "Earned authority — recognised as the person who does the hard thing correctly.",
                    ("Venus", "Jupiter"): "Wealth and wisdom — attracts resources through culture, creativity, and ethical positioning.",
                    ("Venus", "Mercury"): "Commercial creativity — monetises ideas, networks, and aesthetic intelligence.",
                    ("Venus", "Moon"):   "Magnetic empathy — success through relationships, trust, and genuine care for people.",
                    ("Venus", "Saturn"): "Disciplined beauty — long-term brand and reputation builder who outlasts trendier competitors.",
                    ("Jupiter", "Mercury"): "Strategic teacher — turns complex knowledge into accessible, scalable impact.",
                    ("Jupiter", "Moon"): "Generous intuition — wisdom amplified by emotional depth; trusted advisor archetype.",
                    ("Jupiter", "Saturn"): "The long-game master — combines vision with the patience to build institutions that last.",
                    ("Mercury", "Moon"): "Fast, empathetic communicator — reads people and responds with exactly what is needed.",
                    ("Mercury", "Saturn"): "Precision under pressure — methodical thinker who delivers in high-stakes environments.",
                    ("Moon", "Saturn"):  "Resilient authority — tested by difficulty and trusted because of it.",
                }
                impact = _RAJ_IMPACTS.get(pair_key, "Authority and rise to leadership through the combined force of these two planetary lords.")
                yogas.append({
                    "name": "Raj Yoga", "type": "Royal Yoga", "strength": "Strong",
                    "planets": [kl, tl],
                    "description": f"{kl} (kendra lord) and {tl} (trikona lord) conjunct in {ps(kl)}.",
                    "business_impact": impact
                })

    # Adhi Yoga — Jupiter, Mercury, Venus in 6/7/8 from Moon
    if ps("Moon"):
        mi = SIGN_IDX.get(ps("Moon"), 0)
        adhi = [p for p in ["Jupiter","Mercury","Venus"]
                if ps(p) and ((SIGN_IDX.get(ps(p),0) - mi) % 12) + 1 in [6, 7, 8]]
        if len(adhi) >= 2:
            yogas.append({
                "name": "Adhi Yoga", "type": "Authority Yoga",
                "strength": "Very Strong" if len(adhi) == 3 else "Strong",
                "planets": adhi,
                "description": f"{', '.join(adhi)} in 6–8th from Moon. Natural command.",
                "business_impact": "Born to lead — command positions and authority over others."
            })

    # Neecha Bhanga Raja Yoga — debilitated planet, cancellation conditions met
    for planet, deb_s in DEBILITATION.items():
        if ps(planet) != deb_s: continue
        cancelled = False
        deb_lord = SIGN_LORDS.get(deb_s, "")
        if ps(deb_lord) and _is_kendra(ph(deb_lord) or 0): cancelled = True
        exalt_lord = SIGN_LORDS.get(EXALTATION.get(planet, ""), "")
        if exalt_lord and ps(exalt_lord) and _is_kendra(ph(exalt_lord) or 0): cancelled = True
        if cancelled:
            yogas.append({
                "name": "Neecha Bhanga Raja Yoga", "type": "Cancellation Yoga", "strength": "Moderate",
                "planets": [planet],
                "description": f"{planet} debilitated in {deb_s} but cancellation conditions are met.",
                "business_impact": f"Initial struggle in {planet}'s domains transforms into exceptional strength."
            })

    return yogas


# ─── 2. SADE SATI ────────────────────────────────────────────────────────────

def check_sade_sati(natal_moon_sign: str, current_saturn_sign: str) -> Dict:
    mi  = SIGN_IDX.get(natal_moon_sign, 0)
    si  = SIGN_IDX.get(current_saturn_sign, 0)
    diff = (si - mi) % 12

    PHASES = {
        11: ("Rising (Approaching)", "Moderate",
             "Saturn approaching your Moon sign. External pressures begin — relationships, home life, mindset being restructured."),
        0:  ("Peak (Direct)",        "High",
             "Saturn transiting your natal Moon sign. The peak phase — deep transformation, mental discipline tested, karmic clearing at maximum intensity."),
        1:  ("Setting (Departing)",  "Moderate",
             "Saturn past your Moon sign — Sade Sati completing. Gradual relief, lessons integrating, foundation stabilising."),
    }

    if diff in PHASES:
        phase, severity, desc = PHASES[diff]
        active = True
        years_remaining = {11: 5.0, 0: 2.5, 1: 2.5}[diff]
    else:
        phase, severity, desc = "Not Active", "None", f"No Sade Sati. Saturn is {diff} signs ahead of your natal Moon."
        active = False
        years_remaining = 0

    return {
        "active": active, "phase": phase, "severity": severity,
        "natal_moon_sign": natal_moon_sign, "current_saturn_sign": current_saturn_sign,
        "description": desc, "years_remaining": years_remaining,
        "remedies": [
            "Saturday fasting and Shani Puja",
            "Service to elderly or underprivileged",
            "Chant: Om Sham Shanicharaya Namah (108× daily)",
            "Donate black sesame and mustard oil on Saturdays",
            "Wear dark blue or black on Saturdays"
        ] if active else []
    }


# ─── 3. MANGAL DOSHA ─────────────────────────────────────────────────────────

def check_mangal_dosha(planets: Dict, lagna: Dict) -> Dict:
    ls = lagna.get("sign", "")
    if "Mars" not in planets or not ls:
        return {"active": False, "description": "Data unavailable"}

    mars_sign = planets["Mars"]["sign"]
    SEVERITY = {1: "High", 2: "Moderate", 4: "Moderate", 7: "High", 8: "Very High", 12: "Moderate"}

    def check_from(ref_sign):
        if not ref_sign or ref_sign not in SIGN_IDX: return None
        h = _house(mars_sign, ref_sign)
        return {"active": h in SEVERITY, "house": h, "severity": SEVERITY.get(h, "None")}

    from_lagna  = check_from(ls)
    from_moon   = check_from(planets.get("Moon",  {}).get("sign", ""))
    from_venus  = check_from(planets.get("Venus", {}).get("sign", ""))

    cancellations = []
    if mars_sign in OWN_SIGNS.get("Mars", []):
        cancellations.append("Mars in own sign (Aries/Scorpio) — dosha significantly reduced")
    if mars_sign == EXALTATION.get("Mars", ""):
        cancellations.append("Mars exalted in Capricorn — dosha cancelled")
    if planets.get("Jupiter", {}).get("sign") == mars_sign:
        cancellations.append("Jupiter conjunct Mars — benefic influence reduces dosha")
    if planets.get("Saturn", {}).get("sign") == mars_sign:
        cancellations.append("Saturn conjunct Mars — mutual cancellation applies")

    primary_active = from_lagna.get("active", False) if from_lagna else False
    effective_sev  = (from_lagna.get("severity", "None") if not cancellations
                      else "Reduced") if primary_active else "None"

    return {
        "active": primary_active, "mars_sign": mars_sign,
        "mars_house_from_lagna": from_lagna.get("house") if from_lagna else None,
        "from_lagna": from_lagna, "from_moon": from_moon, "from_venus": from_venus,
        "severity": effective_sev, "cancellations": cancellations,
        "description": (
            f"Mars in {mars_sign} (house {from_lagna.get('house','?')} from Lagna) — "
            + ("Mangal Dosha present" + (f" · {len(cancellations)} cancellation(s) apply" if cancellations else "")
               if primary_active else "No Mangal Dosha from Lagna")
        ),
        "remedies": [
            "Mangal Puja on Tuesdays",
            "Chant: Om Angarakaya Namah (108× on Tuesdays)",
            "Donate red lentils on Tuesdays",
            "Feed Hanuman ji on Tuesdays"
        ] if primary_active and not cancellations else []
    }


# ─── 4. ASHTAKAVARGA (simplified Sarvashtakavarga) ───────────────────────────

def calculate_ashtakavarga(planets: Dict, lagna: Dict) -> Dict:
    """
    Approximate Sarvashtakavarga — relative planetary strength per house.
    Scores by dignity, house quality, and aspect contributions.
    Each planet contributes to its own house (full) plus aspected houses (partial):
    all planets aspect 7th; Mars/Rahu/Ketu add 4th+8th; Jupiter adds 5th+9th; Saturn adds 3rd+10th.
    """
    ls = lagna.get("sign", "")
    BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
    HOUSE_DOMAINS = {
        1:"Self & Identity", 2:"Wealth & Speech", 3:"Effort & Siblings",
        4:"Home & Happiness", 5:"Intellect & Children", 6:"Disputes & Health",
        7:"Partnership & Business", 8:"Transformation & Longevity",
        9:"Dharma & Fortune", 10:"Career & Status", 11:"Gains & Network",
        12:"Expenditure & Liberation"
    }
    # 0-indexed offsets for special aspects (4th=+3, 5th=+4, 8th=+7, 9th=+8, 3rd=+2, 10th=+9)
    EXTRA_ASPECT_OFFSETS = {
        "Mars":    [3, 7],
        "Jupiter": [4, 8],
        "Saturn":  [2, 9],
        "Rahu":    [4, 8],
        "Ketu":    [4, 8],
    }

    raw = {h: 0 for h in range(1, 13)}
    for planet, info in planets.items():
        s = info.get("sign", "")
        if not s or s not in SIGN_IDX: continue
        h = _house(s, ls)

        base    = 4 if (_is_kendra(h) or _is_trikona(h)) else (3 if _is_upachaya(h) else (1 if _is_dusthana(h) else 2))
        dignity = (2  if s == EXALTATION.get(planet, "")   else
                   1  if s in OWN_SIGNS.get(planet, [])    else
                  -1  if s == DEBILITATION.get(planet, "") else 0)
        benef   = 1 if planet in BENEFICS else 0
        score   = base + dignity + benef
        raw[h] += score

        # Universal 7th aspect
        h7 = ((h - 1 + 6) % 12) + 1
        raw[h7] += max(1, score // 2)

        # Special aspects
        for off in EXTRA_ASPECT_OFFSETS.get(planet, []):
            ha = ((h - 1 + off) % 12) + 1
            raw[ha] += max(1, score // 3)

    max_r  = max(raw.values()) or 1
    bindus = {h: min(8, max(0, round(v / max_r * 8))) for h, v in raw.items()}

    def strength(b): return "Strong" if b >= 6 else ("Moderate" if b >= 4 else "Weak")

    return {
        "note": "Approximate Sarvashtakavarga — relative planetary strength per house",
        "houses": {
            h: {"bindus": bindus[h], "strength": strength(bindus[h]), "domain": HOUSE_DOMAINS[h]}
            for h in range(1, 13)
        },
        "strong_houses": [h for h in range(1, 13) if strength(bindus[h]) == "Strong"],
        "weak_houses":   [h for h in range(1, 13) if strength(bindus[h]) == "Weak"],
    }


# ─── 5. DIVISIONAL CHARTS (D-9 Navamsa, D-10 Dasamsa) ───────────────────────

def _navamsa(sign: str, deg: float) -> str:
    idx = SIGN_IDX.get(sign, 0)
    n   = min(8, int(deg / (10 / 3)))
    start = {0:"Aries", 4:"Aries", 8:"Aries",
             1:"Capricorn", 5:"Capricorn", 9:"Capricorn",
             2:"Libra",  6:"Libra",  10:"Libra",
             3:"Cancer", 7:"Cancer", 11:"Cancer"}.get(idx, "Aries")
    return SIGNS[(SIGN_IDX[start] + n) % 12]

def _dasamsa(sign: str, deg: float) -> str:
    idx = SIGN_IDX.get(sign, 0)
    n   = min(9, int(deg / 3))
    start = idx if idx % 2 == 0 else (idx + 8) % 12
    return SIGNS[(start + n) % 12]

def calculate_divisional_charts(planets: Dict, lagna: Dict) -> Dict:
    d9, d10 = {}, {}
    for name, info in planets.items():
        s, d = info.get("sign",""), info.get("degree_in_sign", 0)
        if s and s in SIGN_IDX:
            d9[name]  = {"sign": _navamsa(s, d), "natal_sign": s}
            d10[name] = {"sign": _dasamsa(s, d),  "natal_sign": s}

    ls, ld = lagna.get("sign",""), lagna.get("degree_in_sign", 0)
    if ls and ls in SIGN_IDX:
        d9["Lagna"]  = {"sign": _navamsa(ls, ld), "natal_sign": ls}
        d10["Lagna"] = {"sign": _dasamsa(ls, ld),  "natal_sign": ls}

    return {
        "d9": {
            "name": "Navamsa (D-9)",
            "purpose": "Soul, dharma, and the inner quality of each planet. Reveals who you are at the soul level and the deeper purpose behind natal placements.",
            "lagna": d9.get("Lagna", {}).get("sign", ""),
            "planets": d9
        },
        "d10": {
            "name": "Dasamsa (D-10)",
            "purpose": "Career, public life, and professional dharma. Reveals your role in the world and the domain where you will leave your mark.",
            "lagna": d10.get("Lagna", {}).get("sign", ""),
            "planets": d10
        }
    }


# ─── 6. VARSHAPHAL (Solar Return) ────────────────────────────────────────────

def calculate_varshaphal(natal_sun_longitude: float, lat: float, lon: float) -> Dict:
    """Find the Solar Return for the current year and cast the chart."""
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    t = datetime.utcnow()
    today_jd = swe.julday(t.year, t.month, t.day, t.hour + t.minute / 60.0 + t.second / 3600.0)
    target   = natal_sun_longitude % 360

    # Binary search — find the upcoming Solar Return (next occurrence ahead of today)
    lo, hi = today_jd - 5, today_jd + 380
    for _ in range(60):
        mid    = (lo + hi) / 2
        sun_lo = swe.calc_ut(mid, swe.SUN, flags)[0][0]
        diff   = (sun_lo - target + 360) % 360
        if diff < 180: hi = mid
        else:          lo = mid

    ret_jd          = (lo + hi) / 2
    yr, mo, dy, hr  = swe.revjul(ret_jd)

    # Planetary positions at return
    BODIES = {"Sun":swe.SUN,"Moon":swe.MOON,"Mars":swe.MARS,"Mercury":swe.MERCURY,
              "Jupiter":swe.JUPITER,"Venus":swe.VENUS,"Saturn":swe.SATURN,"Rahu":swe.MEAN_NODE}
    p_ret = {}
    for name, bid in BODIES.items():
        lo_deg = swe.calc_ut(ret_jd, bid, flags)[0][0]
        p_ret[name] = {"sign": SIGNS[int(lo_deg/30)], "degree_in_sign": round(lo_deg % 30, 2),
                       "is_retrograde": swe.calc_ut(ret_jd, bid, flags)[0][3] < 0}
    rahu_abs = SIGN_IDX[p_ret["Rahu"]["sign"]] * 30 + p_ret["Rahu"]["degree_in_sign"]
    ketu_abs = (rahu_abs + 180) % 360
    p_ret["Ketu"] = {"sign": SIGNS[int(ketu_abs/30)], "degree_in_sign": round(ketu_abs % 30, 2), "is_retrograde": True}

    # Lagna at birth location
    ayanamsa = swe.get_ayanamsa_ex(ret_jd, swe.FLG_SIDEREAL)[1]
    _, ascmc = swe.houses(ret_jd, lat, lon, b'W')
    lagna_lon = (ascmc[0] - ayanamsa) % 360
    ret_lagna = {"sign": SIGNS[int(lagna_lon/30)], "degree_in_sign": round(lagna_lon % 30, 2)}

    hour_utc, minute_utc = int(hr), int((hr - int(hr)) * 60)
    hour_ist = (hour_utc + 5) % 24
    minute_ist = minute_utc + 30
    if minute_ist >= 60: hour_ist += 1; minute_ist -= 60

    return {
        "return_date": f"{int(yr)}-{int(mo):02d}-{int(dy):02d}",
        "return_time_utc": f"{hour_utc:02d}:{minute_utc:02d}",
        "return_time_ist": f"{hour_ist:02d}:{minute_ist:02d}",
        "lagna": ret_lagna,
        "planets": p_ret,
        "year": int(yr),
        "interpretation": (
            f"Your upcoming {int(yr)} Solar Return rises with {ret_lagna['sign']} Lagna — "
            f"the energetic theme activates from {int(dy):02d}-{int(mo):02d}-{int(yr)}."
        )
    }


# ─── 7. MUHURTA (Auspicious Windows) ─────────────────────────────────────────

NAKSHATRAS_LIST = [
    "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
    "Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni",
    "Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
    "Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishtha","Shatabhisha",
    "Purva Bhadrapada","Uttara Bhadrapada","Revati"
]

NAK_QUALITY = {
    "Rohini":5,"Uttara Phalguni":5,"Uttara Ashadha":5,"Uttara Bhadrapada":5,
    "Pushya":5,"Ashwini":4,"Hasta":4,"Mrigashira":4,"Chitra":4,"Anuradha":4,"Revati":4,
    "Shravana":4,"Punarvasu":3,"Swati":3,"Dhanishtha":3,"Shatabhisha":3,
    "Krittika":2,"Vishakha":2,
    "Mula":1,"Jyeshtha":1,"Ardra":1,"Ashlesha":1,
    "Bharani":1,"Purva Phalguni":1,"Purva Ashadha":1,"Purva Bhadrapada":1,"Magha":1,
}

# Vara quality: Monday=0 … Sunday=6
VARA_Q    = {0:4, 1:2, 2:5, 3:5, 4:4, 5:2, 6:3}
VARA_NAME = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}
VARA_RULER= {0:"Moon",1:"Mars",2:"Mercury",3:"Jupiter",4:"Venus",5:"Saturn",6:"Sun"}

# Rahu Kaal start hour (IST, approx 6am sunrise) by weekday
RAHU_KAAL_IST = {0:7.5, 1:15, 2:12, 3:13.5, 4:10.5, 5:9, 6:16.5}
GOOD_TITHIS   = {2, 3, 5, 7, 10, 11, 13}

def calculate_muhurta(days: int = 7) -> List[Dict]:
    """Find auspicious 2-hour windows over the next N days (IST output)."""
    flags    = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    now_utc  = datetime.utcnow()
    results  = []

    for day_off in range(days):
        day     = now_utc.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=day_off)
        weekday = day.weekday()
        vara_q  = VARA_Q[weekday]
        rahu_start_ist = RAHU_KAAL_IST[weekday]

        day_windows = []

        for hour_utc in range(0, 24, 2):
            dt_utc  = day + timedelta(hours=hour_utc)
            hour_ist = (hour_utc + 5.5)  # IST offset
            if hour_ist >= 24: hour_ist -= 24

            jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                            dt_utc.hour + dt_utc.minute / 60.0)

            moon_lo  = swe.calc_ut(jd, swe.MOON, flags)[0][0]
            sun_lo   = swe.calc_ut(jd, swe.SUN,  flags)[0][0]

            nak_name  = NAKSHATRAS_LIST[int(moon_lo / (360/27)) % 27]
            nak_score = NAK_QUALITY.get(nak_name, 2)

            tithi_num = int(((moon_lo - sun_lo) % 360) / 12) + 1
            tithi_score = 4 if tithi_num in GOOD_TITHIS else 2

            in_rahu    = rahu_start_ist <= hour_ist < rahu_start_ist + 1.5
            rahu_pen   = -3 if in_rahu else 0

            total = vara_q + nak_score + tithi_score + rahu_pen

            if total >= 11:
                h_ist = int(hour_ist); m_ist = int((hour_ist - h_ist) * 60)
                day_windows.append({
                    "time_ist": f"{h_ist:02d}:{m_ist:02d}",
                    "nakshatra": nak_name,
                    "tithi": tithi_num,
                    "score": total,
                    "quality": "Excellent" if total >= 13 else "Good",
                    "rahu_kaal": in_rahu
                })

        if day_windows:
            results.append({
                "date": (day).strftime("%Y-%m-%d"),
                "vara": VARA_NAME[weekday],
                "vara_ruler": VARA_RULER[weekday],
                "windows": sorted(day_windows, key=lambda x: -x["score"])[:3]
            })

    return results
