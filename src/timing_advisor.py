"""
Business Timing Advisor — maps current Dasha + transits to action-type windows.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any

# Action types and which planets/dashas favor them
ACTION_RULES = {
    "Launch": {
        "label": "Launch / Go Live",
        "favorable_planets": ["Sun", "Jupiter", "Mars"],
        "avoid_planets":     ["Saturn", "Rahu", "Ketu"],
        "favorable_dashas":  ["Sun", "Jupiter", "Mars", "Venus"],
        "avoid_dashas":      ["Saturn", "Rahu", "Ketu"],
        "description": "Starting something new — product, business, campaign.",
        "icon": "🚀",
    },
    "Sign": {
        "label": "Sign / Contract",
        "favorable_planets": ["Mercury", "Jupiter", "Venus"],
        "avoid_planets":     ["Saturn", "Rahu"],
        "favorable_dashas":  ["Mercury", "Jupiter", "Venus"],
        "avoid_dashas":      ["Saturn", "Rahu"],
        "description": "Agreements, deals, partnerships, contracts.",
        "icon": "✍️",
    },
    "Hire": {
        "label": "Hire / Team",
        "favorable_planets": ["Jupiter", "Venus", "Mercury"],
        "avoid_planets":     ["Mars", "Rahu", "Saturn"],
        "favorable_dashas":  ["Jupiter", "Venus", "Mercury"],
        "avoid_dashas":      ["Mars", "Rahu"],
        "description": "Bringing people in — hiring, partnerships, alliances.",
        "icon": "🤝",
    },
    "Invest": {
        "label": "Invest / Deploy Capital",
        "favorable_planets": ["Jupiter", "Venus", "Sun"],
        "avoid_planets":     ["Saturn", "Rahu", "Ketu", "Mars"],
        "favorable_dashas":  ["Jupiter", "Venus", "Sun"],
        "avoid_dashas":      ["Saturn", "Rahu", "Ketu"],
        "description": "Deploying money, capital allocation, major purchases.",
        "icon": "💰",
    },
    "Negotiate": {
        "label": "Negotiate / Persuade",
        "favorable_planets": ["Mercury", "Venus", "Jupiter"],
        "avoid_planets":     ["Mars", "Saturn"],
        "favorable_dashas":  ["Mercury", "Venus", "Jupiter"],
        "avoid_dashas":      ["Mars", "Saturn"],
        "description": "Sales conversations, salary negotiation, deals.",
        "icon": "🗣️",
    },
    "Travel": {
        "label": "Travel / Relocate",
        "favorable_planets": ["Jupiter", "Mercury", "Venus"],
        "avoid_planets":     ["Saturn", "Rahu", "Mars"],
        "favorable_dashas":  ["Jupiter", "Mercury", "Moon"],
        "avoid_dashas":      ["Saturn", "Rahu"],
        "description": "Business travel, field visits, relocation.",
        "icon": "✈️",
    },
}

# Nakshatra quality for timing
NAK_QUALITY = {
    "Rohini": 5, "Uttara Phalguni": 5, "Uttara Ashadha": 5, "Uttara Bhadrapada": 5,
    "Pushya": 5, "Ashwini": 4, "Hasta": 4, "Mrigashira": 4, "Chitra": 4,
    "Anuradha": 4, "Revati": 4, "Shravana": 4, "Punarvasu": 3,
    "Swati": 3, "Dhanishtha": 3, "Shatabhisha": 3, "Krittika": 2, "Vishakha": 2,
    "Mula": 1, "Jyeshtha": 1, "Ardra": 1, "Ashlesha": 1,
    "Bharani": 1, "Purva Phalguni": 1, "Purva Ashadha": 1, "Purva Bhadrapada": 1, "Magha": 1,
}

WEEKDAY_Q = {0: 4, 1: 2, 2: 5, 3: 5, 4: 4, 5: 2, 6: 3}
WEEKDAY_NAME = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
                3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

# Each planet rules a weekday; dasha lord's + nakshatra lord's day each get +2 bonus
PLANET_DAY = {
    "Sun": 6, "Moon": 0, "Mars": 1, "Mercury": 2,
    "Jupiter": 3, "Venus": 4, "Saturn": 5, "Rahu": 5, "Ketu": 1,
}

# Nakshatra → ruling planet (Vimshottari lords)
NAK_LORD = {
    "Ashwini": "Ketu", "Bharani": "Venus", "Krittika": "Sun",
    "Rohini": "Moon", "Mrigashira": "Mars", "Ardra": "Rahu",
    "Punarvasu": "Jupiter", "Pushya": "Saturn", "Ashlesha": "Mercury",
    "Magha": "Ketu", "Purva Phalguni": "Venus", "Uttara Phalguni": "Sun",
    "Hasta": "Moon", "Chitra": "Mars", "Swati": "Rahu",
    "Vishakha": "Jupiter", "Anuradha": "Saturn", "Jyeshtha": "Mercury",
    "Mula": "Ketu", "Purva Ashadha": "Venus", "Uttara Ashadha": "Sun",
    "Shravana": "Moon", "Dhanishtha": "Mars", "Shatabhisha": "Rahu",
    "Purva Bhadrapada": "Jupiter", "Uttara Bhadrapada": "Saturn", "Revati": "Mercury",
}


def _score_action(action_key: str, dasha_lord: str, current_planets: Dict,
                  nakshatra: str) -> Dict[str, Any]:
    rules = ACTION_RULES[action_key]

    # Dasha contribution (0-40)
    if dasha_lord in rules["avoid_dashas"]:
        dasha_score = 5
        dasha_status = "blocks"
    elif dasha_lord in rules["favorable_dashas"]:
        dasha_score = 35
        dasha_status = "supports"
    else:
        dasha_score = 20
        dasha_status = "neutral"

    # Transit contribution (0-40): count favorable vs avoid planets in benefic houses
    transit_score = 20  # base
    favorable_transits = []
    caution_transits = []
    for p in rules["favorable_planets"]:
        if p in current_planets:
            transit_score += 5
            favorable_transits.append(p)
    for p in rules["avoid_planets"]:
        if p in current_planets:
            transit_score -= 4
            caution_transits.append(p)
    transit_score = max(0, min(40, transit_score))
    transit_notes = [f"{p} favorable" for p in favorable_transits] + \
                    [f"{p} caution" for p in caution_transits]

    # Build a specific combined why-line
    if dasha_status == "supports" and favorable_transits:
        top_planets = " + ".join(favorable_transits[:2])
        dasha_note = f"{dasha_lord} Dasha + {top_planets} transits align for this."
    elif dasha_status == "supports":
        dasha_note = f"{dasha_lord} Dasha is the primary driver here — transits are mixed."
    elif dasha_status == "blocks" and caution_transits:
        top_caution = " and ".join(caution_transits[:2])
        dasha_note = f"{dasha_lord} Dasha + {top_caution} create friction — proceed cautiously."
    elif dasha_status == "blocks":
        dasha_note = f"{dasha_lord} Dasha works against this — wait for a better window."
    elif favorable_transits:
        top_planets = " + ".join(favorable_transits[:2])
        dasha_note = f"Transits ({top_planets}) compensate for a neutral Dasha period."
    else:
        dasha_note = f"{dasha_lord} Dasha is neutral — timing is workable but not amplified."

    # Nakshatra contribution (0-20)
    nak_q = NAK_QUALITY.get(nakshatra, 2)
    nak_score = round((nak_q / 5) * 20)

    total = dasha_score + transit_score + nak_score  # max 100

    if total >= 75:
        window = "Excellent"
        advice = f"Strong green light. {rules['description']} Act this week."
    elif total >= 55:
        window = "Favorable"
        advice = f"Good window. {rules['description']} Proceed with intention."
    elif total >= 35:
        window = "Neutral"
        advice = f"Neither favored nor blocked. Time is workable but not optimal."
    else:
        window = "Avoid"
        advice = f"Current energies work against this. Delay if possible."

    return {
        "action": action_key,
        "label": rules["label"],
        "icon": rules["icon"],
        "score": total,
        "window": window,
        "advice": advice,
        "dasha_note": dasha_note,
        "transit_notes": transit_notes[:3],
    }


def get_timing_advice(
    active_dasha: str,
    current_planets: Dict,
    nakshatra: str,
) -> Dict[str, Any]:
    """
    Return action-by-action timing scores for today and best weekday this week.
    active_dasha: e.g. "Venus-Saturn" — we use the Maha-Dasha lord.
    """
    md_lord = active_dasha.split("-")[0].strip() if active_dasha else "Sun"

    actions = [
        _score_action(k, md_lord, current_planets, nakshatra)
        for k in ACTION_RULES
    ]
    actions.sort(key=lambda x: x["score"], reverse=True)

    # Best day this week: base quality + dasha lord day bonus + nakshatra lord day bonus
    today = datetime.utcnow()
    lord_day = PLANET_DAY.get(md_lord, -1)
    nak_lord = NAK_LORD.get(nakshatra, "")
    nak_day  = PLANET_DAY.get(nak_lord, -1)
    week_days = []
    for i in range(7):
        d = today + timedelta(days=i)
        wd = d.weekday()
        q = WEEKDAY_Q[wd]
        if wd == lord_day: q += 2
        if wd == nak_day:  q += 2
        week_days.append({"date": d.strftime("%Y-%m-%d"), "day": WEEKDAY_NAME[wd], "quality": q})
    best_day = max(week_days, key=lambda x: x["quality"])

    # Overall window
    top_score = actions[0]["score"] if actions else 0
    if top_score >= 75:
        overall = "Power Window"
        overall_desc = f"{md_lord} Dasha is activating. Multiple high-value actions available now."
    elif top_score >= 55:
        overall = "Active Window"
        overall_desc = f"Selective execution is favorable. Focus on your top-rated action."
    else:
        overall = "Consolidation Phase"
        overall_desc = f"{md_lord} Dasha calls for patience and preparation, not major moves."

    return {
        "active_dasha": active_dasha,
        "dasha_lord": md_lord,
        "nakshatra": nakshatra,
        "overall_window": overall,
        "overall_description": overall_desc,
        "best_day_this_week": best_day,
        "actions": actions,
        "generated_at": today.strftime("%Y-%m-%d %H:%M UTC"),
    }
