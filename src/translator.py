from typing import Dict, Any, List
from datetime import datetime

SIGN_THEMES = {
    "Aries":       {"theme": "New Beginnings",       "energy": "Courageous Action",   "daily": "Something in you is ready to leap. The hesitation you feel is not wisdom — it is old habit. One bold move today, however small, sets the direction for the next 30 days."},
    "Taurus":      {"theme": "Building & Grounding", "energy": "Steady & Patient",    "daily": "Your power today is in the unhurried. Slow down. The thing you build carefully now will still be standing when faster things have crumbled. Tend to what truly nourishes you."},
    "Gemini":      {"theme": "Connecting & Curious", "energy": "Mental Agility",      "daily": "Your mind is running fast and picking up signals from everywhere. Follow the thread that keeps pulling your attention. One conversation today could change the shape of next month."},
    "Cancer":      {"theme": "Feeling & Protecting", "energy": "Deep Intuition",      "daily": "Something you sense but cannot yet articulate is correct. Trust the feeling before the explanation arrives. The people and spaces that feel safe to you are worth protecting today."},
    "Leo":         {"theme": "Heart & Leadership",   "energy": "Warm Confidence",     "daily": "You are allowed to take up space today. Your generosity, your warmth, your willingness to be seen — these are gifts, not liabilities. Let someone see what you are actually capable of."},
    "Virgo":       {"theme": "Attention & Care",     "energy": "Quiet Precision",     "daily": "The detail you are tempted to skip is the one that matters. Give something in your life the full care it deserves today. Mastery is not grand — it is this small, deliberate act, repeated."},
    "Libra":       {"theme": "Balance & Harmony",    "energy": "Graceful Clarity",    "daily": "The situation that has felt unresolved is ready for a fair decision. You do not have to choose sides — you have to choose what is true. Honest, gentle clarity today prevents a harder conversation later."},
    "Scorpio":     {"theme": "Depth & Truth",        "energy": "Inner Knowing",       "daily": "You can feel something that others are not saying. You are probably right. Go deeper rather than wider today — the answer is underneath the surface, not on it."},
    "Sagittarius": {"theme": "Widening Your World",  "energy": "Expansive Optimism",  "daily": "Something larger than your current situation is trying to reach you. Make room for it. Say yes to the thing that feels slightly too big, too far, or too hopeful. That is the one."},
    "Capricorn":   {"theme": "Structure & Patience", "energy": "Calm Endurance",      "daily": "The long work is paying off, even when you cannot see it. Stay the course. What you are building is real and it is growing. One more day of showing up is enough."},
    "Aquarius":    {"theme": "Breaking New Ground",  "energy": "Original Thinking",   "daily": "The idea that seems unconventional is worth exploring. You are thinking ahead of where most people are — do not wait for permission to say so. Share the original thought."},
    "Pisces":      {"theme": "Dreaming & Sensing",   "energy": "Intuitive Flow",      "daily": "The rational plan matters less today than how you feel about it. Let your imagination run. The insight you are looking for will not arrive through logic — it will come through stillness."}
}

SIGN_NATAL = {
    "Aries":       "You came here to initiate. There is a fire in you that wants to move first, break ground, and lead the charge — even when no one asked you to.",
    "Taurus":      "You came here to build. Your gifts are patience, loyalty, and the rare ability to create things that last long after the rush has faded.",
    "Gemini":      "You came here to connect. Your mind bridges worlds, people, and ideas — you are the living conversation between things that did not know they were related.",
    "Cancer":      "You came here to protect. You sense the emotional weather in any room and your deepest instinct is to make people feel safe enough to be themselves.",
    "Leo":         "You came here to lead with your heart. Your warmth, generosity, and refusal to hide are not indulgences — they are your contribution to the world.",
    "Virgo":       "You came here to perfect. You notice the gap between what is and what could be — and you close it with work, care, and quietly extraordinary precision.",
    "Libra":       "You came here to harmonise. You carry an instinct for fairness that most people have to learn. Your gift is making the complex feel balanced and the broken feel whole.",
    "Scorpio":     "You came here to transform. You are unafraid of what is real, what is hidden, or what must be released. You go where others will not — and bring back what matters.",
    "Sagittarius": "You came here to search. Your hunger for truth, meaning, and the widest possible view is not restlessness — it is your compass pointing toward the work only you can do.",
    "Capricorn":   "You came here to endure. Your patience is not passive — it is the deep, structural patience of someone who is building something worth outlasting them.",
    "Aquarius":    "You came here to see ahead. Your sense that the world could be radically different is not naive — it is the perception that makes genuine change possible.",
    "Pisces":      "You came here to feel what others cannot. Your sensitivity is not weakness — it is the instrument through which you perceive what logic alone will always miss."
}

