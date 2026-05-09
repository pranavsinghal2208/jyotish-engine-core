from ..core.context import engine

def get_remedies(context):
    """Predicts challenges and suggests high-end remedies (Stones/Supplements)."""
    state = context.get_state()
    if not state: return None
    
    planets = state["planets_birth"]
    remedies = []
    
    # 1. Challenge: Saturn Influence (Delays, Structure)
    saturn = planets.get("Saturn", {})
    if saturn.get("house") in [8, 12]:
        remedies.append({
            "challenge": "Mental Load & Structural Delays",
            "progress_signal": "Mastery through discipline",
            "ritual": "Saturday silence practice",
            "supplement": "Magnesium L-Threonate for neural rest",
            "stone": "Blue Sapphire (Neelam) for precision",
            "priority": "High"
        })

    # 2. Challenge: Mars Influence (Aggression, Burnout)
    mars = planets.get("Mars", {})
    if mars.get("sign") in ["Cancer", "Libra"]:
        remedies.append({
            "challenge": "Execution Burnout",
            "progress_signal": "Strategic assertion",
            "ritual": "Cold plunge or breathwork",
            "supplement": "Ashwagandha KSM-66",
            "stone": "Red Coral for vitality management",
            "priority": "Medium"
        })

    # Fallback if no major challenges
    if not remedies:
        remedies.append({
            "challenge": "Stable Orbit",
            "progress_signal": "Consistent growth",
            "ritual": "Gratitude logging",
            "supplement": "Multi-vitamin complex",
            "stone": "Clear Quartz for amplification",
            "priority": "Low"
        })

    return remedies