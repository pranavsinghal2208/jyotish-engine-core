from ..core.context import engine
from datetime import datetime, timedelta

def get_lucky_windows(context):
    """Scans the next 7 days for high-momentum energy windows."""
    state = context.get_state()
    if not state: return None
    
    natal_planets = state["planets_birth"]
    start_jd = state["jd_now"]
    
    windows = []
    
    # Scan next 7 days, checking every 6 hours for efficiency in this v1
    for i in range(28): # 7 days * 4 slots per day
        check_jd = start_jd + (i * 0.25) # 0.25 days = 6 hours
        check_planets = engine.get_planetary_positions(check_jd)
        
        # Calculate a simplified Momentum Score for this window
        score = 50
        
        # 1. Moon Alignment (Fast moving, high impact)
        diff = abs(check_planets["Moon"]["longitude"] - natal_planets["Moon"]["longitude"]) % 360
        if diff < 15 or diff > 345: score += 25  # Conjunction
        elif 110 < diff < 130: score += 15      # Trine
        
        # 2. Sun Alignment (Vitality)
        sun_diff = abs(check_planets["Sun"]["longitude"] - natal_planets["Sun"]["longitude"]) % 360
        if 110 < sun_diff < 130: score += 10    # Harmonious solar window
        
        check_dt = datetime.fromtimestamp((check_jd - 2440587.5) * 86400) # Quick conversion
        
        windows.append({
            "timestamp": check_dt.strftime("%Y-%m-%d %H:%M"),
            "score": min(score, 100),
            "vibe": "Peak" if score > 70 else ("Good" if score > 55 else "Neutral")
        })
        
    return {
        "days": 7,
        "windows": windows
    }