PLANET_ARCHETYPES = {
    "Sun":     {"label": "Executive Intent",           "focus": "Identity & Leadership"},
    "Moon":    {"label": "Intuitive Intelligence",     "focus": "Mindset & Perception"},
    "Mars":    {"label": "Execution Energy",           "focus": "Action & Momentum"},
    "Mercury": {"label": "Strategic Communication",    "focus": "Logic & Systems"},
    "Jupiter": {"label": "Expansion Strategy",         "focus": "Growth & Abundance"},
    "Venus":   {"label": "Value & Relationships",      "focus": "Partnerships & Assets"},
    "Saturn":  {"label": "Structural Integrity",       "focus": "Discipline & Legacy"},
    "Rahu":    {"label": "Aggressive Innovation",      "focus": "Ambition & Change"},
    "Ketu":    {"label": "Domain Mastery",             "focus": "Refinement & Depth"}
}

DASHA_THEMES = {
    "Sun":     {"life": "A period when your sense of self comes to the surface. Your presence, your purpose, and how you want to be known in the world — these are the living questions of this chapter.", "focus": "Purpose, presence & identity"},
    "Moon":    {"life": "A deeply internal chapter. Your emotional world and the environments you inhabit become the primary teachers. What nourishes you quietly becomes more important than what impresses others.", "focus": "Intuition, home & emotional truth"},
    "Mars":    {"life": "A chapter of raw energy and forward motion. The urge to act, to build, to fight for what matters is at its most intense. This period favours those who move before they feel fully ready.", "focus": "Courage, action & momentum"},
    "Mercury": {"life": "Your mind opens. This is a chapter of learning, communicating, and connecting — a time when words and ideas become the most powerful tools you carry.", "focus": "Learning, expression & connection"},
    "Jupiter": {"life": "A chapter of genuine good fortune and expansion. Doors open that you did not knock on. Mentors appear. The invitation of this period is to say yes to a life that is larger than the one you have been living.", "focus": "Growth, wisdom & good fortune"},
    "Venus":   {"life": "A chapter devoted to beauty, love, and the things that make life worth living. Relationships deepen, creative instincts sharpen, and the quality of daily experience becomes as important as achievement.", "focus": "Love, beauty & meaningful connection"},
    "Saturn":  {"life": "A chapter of serious, patient work. What you build here is real and lasting. What you avoid will surface. Show up consistently, even when nothing feels like it is moving.", "focus": "Patience, integrity & lasting work"},
    "Rahu":    {"life": "A chapter of intense ambition and rapid change. Rahu pulls you toward unfamiliar territory — new places, new people, new versions of yourself. The hunger is real, but it needs a clear direction.", "focus": "Ambition, change & new horizons"},
    "Ketu":    {"life": "A chapter of letting go and going deep. The outer world holds less pull than usual — that is the invitation. This period rewards those who turn inward, master what they already carry, and release what no longer fits.", "focus": "Depth, release & inner mastery"}
}

AD_STRATEGIES = {
    "Sun":     "Step into one leadership role you have been circling around. Your presence is unusually clear right now — use it.",
    "Moon":    "Trust the gut feeling that keeps arriving before the explanation does. Your intuition is the most reliable instrument in this window.",
    "Mars":    "Take the action you have been calculating but not executing. Movement matters more than perfection here.",
    "Mercury": "Write it, send it, document it. This is the window when communication lands clearly and agreements hold.",
    "Jupiter": "Say yes to the thing that stretches your current capacity. This sub-cycle opens doors that close again quickly.",
    "Venus":   "Invest in one relationship deliberately — a conversation with no agenda. Quality of connection is what this window rewards.",
    "Saturn":  "Do the unglamorous foundational work you have been postponing. Showing up consistently in small things is what this period converts into something lasting.",
    "Rahu":    "Move into territory that makes you slightly uncomfortable. The unfamiliar path is the high-yield path in this sub-cycle.",
    "Ketu":    "Go narrow and deep. Cut one commitment that no longer carries real meaning, and pour that energy into your most essential work."
}

