"""
Tier 0 proof: the validator reproduces the real defect found in the
'Pranav_Singhal_Reading_Final.pdf' export — an ungrounded LLM claiming
"Jupiter — ruler of the 7th house" when, for an Aries lagna, Venus rules the
7th and Jupiter rules the 9th & 12th — while leaving the PDF's CORRECT claims
untouched (no false positives).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.reading.facts import build_fact_table, grounding_text
from src.reading.validator import validate_reading


# Pranav's chart per the PDF (Aries lagna; signs are all the validator needs).
CHART = {
    "lagna": {"sign": "Aries"},
    "planets": {
        "Jupiter": {"sign": "Aries", "is_retrograde": True},
        "Moon":    {"sign": "Cancer"},
        "Sun":     {"sign": "Leo"},
        "Venus":   {"sign": "Leo"},
        "Mercury": {"sign": "Leo"},
        "Mars":    {"sign": "Leo"},
        "Ketu":    {"sign": "Virgo"},
        "Saturn":  {"sign": "Scorpio"},
        "Rahu":    {"sign": "Pisces"},
    },
}


def _ft():
    return build_fact_table(CHART)


def test_house_lords_are_correct_for_aries():
    ft = _ft()
    # Aries lagna, whole-sign.
    assert ft["house_lords"][7] == "Venus"      # 7th = Libra = Venus
    assert ft["planets"]["Jupiter"]["rules_houses"] == [9, 12]
    assert ft["planets"]["Venus"]["rules_houses"] == [2, 7]
    assert ft["planets"]["Sun"]["rules_houses"] == [5]
    assert ft["planets"]["Sun"]["house"] == 5   # Leo from Aries
    assert ft["planets"]["Saturn"]["house"] == 8  # Scorpio from Aries


def test_catches_the_jupiter_seventh_house_hallucination():
    defect = ("Jupiter — ruler of the 7th house in a different reading context "
              "— as antardasha lord.")
    violations = validate_reading(defect, _ft())
    assert len(violations) == 1
    v = violations[0]
    assert v.kind == "lordship"
    assert v.planet == "Jupiter"
    assert v.claimed == 7
    assert v.expected == [9, 12]


def test_correct_claims_from_the_pdf_pass_clean():
    correct = (
        "Sun in Leo in the 5th is powerful. Sun as 5th lord sits in the 5th. "
        "Venus in the 5th stellium, ruling the 2nd house and the 7th house. "
        "Jupiter rules your 9th house and 12th house. "
        "Mars rules both the 1st house and the 8th house."
    )
    assert validate_reading(correct, _ft()) == []


def test_catches_wrong_placement_house_and_sign():
    text = "Saturn in the 5th house. Mars in Cancer."
    violations = validate_reading(text, _ft())
    kinds = {(v.kind, v.planet, v.claimed, tuple_or(v.expected)) for v in violations}
    assert ("placement_house", "Saturn", 5, 8) in kinds      # Saturn is actually H8
    assert ("placement_sign", "Mars", "Cancer", "Leo") in kinds  # Mars is actually Leo


def test_grounding_text_is_renderable():
    g = grounding_text(_ft())
    assert "Lagna (ascendant): Aries, ruled by Mars." in g
    assert "Jupiter: in Aries, house 1, rules house(s) 9, 12 (retrograde" in g


def tuple_or(x):
    return tuple(x) if isinstance(x, list) else x
