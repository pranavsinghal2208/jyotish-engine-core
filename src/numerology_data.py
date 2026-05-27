"""
Reference tables from the Numerology master sheet.
Covers all 81 Driver~Conductor combinations, missing-number remedies,
and per-number meanings.
"""

# ---------------------------------------------------------------------------
# Driver ~ Conductor profiles  (all 81 combinations)
# Key format: "driver~conductor"
# ---------------------------------------------------------------------------
DRIVER_CONDUCTOR_PROFILES = {
    "1~1": {"pros": ["Leadership", "Ambition", "Visibility", "Innovation", "Confidence"], "cons": ["Ego issues", "Impatience", "Rigidity", "Need for control", "Dominance"], "mode": "Business (Leadership roles)", "industries": ["Entrepreneurship", "Management", "Politics", "Startups"], "compatibility": 90},
    "1~2": {"pros": ["Diplomatic", "Leadership", "Cooperative", "Ambition", "Sensitive"], "cons": ["Dependency", "Ego issues", "Easily influenced", "Overly emotional", "Impatience"], "mode": "Service (Partnership/Support roles)", "industries": ["Counseling", "Politics", "Management", "Startups", "Public Relations"], "compatibility": 69},
    "1~3": {"pros": ["Leadership", "Optimism", "Ambition", "Teaching ability", "Visibility"], "cons": ["Ego issues", "Lack of focus", "Overtalkative", "Pride", "Impatience"], "mode": "Both (Teaching/Advisory)", "industries": ["Publishing", "Spiritual fields", "Politics", "Education", "Management"], "compatibility": 76},
    "1~4": {"pros": ["Leadership", "Innovative disruptor", "Determined", "Ambition", "Practical"], "cons": ["Struggles", "Ego issues", "Isolation", "Impatience", "Rigidity"], "mode": "Business (System/Process innovation)", "industries": ["Politics", "Engineering", "Management", "Startups", "Strategy Consulting"], "compatibility": 70},
    "1~5": {"pros": ["Adaptability", "Leadership", "Sales ability", "Communication", "Ambition"], "cons": ["Superficiality", "Ego issues", "Restlessness", "Lack of focus", "Inconsistency"], "mode": "Both (Communication-heavy)", "industries": ["Sales", "Politics", "Marketing", "Management", "Startups"], "compatibility": 76},
    "1~6": {"pros": ["Charm", "Aesthetic sense", "Leadership", "Ambition", "Visibility"], "cons": ["Dependency", "Ego issues", "Materialistic", "Impatience", "Overindulgence"], "mode": "Business (Arts, Creative)", "industries": ["Fashion", "Politics", "Luxury goods", "Design", "Management"], "compatibility": 76},
    "1~7": {"pros": ["Philosophical", "Leadership", "Research ability", "Ambition", "Spiritual depth"], "cons": ["Overthinking", "Ego issues", "Isolation", "Lack of practicality", "Impatience"], "mode": "Service (Research/Spiritual)", "industries": ["Academia", "Research", "Politics", "Management", "Startups"], "compatibility": 66},
    "1~8": {"pros": ["Leadership", "Authority", "Managerial ability", "Karmic strength", "Ambition"], "cons": ["Struggles", "Ego issues", "Isolation", "Stress", "Harshness"], "mode": "Business (Institutional/Structured)", "industries": ["Law", "Governance", "Finance", "Politics", "Corporate"], "compatibility": 60},
    "1~9": {"pros": ["Leadership", "Humanitarian", "Boldness", "Energy", "Ambition"], "cons": ["Short temper", "Ego issues", "Impatience", "Impulsiveness", "Over-dominance"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Politics", "Military", "Engineering", "Management"], "compatibility": 67},

    "2~1": {"pros": ["Diplomatic", "Leadership", "Cooperative", "Ambition", "Sensitive"], "cons": ["Dependency", "Ego issues", "Easily influenced", "Overly emotional", "Impatience"], "mode": "Service (Partnership/Support roles)", "industries": ["Counseling", "Politics", "Management", "Startups", "Public Relations"], "compatibility": 65},
    "2~2": {"pros": ["Diplomatic", "Cooperative", "Sensitive", "Adaptable", "Team player"], "cons": ["Dependency", "Easily influenced", "Overly emotional", "Indecisive", "Moody"], "mode": "Service (Partnership/Support roles)", "industries": ["Public Relations", "Counseling", "HR", "Arts"], "compatibility": 94},
    "2~3": {"pros": ["Diplomatic", "Optimism", "Cooperative", "Sensitive", "Teaching ability"], "cons": ["Dependency", "Lack of focus", "Easily influenced", "Overtalkative", "Overly emotional"], "mode": "Both (Teaching/Advisory)", "industries": ["Publishing", "Counseling", "Spiritual fields", "Education", "Public Relations"], "compatibility": 79},
    "2~4": {"pros": ["Diplomatic", "Innovative disruptor", "Determined", "Cooperative", "Sensitive"], "cons": ["Dependency", "Struggles", "Easily influenced", "Isolation", "Overly emotional"], "mode": "Business (System/Process innovation)", "industries": ["Counseling", "Engineering", "Public Relations", "Strategy Consulting", "Technology"], "compatibility": 57},
    "2~5": {"pros": ["Diplomatic", "Adaptability", "Sales ability", "Cooperative", "Sensitive"], "cons": ["Dependency", "Superficiality", "Restlessness", "Lack of focus", "Easily influenced"], "mode": "Both (Communication-heavy)", "industries": ["Counseling", "Sales", "Marketing", "Public Relations", "HR"], "compatibility": 70},
    "2~6": {"pros": ["Diplomatic", "Aesthetic sense", "Cooperative", "Sensitive", "Adaptable"], "cons": ["Dependency", "Easily influenced", "Materialistic", "Overly emotional", "Overindulgence"], "mode": "Business (Arts, Creative)", "industries": ["Fashion", "Counseling", "Luxury goods", "Design", "Film"], "compatibility": 80},
    "2~7": {"pros": ["Diplomatic", "Philosophical", "Research ability", "Cooperative", "Sensitive"], "cons": ["Dependency", "Overthinking", "Easily influenced", "Isolation", "Lack of practicality"], "mode": "Service (Research/Spiritual)", "industries": ["Counseling", "Research", "Occult", "Public Relations", "Academia"], "compatibility": 65},
    "2~8": {"pros": ["Diplomatic", "Authority", "Managerial ability", "Karmic strength", "Cooperative"], "cons": ["Dependency", "Struggles", "Easily influenced", "Isolation", "Stress"], "mode": "Business (Institutional/Structured)", "industries": ["Counseling", "Law", "Governance", "Finance", "Corporate"], "compatibility": 70},
    "2~9": {"pros": ["Diplomatic", "Humanitarian", "Boldness", "Cooperative", "Sensitive"], "cons": ["Dependency", "Short temper", "Easily influenced", "Overly emotional", "Impulsiveness"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Counseling", "Military", "Engineering", "Sports"], "compatibility": 69},

    "3~1": {"pros": ["Leadership", "Optimism", "Ambition", "Teaching ability", "Visibility"], "cons": ["Ego issues", "Lack of focus", "Overtalkative", "Pride", "Impatience"], "mode": "Both (Teaching/Advisory)", "industries": ["Publishing", "Spiritual fields", "Politics", "Education", "Management"], "compatibility": 82},
    "3~2": {"pros": ["Diplomatic", "Optimism", "Cooperative", "Sensitive", "Teaching ability"], "cons": ["Dependency", "Lack of focus", "Easily influenced", "Overtalkative", "Overly emotional"], "mode": "Both (Teaching/Advisory)", "industries": ["Publishing", "Counseling", "Spiritual fields", "Education", "Public Relations"], "compatibility": 82},
    "3~3": {"pros": ["Optimism", "Teaching ability", "Wisdom", "Visionary", "Creative"], "cons": ["Lack of focus", "Overtalkative", "Pride", "Over-expectation", "Over idealistic"], "mode": "Both (Teaching/Advisory)", "industries": ["Spiritual fields", "Education", "Publishing", "Consulting"], "compatibility": 87},
    "3~4": {"pros": ["Innovative disruptor", "Determined", "Optimism", "Practical", "Teaching ability"], "cons": ["Struggles", "Lack of focus", "Overtalkative", "Isolation", "Pride"], "mode": "Business (System/Process innovation)", "industries": ["Publishing", "Spiritual fields", "Engineering", "Education", "Strategy Consulting"], "compatibility": 64},
    "3~5": {"pros": ["Adaptability", "Optimism", "Sales ability", "Communication", "Teaching ability"], "cons": ["Superficiality", "Restlessness", "Lack of focus", "Overtalkative", "Inconsistency"], "mode": "Both (Communication-heavy)", "industries": ["Publishing", "Spiritual fields", "Sales", "Marketing", "Education"], "compatibility": 66},
    "3~6": {"pros": ["Aesthetic sense", "Optimism", "Teaching ability", "Wisdom", "Visionary"], "cons": ["Dependency", "Lack of focus", "Materialistic", "Overtalkative", "Pride"], "mode": "Business (Arts, Creative)", "industries": ["Publishing", "Fashion", "Spiritual fields", "Luxury goods", "Design"], "compatibility": 85},
    "3~7": {"pros": ["Philosophical", "Optimism", "Research ability", "Teaching ability", "Spiritual depth"], "cons": ["Overthinking", "Lack of focus", "Overtalkative", "Isolation", "Lack of practicality"], "mode": "Service (Research/Spiritual)", "industries": ["Publishing", "Spiritual fields", "Research", "Education", "Academia"], "compatibility": 75},
    "3~8": {"pros": ["Authority", "Managerial ability", "Optimism", "Karmic strength", "Teaching ability"], "cons": ["Struggles", "Lack of focus", "Overtalkative", "Isolation", "Stress"], "mode": "Business (Institutional/Structured)", "industries": ["Publishing", "Spiritual fields", "Law", "Governance", "Finance"], "compatibility": 64},
    "3~9": {"pros": ["Humanitarian", "Boldness", "Optimism", "Energy", "Teaching ability"], "cons": ["Short temper", "Lack of focus", "Overtalkative", "Pride", "Impulsiveness"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Publishing", "Spiritual fields", "Military", "Engineering"], "compatibility": 83},

    "4~1": {"pros": ["Leadership", "Innovative disruptor", "Determined", "Ambition", "Practical"], "cons": ["Struggles", "Ego issues", "Isolation", "Impatience", "Rigidity"], "mode": "Business (System/Process innovation)", "industries": ["Politics", "Engineering", "Management", "Startups", "Strategy Consulting"], "compatibility": 67},
    "4~2": {"pros": ["Diplomatic", "Innovative disruptor", "Determined", "Cooperative", "Sensitive"], "cons": ["Dependency", "Struggles", "Easily influenced", "Isolation", "Overly emotional"], "mode": "Business (System/Process innovation)", "industries": ["Counseling", "Engineering", "Public Relations", "Strategy Consulting", "Technology"], "compatibility": 74},
    "4~3": {"pros": ["Innovative disruptor", "Determined", "Optimism", "Practical", "Teaching ability"], "cons": ["Struggles", "Lack of focus", "Overtalkative", "Isolation", "Pride"], "mode": "Business (System/Process innovation)", "industries": ["Publishing", "Spiritual fields", "Engineering", "Education", "Strategy Consulting"], "compatibility": 65},
    "4~4": {"pros": ["Innovative disruptor", "Hardworking", "Practical", "Determined", "System builder"], "cons": ["Struggles", "Isolation", "Rigidity", "Delays", "Unconventional path"], "mode": "Business (System/Process innovation)", "industries": ["Reform movements", "Engineering", "Strategy Consulting", "Technology"], "compatibility": 85},
    "4~5": {"pros": ["Adaptability", "Innovative disruptor", "Hardworking", "Sales ability", "Communication"], "cons": ["Superficiality", "Struggles", "Restlessness", "Lack of focus", "Isolation"], "mode": "Both (Communication-heavy)", "industries": ["Sales", "Engineering", "Marketing", "Strategy Consulting", "Technology"], "compatibility": 58},
    "4~6": {"pros": ["Creativity", "Aesthetic sense", "Innovative disruptor", "Hardworking", "Practical"], "cons": ["Dependency", "Struggles", "Materialistic", "Isolation", "Overindulgence"], "mode": "Business (Arts, Creative)", "industries": ["Fashion", "Luxury goods", "Design", "Engineering", "Strategy Consulting"], "compatibility": 58},
    "4~7": {"pros": ["Philosophical", "Innovative disruptor", "Hardworking", "Research ability", "Practical"], "cons": ["Overthinking", "Struggles", "Isolation", "Lack of practicality", "Escapism"], "mode": "Service (Research/Spiritual)", "industries": ["Research", "Engineering", "Strategy Consulting", "Technology", "Reform movements"], "compatibility": 55},
    "4~8": {"pros": ["Innovative disruptor", "Hardworking", "Authority", "Managerial ability", "Karmic strength"], "cons": ["Struggles", "Isolation", "Stress", "Harshness", "Rigidity"], "mode": "Business (Institutional/Structured)", "industries": ["Law", "Governance", "Finance", "Corporate", "Engineering"], "compatibility": 71},
    "4~9": {"pros": ["Innovative disruptor", "Hardworking", "Boldness", "Humanitarian", "Energy"], "cons": ["Short temper", "Struggles", "Isolation", "Impulsiveness", "Over-dominance"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Military", "Engineering", "Sports", "Strategy Consulting"], "compatibility": 56},

    "5~1": {"pros": ["Adaptability", "Leadership", "Sales ability", "Communication", "Ambition"], "cons": ["Superficiality", "Ego issues", "Restlessness", "Lack of focus", "Inconsistency"], "mode": "Both (Communication-heavy)", "industries": ["Sales", "Politics", "Marketing", "Management", "Startups"], "compatibility": 77},
    "5~2": {"pros": ["Diplomatic", "Adaptability", "Sales ability", "Cooperative", "Sensitive"], "cons": ["Dependency", "Superficiality", "Restlessness", "Lack of focus", "Easily influenced"], "mode": "Both (Communication-heavy)", "industries": ["Counseling", "Sales", "Marketing", "Public Relations", "HR"], "compatibility": 68},
    "5~3": {"pros": ["Adaptability", "Optimism", "Sales ability", "Communication", "Teaching ability"], "cons": ["Superficiality", "Restlessness", "Lack of focus", "Overtalkative", "Inconsistency"], "mode": "Both (Communication-heavy)", "industries": ["Publishing", "Spiritual fields", "Sales", "Marketing", "Education"], "compatibility": 65},
    "5~4": {"pros": ["Adaptability", "Innovative disruptor", "Hardworking", "Sales ability", "Communication"], "cons": ["Superficiality", "Struggles", "Restlessness", "Lack of focus", "Isolation"], "mode": "Both (Communication-heavy)", "industries": ["Sales", "Engineering", "Marketing", "Strategy Consulting", "Technology"], "compatibility": 64},
    "5~5": {"pros": ["Adaptability", "Sales ability", "Communication", "Wit", "Quick learner"], "cons": ["Superficiality", "Restlessness", "Lack of focus", "Inconsistency", "Impatience"], "mode": "Both (Communication-heavy)", "industries": ["Sales", "Marketing", "Entertainment", "Media"], "compatibility": 95},
    "5~6": {"pros": ["Adaptability", "Romance", "Aesthetic sense", "Sales ability", "Communication"], "cons": ["Superficiality", "Dependency", "Restlessness", "Lack of focus", "Materialistic"], "mode": "Business (Arts, Creative)", "industries": ["Fashion", "Sales", "Luxury goods", "Design", "Marketing"], "compatibility": 80},
    "5~7": {"pros": ["Adaptability", "Philosophical", "Sales ability", "Research ability", "Communication"], "cons": ["Superficiality", "Overthinking", "Restlessness", "Lack of focus", "Isolation"], "mode": "Service (Research/Spiritual)", "industries": ["Sales", "Research", "Occult", "Marketing", "Academia"], "compatibility": 70},
    "5~8": {"pros": ["Adaptability", "Authority", "Managerial ability", "Sales ability", "Karmic strength"], "cons": ["Superficiality", "Struggles", "Restlessness", "Lack of focus", "Isolation"], "mode": "Business (Institutional/Structured)", "industries": ["Sales", "Law", "Governance", "Finance", "Corporate"], "compatibility": 75},
    "5~9": {"pros": ["Adaptability", "Humanitarian", "Boldness", "Sales ability", "Communication"], "cons": ["Superficiality", "Short temper", "Restlessness", "Lack of focus", "Inconsistency"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Sales", "Military", "Marketing", "Sports"], "compatibility": 66},

    "6~1": {"pros": ["Charm", "Aesthetic sense", "Leadership", "Ambition", "Visibility"], "cons": ["Dependency", "Ego issues", "Materialistic", "Impatience", "Overindulgence"], "mode": "Business (Arts, Creative)", "industries": ["Fashion", "Politics", "Luxury goods", "Design", "Management"], "compatibility": 85},
    "6~2": {"pros": ["Diplomatic", "Aesthetic sense", "Cooperative", "Sensitive", "Adaptable"], "cons": ["Dependency", "Easily influenced", "Materialistic", "Overly emotional", "Overindulgence"], "mode": "Business (Arts, Creative)", "industries": ["Fashion", "Counseling", "Luxury goods", "Design", "Film"], "compatibility": 80},
    "6~3": {"pros": ["Aesthetic sense", "Optimism", "Teaching ability", "Wisdom", "Visionary"], "cons": ["Dependency", "Lack of focus", "Materialistic", "Overtalkative", "Pride"], "mode": "Business (Arts, Creative)", "industries": ["Publishing", "Fashion", "Spiritual fields", "Luxury goods", "Design"], "compatibility": 80},
    "6~4": {"pros": ["Creativity", "Aesthetic sense", "Innovative disruptor", "Hardworking", "Practical"], "cons": ["Dependency", "Struggles", "Materialistic", "Isolation", "Overindulgence"], "mode": "Business (Arts, Creative)", "industries": ["Fashion", "Luxury goods", "Design", "Engineering", "Strategy Consulting"], "compatibility": 70},
    "6~5": {"pros": ["Adaptability", "Romance", "Aesthetic sense", "Sales ability", "Communication"], "cons": ["Superficiality", "Dependency", "Restlessness", "Lack of focus", "Materialistic"], "mode": "Business (Arts, Creative)", "industries": ["Fashion", "Sales", "Luxury goods", "Design", "Marketing"], "compatibility": 76},
    "6~6": {"pros": ["Aesthetic sense", "Charm", "Romance", "Caring", "Creativity"], "cons": ["Dependency", "Materialistic", "Overindulgence", "Over-romantic", "Jealousy"], "mode": "Business (Arts, Creative)", "industries": ["Fashion", "Luxury goods", "Design", "Film"], "compatibility": 95},
    "6~7": {"pros": ["Philosophical", "Aesthetic sense", "Research ability", "Spiritual depth", "Charm"], "cons": ["Dependency", "Overthinking", "Materialistic", "Isolation", "Lack of practicality"], "mode": "Service (Research/Spiritual)", "industries": ["Fashion", "Research", "Luxury goods", "Design", "Academia"], "compatibility": 56},
    "6~8": {"pros": ["Aesthetic sense", "Authority", "Managerial ability", "Karmic strength", "Discipline"], "cons": ["Dependency", "Struggles", "Materialistic", "Isolation", "Stress"], "mode": "Business (Institutional/Structured)", "industries": ["Fashion", "Law", "Governance", "Finance", "Luxury goods"], "compatibility": 57},
    "6~9": {"pros": ["Aesthetic sense", "Humanitarian", "Boldness", "Energy", "Courage"], "cons": ["Dependency", "Short temper", "Materialistic", "Overindulgence", "Impulsiveness"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Fashion", "Luxury goods", "Military", "Design"], "compatibility": 76},

    "7~1": {"pros": ["Philosophical", "Leadership", "Research ability", "Ambition", "Spiritual depth"], "cons": ["Overthinking", "Ego issues", "Isolation", "Lack of practicality", "Impatience"], "mode": "Service (Research/Spiritual)", "industries": ["Academia", "Research", "Politics", "Management", "Startups"], "compatibility": 63},
    "7~2": {"pros": ["Diplomatic", "Philosophical", "Research ability", "Cooperative", "Sensitive"], "cons": ["Dependency", "Overthinking", "Easily influenced", "Isolation", "Lack of practicality"], "mode": "Service (Research/Spiritual)", "industries": ["Counseling", "Research", "Occult", "Public Relations", "Academia"], "compatibility": 73},
    "7~3": {"pros": ["Philosophical", "Optimism", "Research ability", "Teaching ability", "Spiritual depth"], "cons": ["Overthinking", "Lack of focus", "Overtalkative", "Isolation", "Lack of practicality"], "mode": "Service (Research/Spiritual)", "industries": ["Publishing", "Spiritual fields", "Research", "Education", "Academia"], "compatibility": 69},
    "7~4": {"pros": ["Philosophical", "Innovative disruptor", "Hardworking", "Research ability", "Practical"], "cons": ["Overthinking", "Struggles", "Isolation", "Lack of practicality", "Escapism"], "mode": "Service (Research/Spiritual)", "industries": ["Research", "Engineering", "Strategy Consulting", "Technology", "Reform movements"], "compatibility": 57},
    "7~5": {"pros": ["Adaptability", "Philosophical", "Sales ability", "Research ability", "Communication"], "cons": ["Superficiality", "Overthinking", "Restlessness", "Lack of focus", "Isolation"], "mode": "Service (Research/Spiritual)", "industries": ["Sales", "Research", "Occult", "Marketing", "Academia"], "compatibility": 65},
    "7~6": {"pros": ["Philosophical", "Aesthetic sense", "Research ability", "Spiritual depth", "Charm"], "cons": ["Dependency", "Overthinking", "Materialistic", "Isolation", "Lack of practicality"], "mode": "Service (Research/Spiritual)", "industries": ["Fashion", "Research", "Luxury goods", "Design", "Academia"], "compatibility": 70},
    "7~7": {"pros": ["Philosophical", "Research ability", "Spiritual depth", "Intuition", "Analytical"], "cons": ["Detachment", "Overthinking", "Isolation", "Escapism", "Lack of practicality"], "mode": "Service (Research/Spiritual)", "industries": ["Research", "Healing", "Academia", "Occult"], "compatibility": 93},
    "7~8": {"pros": ["Philosophical", "Authority", "Managerial ability", "Research ability", "Karmic strength"], "cons": ["Detachment", "Overthinking", "Struggles", "Isolation", "Stress"], "mode": "Business (Institutional/Structured)", "industries": ["Law", "Research", "Governance", "Finance", "Corporate"], "compatibility": 66},
    "7~9": {"pros": ["Philosophical", "Humanitarian", "Boldness", "Research ability", "Energy"], "cons": ["Short temper", "Detachment", "Overthinking", "Isolation", "Escapism"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Research", "Military", "Engineering", "Sports"], "compatibility": 55},

    "8~1": {"pros": ["Leadership", "Authority", "Managerial ability", "Karmic strength", "Ambition"], "cons": ["Struggles", "Ego issues", "Isolation", "Stress", "Harshness"], "mode": "Business (Institutional/Structured)", "industries": ["Law", "Governance", "Finance", "Politics", "Corporate"], "compatibility": 69},
    "8~2": {"pros": ["Diplomatic", "Authority", "Managerial ability", "Karmic strength", "Cooperative"], "cons": ["Dependency", "Struggles", "Easily influenced", "Isolation", "Stress"], "mode": "Business (Institutional/Structured)", "industries": ["Counseling", "Law", "Governance", "Finance", "Corporate"], "compatibility": 62},
    "8~3": {"pros": ["Authority", "Managerial ability", "Optimism", "Karmic strength", "Teaching ability"], "cons": ["Struggles", "Lack of focus", "Overtalkative", "Isolation", "Stress"], "mode": "Business (Institutional/Structured)", "industries": ["Publishing", "Spiritual fields", "Law", "Governance", "Finance"], "compatibility": 67},
    "8~4": {"pros": ["Innovative disruptor", "Hardworking", "Authority", "Managerial ability", "Karmic strength"], "cons": ["Struggles", "Isolation", "Stress", "Harshness", "Rigidity"], "mode": "Business (Institutional/Structured)", "industries": ["Law", "Governance", "Finance", "Corporate", "Engineering"], "compatibility": 67},
    "8~5": {"pros": ["Adaptability", "Authority", "Managerial ability", "Sales ability", "Karmic strength"], "cons": ["Superficiality", "Struggles", "Restlessness", "Lack of focus", "Isolation"], "mode": "Business (Institutional/Structured)", "industries": ["Sales", "Law", "Governance", "Finance", "Corporate"], "compatibility": 70},
    "8~6": {"pros": ["Aesthetic sense", "Authority", "Managerial ability", "Karmic strength", "Discipline"], "cons": ["Dependency", "Struggles", "Materialistic", "Isolation", "Stress"], "mode": "Business (Institutional/Structured)", "industries": ["Fashion", "Law", "Governance", "Finance", "Luxury goods"], "compatibility": 64},
    "8~7": {"pros": ["Philosophical", "Authority", "Managerial ability", "Research ability", "Karmic strength"], "cons": ["Detachment", "Overthinking", "Struggles", "Isolation", "Stress"], "mode": "Business (Institutional/Structured)", "industries": ["Law", "Research", "Governance", "Finance", "Corporate"], "compatibility": 55},
    "8~8": {"pros": ["Managerial ability", "Authority", "Karmic strength", "Endurance", "Discipline"], "cons": ["Struggles", "Isolation", "Stress", "Harshness", "Delays"], "mode": "Business (Institutional/Structured)", "industries": ["Law", "Governance", "Finance", "Corporate"], "compatibility": 90},
    "8~9": {"pros": ["Managerial ability", "Authority", "Boldness", "Humanitarian", "Karmic strength"], "cons": ["Short temper", "Struggles", "Isolation", "Stress", "Harshness"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Law", "Governance", "Finance", "Military"], "compatibility": 60},

    "9~1": {"pros": ["Leadership", "Humanitarian", "Boldness", "Energy", "Ambition"], "cons": ["Short temper", "Ego issues", "Impatience", "Impulsiveness", "Over-dominance"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Politics", "Military", "Engineering", "Management"], "compatibility": 78},
    "9~2": {"pros": ["Diplomatic", "Humanitarian", "Boldness", "Cooperative", "Sensitive"], "cons": ["Dependency", "Short temper", "Easily influenced", "Overly emotional", "Impulsiveness"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Counseling", "Military", "Engineering", "Sports"], "compatibility": 66},
    "9~3": {"pros": ["Humanitarian", "Boldness", "Optimism", "Energy", "Teaching ability"], "cons": ["Short temper", "Lack of focus", "Overtalkative", "Pride", "Impulsiveness"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Publishing", "Spiritual fields", "Military", "Engineering"], "compatibility": 78},
    "9~4": {"pros": ["Innovative disruptor", "Hardworking", "Boldness", "Humanitarian", "Energy"], "cons": ["Short temper", "Struggles", "Isolation", "Impulsiveness", "Over-dominance"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Military", "Engineering", "Sports", "Strategy Consulting"], "compatibility": 62},
    "9~5": {"pros": ["Adaptability", "Humanitarian", "Boldness", "Sales ability", "Communication"], "cons": ["Superficiality", "Short temper", "Restlessness", "Lack of focus", "Inconsistency"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Sales", "Military", "Marketing", "Sports"], "compatibility": 60},
    "9~6": {"pros": ["Aesthetic sense", "Humanitarian", "Boldness", "Energy", "Courage"], "cons": ["Dependency", "Short temper", "Materialistic", "Overindulgence", "Impulsiveness"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Fashion", "Luxury goods", "Military", "Design"], "compatibility": 75},
    "9~7": {"pros": ["Philosophical", "Humanitarian", "Boldness", "Research ability", "Energy"], "cons": ["Short temper", "Detachment", "Overthinking", "Isolation", "Escapism"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Research", "Military", "Engineering", "Sports"], "compatibility": 73},
    "9~8": {"pros": ["Managerial ability", "Authority", "Boldness", "Humanitarian", "Karmic strength"], "cons": ["Short temper", "Struggles", "Isolation", "Stress", "Harshness"], "mode": "Business (Leadership/Action)", "industries": ["Activism", "Law", "Governance", "Finance", "Military"], "compatibility": 55},
    "9~9": {"pros": ["Humanitarian", "Boldness", "Energy", "Courage", "Passion"], "cons": ["Short temper", "Impulsiveness", "Over-dominance", "Over-expansion", "Aggression"], "mode": "Business (Leadership/Action)", "industries": ["Engineering", "Sports", "Military", "Activism"], "compatibility": 91},
}

# ---------------------------------------------------------------------------
# Missing number remedies (numbers absent from Lo Shu birth chart)
# ---------------------------------------------------------------------------
MISSING_NUMBER_REMEDIES = {
    1: {
        "planet": "Sun", "color": "Black", "element": "Water",
        "name": "Directional Alignment",
        "framework": {
            "meaning": "Identity-matrix friction. Decisional inertia.",
            "effect": "Reduced torque in personal authority. Latency in first-mover execution.",
            "resolution": "Solar-alignment (Morning Sun). Red-element wrist alignment. Prioritize decisional closure."
        },
        "remedies": ["Offer water to Sun daily", "Water fountain in North", "Red dhaga on wrist"],
    },
    2: {
        "planet": "Moon", "color": "Pink", "element": "Earth",
        "name": "Equilibrium & Feedback",
        "framework": {
            "meaning": "Atmospheric volatility. Unstable internal radar.",
            "effect": "High-friction interpersonal feedback. Emotional processing latency.",
            "resolution": "Mountain-visual environment design. Silver-vessel hydration. Lunar rigor (Shiv Aradhana)."
        },
        "remedies": ["Mountain picture in house", "Flower Agate bracelet", "Silver glass hydration"],
    },
    3: {
        "planet": "Jupiter", "color": "Green", "element": "Wood",
        "name": "Expansion & Arbitrage",
        "framework": {
            "meaning": "Information-gap. Scarcity-logic bias.",
            "effect": "Yield-leakage in growth opportunities. Mentorship-insulation.",
            "resolution": "Daily Saffron-tilak alignment. Wood-element environment design. Active mentorship networking."
        },
        "remedies": ["Peridot grounding", "Use wooden furniture", "Apply kesar tilak"],
    },
    4: {
        "planet": "Rahu", "color": "Purple / Gold", "element": "Wood",
        "name": "Systemic Discipline",
        "framework": {
            "meaning": "Execution instability. Non-linear scaling friction.",
            "effect": "Revenue volatility. Delays in system-build closures.",
            "resolution": "Botanical environment design. Green Aventurine grounding. Service-animal (stray dog) support."
        },
        "remedies": ["Water plants daily", "Green Aventurine bracelet", "Feed stray dogs"],
    },
    5: {
        "planet": "Mercury", "color": "Yellow", "element": "Earth",
        "name": "Stability & Transmission",
        "framework": {
            "meaning": "Data-processing restlessness. Logic-friction.",
            "effect": "Communication-leakage. Reduced grounding in high-bandwidth environments.",
            "resolution": "Botanical immersion. Green-element color therapy. Crystalline data-grounding."
        },
        "remedies": ["Walk barefoot in nature", "Green nutrient-alignment", "Smoky Quartz grounding"],
    },
    6: {
        "planet": "Venus", "color": "White", "element": "Hard Metal",
        "name": "Support & Capital",
        "framework": {
            "meaning": "Alliance-gap. Resource-entropy.",
            "effect": "Low support-coefficient from circles. ROI friction in aesthetics and luxury.",
            "resolution": "Metal-element system (Wind Chimes in NW). Golden-metal wrist alignment. White-element resource scaling."
        },
        "remedies": ["Metal wind chimes in NW", "Golden wrist watch", "Donate white items"],
    },
    7: {
        "planet": "Ketu", "color": "Grey", "element": "Soft Metal",
        "name": "Insight & Introspection",
        "framework": {
            "meaning": "Spiritual-logic friction. Data-insulation.",
            "effect": "Connectivity-gap with legacy. Latency in internal-signal detection.",
            "resolution": "7-Mukhi Rudraksh alignment. Service-animal support. Process-audit retreat."
        },
        "remedies": ["Stray dog seva", "Wear 7 Mukhi Rudraksh"],
    },
    8: {
        "planet": "Saturn", "color": "Blue", "element": "Earth",
        "name": "Execution & Assets",
        "framework": {
            "meaning": "Institutional friction. Duration-gap.",
            "effect": "Success-latency. High-friction in long-range property or structural scaling.",
            "resolution": "Saturday execution-fast. NE-quadrant water alignment. Strategic currency donations."
        },
        "remedies": ["Water pot in NE corner", "Saturday fast", "Strategic donations"],
    },
    9: {
        "planet": "Mars", "color": "Red", "element": "Fire",
        "name": "Torque & Visibility",
        "framework": {
            "meaning": "Velocity-gap. Energy-leakage.",
            "effect": "Recognition-lag. Low-torque execution in competitive domains.",
            "resolution": "Red-spectrum light alignment (South). Martian-rigor (Hanuman Puja). Fire Agate grounding."
        },
        "remedies": ["Red light in South", "9 Mukhi Rudraksh", "Martian puja rigor"],
    },
}

# ---------------------------------------------------------------------------
# Namank (Name Number) Definitions
# ---------------------------------------------------------------------------
NAMANK_INTERPRETATIONS = {
    1: "Leader Vibration — Authority-led identity. Optimized for first-mover innovation and decisional command.",
    2: "Diplomat Vibration — Equilibrium-led identity. Optimized for alliance-building and harmonious connectivity.",
    3: "Creator Vibration — Expression-led identity. Optimized for high-bandwidth communication and optimistic scaling.",
    4: "Builder Vibration — Structure-led identity. Optimized for system-permanence and rigorous practical builds.",
    5: "Catalyst Vibration — Change-led identity. Optimized for high-volatility adaptation and rapid mental agility.",
    6: "Guardian Vibration — Responsibility-led identity. Optimized for resource-nurturing and domestic/family scaling.",
    7: "Seeker Vibration — Analysis-led identity. Optimized for deep-niche research and spiritual-logic sensing.",
    8: "Executive Vibration — Power-led identity. Optimized for material scaling and authoritative asset command.",
    9: "Humanitarian Vibration — Scale-led identity. Optimized for global-impact and systemic completion logic.",
}

# ---------------------------------------------------------------------------
# Lottery / Lucky Number Logic (Based on KUA & Mulank)
# ---------------------------------------------------------------------------
LOTTERY_NUMBER_MEANINGS = {
    "primary": "Universal Luck digit. Low-resistance window for dates, tokens, and numerical data-points.",
    "secondary": "Financial Flow digit. Optimized for removing blocks in material growth and revenue-flow.",
}

# ---------------------------------------------------------------------------
# Per-number meanings (planet, color, element, characteristics)
# ---------------------------------------------------------------------------
NUMBER_MEANINGS = {
    1: {"planet": "Sun",     "color": "Black",        "element": "Water",      "characteristics": "Independence, Command, Innovation."},
    2: {"planet": "Moon",    "color": "Pink",         "element": "Earth",      "characteristics": "Equilibrium, Intuition, Diplomacy."},
    3: {"planet": "Jupiter", "color": "Green",        "element": "Wood",       "characteristics": "Expansion, Expression, Optimization."},
    4: {"planet": "Rahu",    "color": "Purple/Gold",  "element": "Wood",       "characteristics": "Stability, Disruption, Structure."},
    5: {"planet": "Mercury", "color": "Yellow",       "element": "Earth",      "characteristics": "Adaptation, Transmission, Agility."},
    6: {"planet": "Venus",   "color": "White",        "element": "Hard Metal", "characteristics": "Value, Nurturing, Harmony."},
    7: {"planet": "Ketu",    "color": "Grey",         "element": "Soft Metal", "characteristics": "Audit, Introspection, Insight."},
    8: {"planet": "Saturn",  "color": "Blue",         "element": "Earth",      "characteristics": "Authority, Duration, Success."},
    9: {"planet": "Mars",    "color": "Red",          "element": "Fire",       "characteristics": "Velocity, Energy, Completion."},
}

# Lo Shu grid layout: number → (row, col) zero-indexed
LO_SHU_POSITIONS = {4: (0,0), 9: (0,1), 2: (0,2), 3: (1,0), 5: (1,1), 7: (1,2), 8: (2,0), 1: (2,1), 6: (2,2)}

KARMIC_NUMBERS = [10, 13, 14, 16, 19]