DAILY_ACTIONS = {
    "Aries":       ["Take the bold action you have been postponing — today is the right day", "Lead one conversation that needs someone to go first", "Notice where you are overthinking and choose to move instead"],
    "Taurus":      ["Tend to one thing with full care and no rushing", "Invest time in something that will still matter in a year", "Let yourself enjoy a moment of real comfort — it restores your energy"],
    "Gemini":      ["Reach out to someone who makes you think differently", "Write down the idea that keeps returning — it deserves attention", "Learn one thing that connects two worlds you care about"],
    "Cancer":      ["Check in on someone you have been quietly thinking about", "Protect the space and the people that genuinely nourish you", "Trust the feeling that arrived before you could explain it"],
    "Leo":         ["Say the true thing you have been softening for others' comfort", "Acknowledge your own effort — you have been carrying more than you show", "Let one person fully see what you are working on"],
    "Virgo":       ["Give one task the full care it deserves — not all tasks, just one", "Release the standard that has been exhausting you without benefiting anyone", "Notice what is quietly, reliably working — and honour it"],
    "Libra":       ["Make the decision you have been balancing — you already know the answer", "Reach out to repair one relationship that genuinely matters to you", "Ask for what you actually need, not the easier version of it"],
    "Scorpio":     ["Investigate the thing no one else wants to look at", "Let go of one grievance that has been costing you more than it is worth", "Do the deep work — the surface task can wait"],
    "Sagittarius": ["Say yes to the thing that feels slightly too large or too far", "Spend time with someone who operates at a scale you are still growing into", "Let your biggest question breathe — do not try to resolve it today, just hold it"],
    "Capricorn":   ["Put 90 minutes into the work that most needs your full presence", "Honour one commitment you made to yourself, not just to others", "Acknowledge progress — the mountain is moving even when it does not feel like it"],
    "Aquarius":    ["Share the unconventional idea — do not wait for permission", "Connect with someone who thinks in a way that surprises you", "Give yourself space to think freely without solving for anyone else's needs"],
    "Pisces":      ["Create something — even small — without needing a practical reason", "Spend 20 minutes in real quiet to let the deeper signal come through", "Trust the intuition that has been arriving repeatedly — it has something to say"]
}



def detect_stellium(planets: Dict[str, Any]) -> str:
    sign_planets: Dict[str, List[str]] = {}
    for name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if name in planets:
            sign = planets[name]["sign"]
            sign_planets.setdefault(sign, []).append(name)

    for sign, group in sign_planets.items():
        if len(group) >= 3:
            if len(group) == 2:
                pl_str = " and ".join(group)
            else:
                pl_str = ", ".join(group[:-1]) + " and " + group[-1]
            return f"{pl_str} are all placed in {sign} — a rare and powerful stellium. This concentrates extraordinary energy in {sign}'s domain: creativity, leadership, and bold self-expression."
    return ""


def get_retrograde_note(transit_planets: Dict[str, Any]) -> str:
    retro = [n for n in ["Mercury", "Mars", "Jupiter", "Venus", "Saturn"]
             if transit_planets.get(n, {}).get("is_retrograde")]
    if not retro:
        return "All major planets are direct today — a clean window for forward momentum. Decisions made now tend to stick."
    if "Mercury" in retro:
        return "Mercury is retrograde right now. This is a natural pause built into the cosmic rhythm: review, revise, and reconnect before launching anything new. Contracts and new agreements are better finalised after Mercury goes direct."
    names = " and ".join(retro)
    verb = "is" if len(retro) == 1 else "are"
    return f"{names} {verb} retrograde now — internalised energy. Use this period for reflection and refinement rather than aggressive expansion. The ground is being prepared."


def generate_directive(md_lord: str, ad_lord: str, transit_planets: Dict[str, Any]) -> str:
    ad_strategy = AD_STRATEGIES.get(ad_lord, "")
    retro_note  = get_retrograde_note(transit_planets)
    all_direct  = "All major planets are direct" in retro_note

    parts = []
    if md_lord and ad_lord and ad_strategy:
        # Lead with the specific dasha instruction
        parts.append(
            f"{md_lord} Maha-Dasha · {ad_lord} Bhukti opens a specific lane: "
            f"{ad_strategy[0].lower() + ad_strategy[1:]}"
        )
    # Add transit colour — only the retrograde warning if relevant, skip the generic direct note
    if not all_direct:
        parts.append(retro_note)
    elif parts:
        parts.append("All major planets are direct today — clean forward momentum.")

    return " ".join(parts) if parts else retro_note


