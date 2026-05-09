from ..core.context import engine
from datetime import datetime

def get_live_transits(context):
    """Calculates a high-precision Live Energy Score (The Pulse)."""
    state = context.get_state()
    if not state: return None
    
    now_jd = state["jd_now"]
    now_planets = engine.get_planetary_positions(now_jd)
    natal_planets = state["planets_birth"]
    
    # 1. Calculation: Transit-to-Natal Pulse
    # We look for "Trines" (120 deg) and "Conjunctions" (0 deg) with Natal Sun/Moon/Jupiter
    score = 50 # Baseline
    active_vibe = "Neutral"
    highlights = []
    
    # Example Logic: Current Moon relationship to Natal Moon
    diff = abs(now_planets["Moon"]["longitude"] - natal_planets["Moon"]["longitude"]) % 360
    if diff < 10 or diff > 350:
        score += 20
        active_vibe = "High Alignment"
        highlights.append("Lunar Return: Emotional clarity is at a monthly peak.")
    elif 110 < diff < 130:
        score += 15
        active_vibe = "Harmonious"
        highlights.append("Moon Trine Moon: Intuition and action are in sync.")
        
    # Example Logic: Jupiter Movement
    if now_planets["Jupiter"]["sign"] == natal_planets["Sun"]["sign"]:
        score += 10
        highlights.append("Jupiter supporting your Core Identity: Expansion is favored.")

    return {
        "score": min(score, 100),
        "vibe": active_vibe,
        "current_moon": now_planets["Moon"]["sign"],
        "highlights": highlights,
        "timestamp": datetime.utcnow().isoformat()
    }