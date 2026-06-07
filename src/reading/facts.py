"""
Fact-table builder — the deterministic "truth" a reading is allowed to assert.

Consumes the payload already produced by /api/chart (engine + astro_tools) and
flattens it into a single canonical structure of structural facts: house
lordships, planet placements (sign + house), rulerships, retrograde state, and
the active dasha. This is the ONLY source the narrative layer may draw factual
claims from, and the exact reference the validator diffs against.

Whole-sign houses (engine uses swe houses 'W'), so a house's lord is simply the
lord of the sign that sits in it relative to the lagna. No cusp ambiguity.
"""
from typing import Dict, Any, List

from ..astro_tools import SIGNS, SIGN_IDX, SIGN_LORDS, OWN_SIGNS, _house

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

_NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]


def _nakshatra_of(longitude: float) -> str:
    return _NAKSHATRAS[int(longitude / (360 / 27)) % 27]


def _house_lords(lagna_sign: str) -> Dict[int, str]:
    """Map house number (1..12) -> ruling planet, whole-sign relative to lagna."""
    li = SIGN_IDX[lagna_sign]
    return {h: SIGN_LORDS[SIGNS[(li + h - 1) % 12]] for h in range(1, 13)}


def _active_dasha(dashas: List[Dict], today: str) -> Dict[str, Any]:
    """Return the currently running mahadasha + antardasha lords for `today` (YYYY-MM-DD)."""
    if not dashas:
        return {}
    md = next((d for d in dashas if d["start"] <= today <= d["end"]), dashas[0])
    bhuktis = md.get("bhuktis") or [{}]
    ad = next((b for b in bhuktis if b.get("start", "") <= today <= b.get("end", "")), bhuktis[0])
    return {
        "md_lord": md.get("lord"),
        "ad_lord": ad.get("lord"),
        "md_start": md.get("start"), "md_end": md.get("end"),
        "ad_start": ad.get("start"), "ad_end": ad.get("end"),
    }


def build_fact_table(chart: Dict[str, Any], today: str = "") -> Dict[str, Any]:
    """
    Flatten an /api/chart payload into the canonical fact-table.

    `chart` needs at least: lagna{sign}, planets{<Planet>{sign,longitude,is_retrograde}}.
    Optional: dashas (enables active-dasha facts). `today` is YYYY-MM-DD.
    """
    lagna_sign = chart["lagna"]["sign"]
    planets = chart["planets"]
    house_lords = _house_lords(lagna_sign)

    # Inverse map: planet -> [houses it rules]
    planet_rules: Dict[str, List[int]] = {p: [] for p in PLANETS}
    for h, lord in house_lords.items():
        planet_rules.setdefault(lord, []).append(h)

    planet_facts: Dict[str, Dict[str, Any]] = {}
    for p in PLANETS:
        if p not in planets:
            continue
        pd = planets[p]
        sign = pd["sign"]
        house = _house(sign, lagna_sign)
        planet_facts[p] = {
            "sign": sign,
            "house": house,
            "rules_houses": sorted(planet_rules.get(p, [])),
            "retrograde": bool(pd.get("is_retrograde", False)),
            "own_sign": sign in OWN_SIGNS.get(p, []),
            "nakshatra": _nakshatra_of(pd["longitude"]) if "longitude" in pd else None,
        }

    return {
        "lagna": {"sign": lagna_sign, "lord": SIGN_LORDS[lagna_sign]},
        "house_lords": house_lords,
        "planets": planet_facts,
        "dasha": _active_dasha(chart.get("dashas", []), today) if today else {},
        # Pass-through facts the deeper template sections consume. Kept as-is from
        # the chart payload so the template has a single grounding source.
        "dashas_full": chart.get("dashas", []),
        "yogas": chart.get("yogas", []),
        "divisional": chart.get("divisional_charts", {}),
        "karakas": chart.get("karakas", {}),  # filled once Jaimini computation lands
    }


def grounding_text(ft: Dict[str, Any]) -> str:
    """
    Render the fact-table as the deterministic fact-sheet handed to the LLM.

    This is the LLM's *only* permitted source of astrological facts. Phrased as
    flat declaratives so the model restyles rather than reasons.
    """
    lines: List[str] = []
    lines.append(f"Lagna (ascendant): {ft['lagna']['sign']}, ruled by {ft['lagna']['lord']}.")

    hl = ", ".join(f"{h}={lord}" for h, lord in sorted(ft["house_lords"].items()))
    lines.append(f"House lords (whole-sign): {hl}.")

    for p, f in ft["planets"].items():
        rules = ", ".join(map(str, f["rules_houses"])) or "none"
        extras = []
        if f["retrograde"]:
            extras.append("retrograde")
        if f["own_sign"]:
            extras.append("own sign")
        if f.get("nakshatra"):
            extras.append(f"nakshatra {f['nakshatra']}")
        tail = f" ({'; '.join(extras)})" if extras else ""
        lines.append(f"{p}: in {f['sign']}, house {f['house']}, rules house(s) {rules}{tail}.")

    d = ft.get("dasha") or {}
    if d.get("md_lord"):
        lines.append(
            f"Active period: {d['md_lord']} mahadasha "
            f"({d.get('md_start')}–{d.get('md_end')}), "
            f"{d['ad_lord']} antardasha ({d.get('ad_start')}–{d.get('ad_end')})."
        )
    return "\n".join(lines)