def generate_coach_insights(natal_planets: Dict[str, Any], lagna: Dict[str, Any],
                             transit_planets: Dict[str, Any] = None,
                             md_lord: str = None, ad_lord: str = None) -> Dict[str, Any]:
    if transit_planets is None:
        transit_planets = natal_planets

    transit_moon_sign = transit_planets["Moon"]["sign"]
    moon_theme = SIGN_THEMES[transit_moon_sign]

    sun_sign = natal_planets["Sun"]["sign"]
    lagna_sign = lagna["sign"]
    natal_moon_sign = natal_planets["Moon"]["sign"]

    stellium_note = detect_stellium(natal_planets)

    superpowers = [
        {
            "title": f"Sun in {sun_sign} — Your Core Identity",
            "description": SIGN_NATAL[sun_sign]
        },
        {
            "title": f"{lagna_sign} Rising — How the World Sees You",
            "description": SIGN_NATAL[lagna_sign]
        }
    ]

    if stellium_note:
        superpowers.append({
            "title": "Rare Planetary Concentration",
            "description": stellium_note
        })

    directive = generate_directive(md_lord, ad_lord, transit_planets)

    return {
        "daily_theme": moon_theme["theme"],
        "energy_signature": f"Moon in {transit_moon_sign} today · {moon_theme['energy']}",
        "uplift_narrative": moon_theme["daily"],
        "superpowers": superpowers,
        "operational_pointer": directive,
        "daily_actions": DAILY_ACTIONS.get(transit_moon_sign, []),
        "natal_moon_sign": natal_moon_sign
    }


def generate_business_pulse(dashas: List[Dict], current_date: datetime) -> Dict[str, Any]:
    date_str = current_date.strftime("%Y-%m-%d")

    active_md = next((d for d in dashas if d["start"] <= date_str <= d["end"]), dashas[0])
    active_ad = next((b for b in active_md["bhuktis"] if b["start"] <= date_str <= b["end"]),
                     active_md["bhuktis"][0])

    md_lord = active_md["lord"]
    ad_lord = active_ad["lord"]

    md_theme = DASHA_THEMES.get(md_lord, {"life": "", "focus": ""})
    ad_strategy = AD_STRATEGIES.get(ad_lord, "")

    strategy = f"{md_theme['life']} Right now, the {ad_lord} sub-cycle sharpens the focus: {ad_strategy}"

    return {
        "active_dasha": f"{md_lord}-{ad_lord}",
        "display_dasha": f"{md_lord} Maha-Dasha · {ad_lord} Bhukti",
        "focus": md_theme["focus"],
        "target_kpi": f"{md_lord} · {ad_lord} sub-cycle",
        "strategy": strategy
    }



def get_cosmic_schedule_advice(events: List[Dict], transit_planets: Dict[str, Any], active_dasha_lord: str = "") -> List[Dict]:
    advice_list = []
    mercury_retro = transit_planets.get("Mercury", {}).get("is_retrograde", False)
    mars_in_fire = transit_planets.get("Mars", {}).get("sign") in ["Leo", "Aries", "Sagittarius"]
    
    # Dasha-specific high-stakes mapping
    dasha_risk_map = {
        "Saturn": ["negotiation", "contract", "legal", "closure"],
        "Rahu":   ["innovation", "new venture", "tech", "pitch"],
        "Mars":   ["execution", "action", "launch", "competition"],
        "Mercury": ["sales", "communication", "writing", "agreement"]
    }

    for event in events:
        summary = event.get("summary", "")
        is_high_stakes = event.get("is_high_stakes", False)
        summary_lower = summary.lower()

        # 1. Mercury Retrograde Check
        if mercury_retro and any(kw in summary_lower for kw in ["negotiation", "contract", "legal", "sign"]):
            advice_list.append({
                "event": summary,
                "risk": "High",
                "reason": "Mercury retrograde increases the risk of miscommunication and missed details in agreements.",
                "action": "Delay final signatures if possible. If you must proceed, read every clause twice and confirm all verbal agreements in writing."
            })
            continue

        # 2. Dasha-Event Synergy
        relevant_keywords = dasha_risk_map.get(active_dasha_lord, [])
        synergy_found = any(kw in summary_lower for kw in relevant_keywords)

        if synergy_found:
            advice_list.append({
                "event": summary,
                "risk": "Low",
                "reason": f"Active {active_dasha_lord} Dasha creates a natural resonance for {active_dasha_lord.lower()}-related activities.",
                "action": f"This event aligns with your current life chapter focus. Lean into {active_dasha_lord.lower()} energy: precision and long-term strategy." if active_dasha_lord == "Saturn" else "Lead with confidence; the cosmic timing is in your favour."
            })
            continue

        # 3. Specific Transit Win
        if "pitch" in summary_lower or "presentation" in summary_lower:
            if mars_in_fire:
                advice_list.append({
                    "event": summary,
                    "risk": "Low",
                    "reason": "Mars in a fire sign gives you extra conviction, presence, and decisive energy right now.",
                    "action": "Lead with confidence. Go in with your strongest point first. Decisive, energetic delivery will carry the room."
                })
                continue

        # 4. Fallback for general high-stakes
        if is_high_stakes:
            advice_list.append({
                "event": summary,
                "risk": "Moderate",
                "reason": "High-stakes moment during a planetary transition period.",
                "action": "Preparation and presence are your greatest assets. Be clear, calm, and fully ready."
            })

    return advice_list
