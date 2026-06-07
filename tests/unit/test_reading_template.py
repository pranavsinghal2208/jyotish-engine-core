"""
Template-schema tests: the reading plan is well-formed, tier subsetting works,
per-section grounding pulls only that section's facts, and a section whose facts
aren't computed yet (karakas) is flagged has_data=False so the generator skips
it instead of letting the LLM invent content.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.reading.facts import build_fact_table
from src.reading.template import build_reading_plan, section_grounding, SECTIONS, MASS, DEEP


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
    "dashas": [
        {"lord": "Venus", "start": "2014-01-01", "end": "2034-01-01",
         "bhuktis": [{"lord": "Jupiter", "start": "2024-03-01", "end": "2026-11-01"}]},
    ],
    "yogas": [{"name": "Sun in own sign in own house"}],
    "divisional_charts": {"d9": {"lagna": "Pisces"}, "d10": {}},
    # karakas intentionally absent — not computed yet
}


def _ft():
    return build_fact_table(CHART, today="2026-06-07")


def test_mass_tier_is_a_strict_subset_of_deep():
    mass_ids = {p["section"].id for p in build_reading_plan(_ft(), MASS)}
    deep_ids = {p["section"].id for p in build_reading_plan(_ft(), DEEP)}
    assert mass_ids < deep_ids                 # strict subset
    assert "chart_table" not in mass_ids       # deep-only
    assert "planets" not in mass_ids           # deep-only
    assert "cover" in mass_ids and "now" in mass_ids and "final" in mass_ids


def test_plan_is_ordered_and_carries_budgets():
    plan = build_reading_plan(_ft(), DEEP)
    orders = [p["section"].order for p in plan]
    assert orders == sorted(orders)
    assert all(p["word_budget"] for p in plan)  # every deep section has a budget


def test_section_grounding_is_focused():
    ft = _ft()
    lum = next(s for s in SECTIONS if s.id == "luminaries")
    g = section_grounding(lum, ft)
    assert "Sun:" in g and "Moon:" in g
    assert "Saturn:" not in g                   # not requested by this section


def test_now_section_resolves_dynamic_dasha_lords():
    ft = _ft()
    now = next(s for s in SECTIONS if s.id == "now")
    g = section_grounding(now, ft)
    # md_lord=Venus, ad_lord=Jupiter for this chart/date
    assert "Active period: Venus mahadasha" in g
    assert "Venus:" in g and "Jupiter:" in g


def test_karakas_section_flagged_no_data_until_computed():
    plan = build_reading_plan(_ft(), DEEP)
    karakas = next(p for p in plan if p["section"].id == "karakas")
    assert karakas["has_data"] is False         # generator must skip, not hallucinate
