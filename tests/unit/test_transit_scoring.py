import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.timing_advisor import get_timing_advice, _score_action

def test_house_aware_transit_scoring():
    active_dasha = "Venus-Saturn"
    current_planets = {
        "Venus": {"sign": "Scorpio"}
    }
    nakshatra = "Rohini"
    personal_day = 1

    # Case 1: Venus is in 2H
    planet_house_2h = {"Venus": 2}
    advice_2h = get_timing_advice(
        active_dasha, current_planets, nakshatra, personal_day, planet_house=planet_house_2h
    )

    # Case 2: Venus is in 8H
    planet_house_8h = {"Venus": 8}
    advice_8h = get_timing_advice(
        active_dasha, current_planets, nakshatra, personal_day, planet_house=planet_house_8h
    )

    # Let's verify scores for "Sign" action (which has Venus as a favorable planet)
    action_2h = next(a for a in advice_2h["actions"] if a["action"] == "Sign")
    action_8h = next(a for a in advice_8h["actions"] if a["action"] == "Sign")

    print(f"Venus 2H 'Sign' score: {action_2h['score']}")
    print(f"Venus 8H 'Sign' score: {action_8h['score']}")
    print(f"Venus 2H transit notes: {action_2h['transit_notes']}")
    print(f"Venus 8H transit notes: {action_8h['transit_notes']}")

    # Venus 2H should have higher score than Venus 8H (specifically +4 points higher because 2H gets +5 and 8H gets +1)
    assert action_2h["score"] == action_8h["score"] + 4
    
    # Venus 2H should list Venus as favorable, Venus 8H should list Venus as caution
    assert "Venus favorable" in action_2h["transit_notes"]
    assert "Venus caution" in action_8h["transit_notes"]
