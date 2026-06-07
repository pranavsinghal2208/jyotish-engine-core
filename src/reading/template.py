"""
Reading template — the section schema a generator fills.

Modelled on the structure of a strong long-form reading, but built as DATA, not
prose: each Section declares (1) which fact-table fields it grounds on, (2) the
cross-factor synthesis it must perform — the craft the current translator.py
lacks — and (3) the author brief (voice, length). The generator walks SECTIONS,
builds a focused per-section grounding string, hands it to the LLM with the
brief, then runs the validator on the result.

Two audience tiers, deliberately:
  MASS  — short, jargon-free, "millions who don't know what Mahadasha means"
          (the Pattern-app positioning). A subset of sections, tight word budgets.
  DEEP  — the premium long-form deep-dive (what the reference PDF is).
Keeping these separate stops the mass product from drifting into a 10-page essay.

This module is pure/deterministic. No LLM, no I/O.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Set

from .facts import grounding_text  # reused for whole-chart fallback

MASS = "mass"
DEEP = "deep"


@dataclass
class Section:
    id: str
    title: str
    order: int
    tiers: Set[str]                 # which audience tiers include this section
    facts: List[str]                # fact selectors this section grounds on (see _resolve)
    synthesis: str                  # the cross-factor logic the author/LLM must apply
    brief: str                      # voice + format instruction
    word_budget: Dict[str, int] = field(default_factory=dict)  # tier -> max words


# ─── The section spine ────────────────────────────────────────────────────────
# Selectors understood by _resolve(): "lagna", "house_lords", "yogas",
# "dashas_full", "dasha_active", "divisional:d9", "divisional:d10", "karakas",
# and "planets:<spec>" where spec is "all", a comma list ("Sun,Moon"), or a
# dynamic role: "lagna_lord", "md_lord", "ad_lord", "tenth_lord".

SECTIONS: List[Section] = [
    Section(
        id="cover", title="Cover & Frame", order=0, tiers={MASS, DEEP},
        facts=["lagna", "dasha_active"],
        synthesis="One-line identity: ascendant nature + the single current life-phase theme (active mahadasha).",
        brief="Name, birth data, a one-line summary, and a 1-2 sentence plain-language frame. No jargon unexplained.",
        word_budget={MASS: 60, DEEP: 120},
    ),
    Section(
        id="chart_table", title="Your Birth Chart", order=1, tiers={DEEP},
        facts=["planets:all", "house_lords"],
        synthesis="Flag standout patterns: any house with 3+ planets (stellium), retrograde planets, own-sign/exalted placements.",
        brief="Render the planet table (Planet | Sign & House | Nakshatra | Notes), then one footnote on the chart's most striking pattern.",
        word_budget={DEEP: 120},
    ),
    Section(
        id="lagna", title="Foundation — Ascendant & Its Lord", order=2, tiers={MASS, DEEP},
        facts=["lagna", "planets:lagna_lord"],
        synthesis="Combine ascendant temperament + where the lagna lord sits (house/sign) + its nakshatra. Name the core tension this creates.",
        brief="Who they are on first contact, and the central tension to calibrate over a lifetime. Plain language.",
        word_budget={MASS: 130, DEEP: 320},
    ),
    Section(
        id="signature", title="The Defining Signature", order=3, tiers={MASS, DEEP},
        facts=["planets:all", "yogas"],
        synthesis="Rank and pick the SINGLE most prominent feature (largest stellium / strongest yoga / exalted lord) and lead with it. Explain why it dominates the chart.",
        brief="One standout signature, stated boldly, with its practical consequence. This is the hook.",
        word_budget={MASS: 120, DEEP: 300},
    ),
    Section(
        id="luminaries", title="Sun & Moon — Soul and Mind", order=4, tiers={MASS, DEEP},
        facts=["planets:Sun,Moon"],
        synthesis="Sun (sign+house+nakshatra) = outer identity/will; Moon = inner emotional processing. Contrast them; include each one's shadow side.",
        brief="Two short sub-sections. Balanced — strength and shadow, never flattery only.",
        word_budget={MASS: 150, DEEP: 400},
    ),
    Section(
        id="planets", title="The Working Planets", order=5, tiers={DEEP},
        facts=["planets:Mars,Mercury,Jupiter,Venus,Saturn,Rahu,Ketu"],
        synthesis="Read each planet through the houses it RULES landing in the house it SITS in. One shadow line each. This dual-rulership lens is the synthesis the lookup templates miss.",
        brief="Per-planet, compact. Lead with the rulership→placement link, then one lived consequence.",
        word_budget={DEEP: 500},
    ),
    Section(
        id="yogas", title="Patterns That Fire", order=6, tiers={MASS, DEEP},
        facts=["yogas"],
        synthesis="Only yogas that actually form in this chart. Translate each into a plain-language life effect — no Sanskrit left unexplained.",
        brief="MASS: top 1-2 only. DEEP: all. Name → what it means in real life.",
        word_budget={MASS: 90, DEEP: 280},
    ),
    Section(
        id="timeline", title="Your Timeline", order=7, tiers={MASS, DEEP},
        facts=["dashas_full", "dasha_active"],
        synthesis="Map each mahadasha to a life theme; mark the current one; give the past period's meaning so the present has context.",
        brief="A compact period table + short prose. Frame dashas as 'which quality is foregrounded now', not jargon.",
        word_budget={MASS: 120, DEEP: 320},
    ),
    Section(
        id="now", title="Right Now", order=8, tiers={MASS, DEEP},
        facts=["dasha_active", "planets:md_lord", "planets:ad_lord"],
        synthesis="Combine the active mahadasha lord + antardasha lord placements into what THIS window emphasises, then convert to a concrete 'what this period is asking of you'.",
        brief="The most actionable section. Specific and forward-looking, not fatalistic.",
        word_budget={MASS: 130, DEEP: 350},
    ),
    Section(
        id="d9", title="The Deeper Self (Navamsha)", order=9, tiers={DEEP},
        facts=["divisional:d9", "lagna"],
        synthesis="Contrast the navamsha lagna with the natal lagna — the inner self vs the outer presentation.",
        brief="What changes when circumstances strip away. Inner vs outer.",
        word_budget={DEEP: 280},
    ),
    Section(
        id="d10", title="Career & Public Life (Dashamsha)", order=10, tiers={DEEP},
        facts=["divisional:d10", "planets:tenth_lord"],
        synthesis="Career signature from the 10th-lord placement; if the 10th lord sits in a dusthana (6/8/12), call out a non-linear/disruptive career pattern.",
        brief="Career direction and the shape of the professional path.",
        word_budget={DEEP: 280},
    ),
    Section(
        id="karakas", title="Jaimini Karakas", order=11, tiers={DEEP},
        facts=["karakas"],
        synthesis="Atmakaraka (highest-degree planet) = soul aim; Amatyakaraka = career vehicle. State the life purpose they point to together.",
        brief="REQUIRES Jaimini karaka computation (not yet in engine — pending option A). Skip gracefully until karakas are populated.",
        word_budget={DEEP: 220},
    ),
    Section(
        id="final", title="A Final Note", order=12, tiers={MASS, DEEP},
        facts=["lagna", "dasha_active"],
        synthesis="Weave the 2-3 dominant threads (signature + current phase + core tension) into a short, forward-looking close.",
        brief="Synthesis, not new facts. Warm, honest, brief.",
        word_budget={MASS: 80, DEEP: 200},
    ),
]


# ─── Per-section grounding extraction ─────────────────────────────────────────

def _planet_line(name: str, f: Dict[str, Any]) -> str:
    rules = ", ".join(map(str, f.get("rules_houses", []))) or "none"
    extras = []
    if f.get("retrograde"):
        extras.append("retrograde")
    if f.get("own_sign"):
        extras.append("own sign")
    if f.get("nakshatra"):
        extras.append(f"nakshatra {f['nakshatra']}")
    tail = f" ({'; '.join(extras)})" if extras else ""
    return f"{name}: in {f['sign']}, house {f['house']}, rules house(s) {rules}{tail}."


def _resolve_planet_names(spec: str, ft: Dict[str, Any]) -> List[str]:
    if spec == "all":
        return list(ft.get("planets", {}).keys())
    out: List[str] = []
    for tok in spec.split(","):
        tok = tok.strip()
        if tok == "lagna_lord":
            out.append(ft["lagna"]["lord"])
        elif tok == "md_lord":
            out.append((ft.get("dasha") or {}).get("md_lord", ""))
        elif tok == "ad_lord":
            out.append((ft.get("dasha") or {}).get("ad_lord", ""))
        elif tok == "tenth_lord":
            out.append(ft.get("house_lords", {}).get(10, ""))
        else:
            out.append(tok)
    # de-dup, drop empties / planets absent from the fact-table
    seen, res = set(), []
    for n in out:
        if n and n in ft.get("planets", {}) and n not in seen:
            seen.add(n)
            res.append(n)
    return res


def _resolve(selector: str, ft: Dict[str, Any]) -> str:
    """Render one fact selector into a grounding line/block, or '' if no data."""
    if selector == "lagna":
        return f"Lagna: {ft['lagna']['sign']}, ruled by {ft['lagna']['lord']}."
    if selector == "house_lords":
        hl = ", ".join(f"{h}={l}" for h, l in sorted(ft.get("house_lords", {}).items()))
        return f"House lords (whole-sign): {hl}." if hl else ""
    if selector == "dasha_active":
        d = ft.get("dasha") or {}
        if not d.get("md_lord"):
            return ""
        return (f"Active period: {d['md_lord']} mahadasha ({d.get('md_start')}–{d.get('md_end')}), "
                f"{d.get('ad_lord')} antardasha ({d.get('ad_start')}–{d.get('ad_end')}).")
    if selector == "dashas_full":
        rows = ft.get("dashas_full") or []
        if not rows:
            return ""
        line = "; ".join(f"{r['lord']} {r['start']}→{r['end']}" for r in rows)
        return f"Mahadasha timeline: {line}."
    if selector == "yogas":
        ys = ft.get("yogas") or []
        if not ys:
            return ""
        names = "; ".join(y.get("name", str(y)) if isinstance(y, dict) else str(y) for y in ys)
        return f"Yogas present: {names}."
    if selector == "karakas":
        k = ft.get("karakas") or {}
        if not k:
            return ""  # not computed yet
        return "Karakas: " + ", ".join(f"{role}={planet}" for role, planet in k.items()) + "."
    if selector.startswith("divisional:"):
        key = selector.split(":", 1)[1]
        dv = (ft.get("divisional") or {}).get(key)
        return f"{key.upper()}: {dv}." if dv else ""
    if selector.startswith("planets:"):
        names = _resolve_planet_names(selector.split(":", 1)[1], ft)
        lines = [_planet_line(n, ft["planets"][n]) for n in names]
        return "\n".join(lines)
    return ""


def section_grounding(section: Section, ft: Dict[str, Any]) -> str:
    """Focused grounding string for one section — only the facts it declared."""
    blocks = [b for b in (_resolve(sel, ft) for sel in section.facts) if b]
    return "\n".join(blocks)


def build_reading_plan(ft: Dict[str, Any], tier: str = DEEP) -> List[Dict[str, Any]]:
    """
    Ordered, generator-ready plan for the given tier. Each item:
      {section, grounding, has_data}
    `has_data=False` means the section's facts aren't available yet (e.g. karakas)
    — the generator should skip it rather than let the LLM invent the content.
    """
    plan: List[Dict[str, Any]] = []
    for s in sorted(SECTIONS, key=lambda x: x.order):
        if tier not in s.tiers:
            continue
        grounding = section_grounding(s, ft)
        plan.append({
            "section": s,
            "grounding": grounding,
            "has_data": bool(grounding),
            "word_budget": s.word_budget.get(tier),
        })
    return plan
