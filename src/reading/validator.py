"""
Reading validator — the backstop that catches factual drift in generated prose.

In the hybrid pipeline the LLM only restyles facts it was handed, but "only"
is a hope, not a guarantee. This module re-reads the generated text, extracts
the structural claims it actually makes (house lordships, planet placements),
and diffs each against the deterministic fact-table. Any contradiction is a
Violation — caught before the PDF ships.

Scope is deliberately narrow: the high-frequency, high-trust-damage claim types
that an ungrounded model gets wrong (e.g. asserting a planet rules a house it
does not). It is a guardrail, not a full NLP parser — it errs toward silence
over false positives, so a clean reading never gets blocked spuriously.
"""
import re
from dataclasses import dataclass
from typing import Dict, Any, List

_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
_SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
          "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

_P = "|".join(_PLANETS)
_SG = "|".join(_SIGNS)
_ORD = r"(\d{1,2})(?:st|nd|rd|th)"

# Lordship claims: "<P> ... ruler/lord of the Nth house" / "<P> as Nth lord" /
# "<P> rules/ruling [the|your] Nth house". Window-limited so a far-away planet
# is not wrongly tied to a lordship phrase.
_LORD_PATTERNS = [
    re.compile(rf"\b({_P})\b[^.]{{0,60}}?\b(?:ruler|lord)\s+of\s+(?:the\s+|your\s+)?{_ORD}\s+house", re.I),
    re.compile(rf"\b({_P})\b[^.]{{0,50}}?\brul(?:es?|ing)\s+(?:the\s+|your\s+)?{_ORD}\s+house", re.I),
    re.compile(rf"\b({_P})\b[^.]{{0,40}}?\bas\s+(?:the\s+|your\s+)?{_ORD}\s+lord\b", re.I),
]
# Placement claims.
_HOUSE_PLACE = re.compile(rf"\b({_P})\b\s+in\s+(?:the\s+)?{_ORD}\s+house", re.I)
_SIGN_PLACE = re.compile(rf"\b({_P})\b\s+in\s+({_SG})\b", re.I)


@dataclass
class Violation:
    kind: str          # "lordship" | "placement_house" | "placement_sign"
    planet: str
    claimed: Any       # house number or sign the text asserted
    expected: Any      # what the fact-table says
    snippet: str       # the offending text, trimmed

    def __str__(self) -> str:
        return f"[{self.kind}] {self.planet}: text says {self.claimed!r}, chart says {self.expected!r} — “{self.snippet}”"


def _norm(p: str) -> str:
    return p.capitalize()


def _snip(text: str, start: int, end: int, pad: int = 24) -> str:
    s = text[max(0, start - pad):min(len(text), end + pad)].strip()
    return re.sub(r"\s+", " ", s)


def validate_reading(text: str, ft: Dict[str, Any]) -> List[Violation]:
    """Return every structural claim in `text` that contradicts fact-table `ft`."""
    out: List[Violation] = []
    seen = set()
    planets = ft.get("planets", {})

    def add(v: Violation):
        key = (v.kind, v.planet, str(v.claimed))
        if key not in seen:
            seen.add(key)
            out.append(v)

    # Lordship claims
    for pat in _LORD_PATTERNS:
        for m in pat.finditer(text):
            planet = _norm(m.group(1))
            claimed_house = int(m.group(2))
            expected = planets.get(planet, {}).get("rules_houses")
            if expected is not None and claimed_house not in expected:
                add(Violation("lordship", planet, claimed_house, expected,
                              _snip(text, m.start(), m.end())))

    # Placement — house
    for m in _HOUSE_PLACE.finditer(text):
        planet = _norm(m.group(1))
        claimed_house = int(m.group(2))
        expected = planets.get(planet, {}).get("house")
        if expected is not None and claimed_house != expected:
            add(Violation("placement_house", planet, claimed_house, expected,
                          _snip(text, m.start(), m.end())))

    # Placement — sign
    for m in _SIGN_PLACE.finditer(text):
        planet = _norm(m.group(1))
        claimed_sign = m.group(2).capitalize()
        expected = planets.get(planet, {}).get("sign")
        if expected is not None and claimed_sign != expected:
            add(Violation("placement_sign", planet, claimed_sign, expected,
                          _snip(text, m.start(), m.end())))

    return out
