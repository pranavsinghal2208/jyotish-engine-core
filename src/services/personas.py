from ..core.context import engine

def identify_persona(context):
    """Categorizes the user into a High-Stake Marketing Persona based on their chart."""
    state = context.get_state()
    if not state: return "The Voyager"
    
    planets = state["planets_birth"]
    
    # 1. THE SOVEREIGN (Sun Dominant in 1st, 10th) - High Stakes Founder
    sun = planets.get("Sun", {})
    if sun.get("house") in [1, 10] or sun.get("sign") in ["Leo", "Aries"]:
        return {
            "name": "The Sovereign",
            "motivation": "Expansion, Recognition, Legacy",
            "de_motivation": "Mediocrity, Loss of Control",
            "retention_hook": "Legacy Benchmarking",
            "ideal_for_retainer": True
        }

    # 2. THE KINETIC (Mars Dominant) - High Frequency Trader / Scaler
    mars = planets.get("Mars", {})
    if mars.get("house") in [1, 3, 10] or mars.get("sign") in ["Aries", "Scorpio", "Capricorn"]:
        return {
            "name": "The Kinetic",
            "motivation": "Speed, Execution, Edge",
            "de_motivation": "Burnout, Friction, Stagnation",
            "retention_hook": "Daily Momentum Ticker",
            "ideal_for_retainer": True
        }

    # 3. THE ARCHITECT (Saturn Dominant) - Systems/Efficiency Mindset
    saturn = planets.get("Saturn", {})
    if saturn.get("house") in [1, 4, 10] or saturn.get("sign") in ["Capricorn", "Aquarius", "Libra"]:
        return {
            "name": "The Architect",
            "motivation": "Efficiency, Structure, Profitability",
            "de_motivation": "Chaos, Cost Leakage, Inefficiency",
            "retention_hook": "Weekly Strategic Map",
            "ideal_for_retainer": True
        }

    # Fallback
    return {
        "name": "The Seeker",
        "motivation": "Clarity, Self-Discovery",
        "de_motivation": "Confusion, Indecision",
        "retention_hook": "Daily Theme Narrative",
        "ideal_for_retainer": False
    }

def get_pain_point_strategy(pain_point):
    """Maps user pain points to 2L retainer justifications."""
    strategies = {
        "Efficiency": "Justify 2L via 20% increase in People/System throughput.",
        "Cash": "Justify 2L via 15% reduction in Receivables/GST leakage.",
        "Cost": "Justify 2L via permanent 10% reduction in burn/operational overhead."
    }
    return strategies.get(pain_point, "Focus on general Business Pulse.")