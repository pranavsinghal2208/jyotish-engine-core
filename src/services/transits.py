from ..core.context import engine
from datetime import datetime

def get_live_transits(context):
    """Calculates a high-precision Live Energy Score using Aspect Stacking."""
    state = context.get_state()
    if not state: return None
    
    now_jd = state["jd_now"]
    now_planets = engine.get_planetary_positions(now_jd)
    natal_planets = state["planets_birth"]
    
    score = 50
    active_vibe = "Stable"
    highlights = []
    
    # --- ASPECT STACKING ENGINE ---
    # We check relationships between current Moon/Sun and Natal Moon/Sun/Jupiter/Saturn
    checks = [
        ("Moon", "Moon", 25, "Lunar Alignment"),
        ("Moon", "Sun", 15, "Vitality Flow"),
        ("Sun", "Sun", 10, "Solar Peak"),
        ("Moon", "Jupiter", 15, "Growth Window"),
        ("Moon", "Saturn", -10, "Focus Period") # Saturn decreases score but adds "Focus"
    ]
    
    for t_pl, n_pl, weight, label in checks:
        if t_pl in now_planets and n_pl in natal_planets:
            diff = abs(now_planets[t_pl]["longitude"] - natal_planets[n_pl]["longitude"]) % 360
            
            # Conjunction/Opp (Strong)
            if diff < 10 or 170 < diff < 190: 
                score += weight
                highlights.append(f"{label}: Strong energy influence.")
            # Trine/Sextile (Harmonious)
            elif 55 < diff < 65 or 115 < diff < 125 or 235 < diff < 245 or 295 < diff < 305:
                score += (weight * 0.7)
                highlights.append(f"{label}: Harmonious flow detected.")
            # Square (Dynamic Tension)
            elif 85 < diff < 95 or 265 < diff < 275:
                score += (abs(weight) * 0.4) # Add positive points for actionability
                highlights.append(f"{label}: Dynamic window — prioritize execution.")

    # Calibration: Set vibes based on final score
    if score > 75: active_vibe = "Peak Momentum"
    elif score > 65: active_vibe = "High Alignment"
    elif score > 55: active_vibe = "Favorable"
    elif score < 45: active_vibe = "Rest & Recalibrate"

    return {
        "score": round(max(0, min(score, 100))),
        "vibe": active_vibe,
        "current_moon": now_planets.get("Moon", {}).get("sign", "Unknown"),
        "highlights": highlights[:2], # Top 2 for the ticker
        "timestamp": datetime.utcnow().isoformat()
    }