from typing import Dict, Any, List
from datetime import datetime

# ---------------------------------------------------------------------------
# Chart-Specific Content Layer — planet × sign × house combinations
# ---------------------------------------------------------------------------

SIGN_ORDER = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

HOUSE_SHORT = {
    1: "identity & body", 2: "wealth & speech", 3: "effort & siblings",
    4: "home & heart", 5: "intellect & children", 6: "work & obstacles",
    7: "partnerships", 8: "hidden depth & transformation", 9: "luck & dharma",
    10: "career & status", 11: "gains & networks", 12: "loss & liberation"
}

def get_house(planet_sign: str, lagna_sign: str) -> int:
    return (SIGN_ORDER.index(planet_sign) - SIGN_ORDER.index(lagna_sign)) % 12 + 1


PLANET_SIGN_INTERP = {
    "Sun": {
        "Aries":       "High-velocity identity. Lead through direct action and first-mover execution.",
        "Taurus":      "Asset-backed identity. Prioritize durable builds and material compounding. Resist trend-chasing.",
        "Gemini":      "Networked identity. Bridge disparate ideas. Value connectivity over specialization.",
        "Cancer":      "Intuition-led identity. Scale through emotional intelligence and high-trust environments.",
        "Leo":         "Authority-led identity. Command visibility. Lead from the center, not the front.",
        "Virgo":       "Precision-led identity. Excellence through audit and process optimization.",
        "Libra":       "Equilibrium identity. Scale through strategic partnership and diplomatic leverage.",
        "Scorpio":     "High-stakes identity. Resilient in crisis. Value depth and hidden data.",
        "Sagittarius": "Vision-led identity. Drive growth through big-picture systems and global perspective.",
        "Capricorn":   "Structure-led identity. Master of endurance and long-range institutional builds.",
        "Aquarius":    "Disruptive identity. Focus on systems-thinking and unconventional logic.",
        "Pisces":      "Sensing identity. Perceive non-linear signals and creative breakthroughs."
    },
    "Moon": {
        "Aries":       "Fast emotional response. High-friction processing. Needs immediate closure.",
        "Taurus":      "Fixed emotional anchor. Values continuity. High resistance to volatility.",
        "Gemini":      "Communication-led mindset. Processes logic through dialogue and varied data streams.",
        "Cancer":      "High-bandwidth empathy. Senses sub-text and atmospheric shifts instantly.",
        "Leo":         "Loyalty-led mindset. Thrives on recognition and central team importance.",
        "Virgo":       "Analytical mindset. Processes emotions through categorization and audit.",
        "Libra":       "Harmony-led mindset. Optimized for collaboration. Instinctive win-win negotiator.",
        "Scorpio":     "Strategic mindset. High-intensity focus. Senses what others conceal.",
        "Sagittarius": "Expansive mindset. High recovery speed. Finds opportunity in difficulty.",
        "Capricorn":   "Disciplined mindset. Channels feeling into utility and long-term targets.",
        "Aquarius":    "Detached mindset. Objective observer. Optimized for humanitarian or large-scale logic.",
        "Pisces":      "Fluid mindset. Creative and non-linear. Absorbs and transmutes external data."
    },
    "Mars": {
        "Aries":       "Direct execute-mode. High initiative. Best as a strike-team lead.",
        "Taurus":      "Persistence execute-mode. High torque. Slow start, unstoppable finish.",
        "Gemini":      "Iterative execute-mode. High mental agility. Rapid prototyping specialist.",
        "Cancer":      "Defensive execute-mode. Driven by security and loyalty-backed targets.",
        "Leo":         "Visibility execute-mode. High performance. Driven by stakes and recognition.",
        "Virgo":       "Audit execute-mode. Driven by precision and error-reduction.",
        "Libra":       "Collaboration execute-mode. Driven by strategic alliances and team morale.",
        "Scorpio":     "Stealth execute-mode. High leverage. Operates best under pressure.",
        "Sagittarius": "Purpose-led execute-mode. Driven by vision and scale. Unstoppable when aligned.",
        "Capricorn":   "Institutional execute-mode. Driven by status and long-range structural wins.",
        "Aquarius":    "System execute-mode. Driven by logic and collective impact.",
        "Pisces":      "Intuitive execute-mode. Driven by flow and creative timing."
    },
    "Jupiter": {
        "Aries":       "Scale through initiative. Every new launch is a high-yield teacher.",
        "Taurus":      "Scale through assets. Wealth and knowledge accumulation is steady and tangible.",
        "Gemini":      "Scale through networks. Information arbitrage and dialogue drive expansion.",
        "Cancer":      "Scale through foundations. Growth is rooted in family and high-trust circles.",
        "Leo":         "Scale through platforms. Leadership and visibility are your primary expanders.",
        "Virgo":       "Scale through mastery. Excellence in service and process drive ROI.",
        "Libra":       "Scale through alliances. Your highest ROI opportunities arrive through partners.",
        "Scorpio":     "Scale through depth. Transformation and crisis-management reveal new wisdom.",
        "Sagittarius": "Scale through systems. Global reach and philosophical reach drive growth.",
        "Capricorn":   "Scale through structure. Recognition and seniority come through duration.",
        "Aquarius":    "Scale through impact. Collective progress and visionary logic drive expansion.",
        "Pisces":      "Scale through vision. Imagination and sensing are your greatest growth-engines."
    },
    "Saturn": {
        "Aries":       "Discipline in strategy. Learning to slow down is the primary life-lesson.",
        "Taurus":      "Discipline in security. Master wealth and stability through sustained effort.",
        "Gemini":      "Discipline in depth. Focus your mental agility into specialized mastery.",
        "Cancer":      "Discipline in boundaries. Build resilience by protecting your internal bandwidth.",
        "Leo":         "Discipline in authority. Lead without needing validation or applause.",
        "Virgo":       "Discipline in audit. Precision and service yield permanent results.",
        "Libra":       "Discipline in equity. Build lasting partnerships through strict fairness.",
        "Scorpio":     "Discipline in surrender. Acceptance of change is your ultimate power.",
        "Sagittarius": "Discipline in truth. Wisdom through testing and questioning belief-systems.",
        "Capricorn":   "Discipline in legacy. Consistent effort yields institutional authority.",
        "Aquarius":    "Discipline in systems. Build impact within and across organizational structures.",
        "Pisces":      "Discipline in grounding. Fix non-linear vision into durable output."
    }
}

# ---------------------------------------------------------------------------
# "Normal" Language Interpretation Layer
# ---------------------------------------------------------------------------

HOUSE_MEANINGS = {
    1: {
        "name": "Self & Health", 
        "impact": "Core presence and physical battery.",
        "if_strong": "Natural authority. High trust-coefficient. Leverage for leadership and physical risks.",
        "if_weak": {
            "meaning": "Operational battery-leakage. Identity-matrix friction.",
            "effect": "Low decisional torque. Increased susceptibility to external energy-drain.",
            "resolution": "Implement strict Energy Hygiene. Solar-alignment (Morning Sun). Prioritize vital posture and decisional boundaries."
        },
        "remedy": "Solar alignment. Early morning light exposure. Focus on vital posture."
    },
    2: {
        "name": "Wealth & Family", 
        "impact": "Asset accumulation and early programming.",
        "if_strong": "High wealth-retention. Optimized for long-term compounding and family legacy.",
        "if_weak": {
            "meaning": "Capital-retention friction. Speech-transmission leakage.",
            "effect": "Revenue-leakage via impulse. Domestic-resource instability.",
            "resolution": "Automate savings to bypass impulse. Practice precise, honest speech. Keep silver in contact with wealth-zones."
        },
        "remedy": "Keep silver in contact with wealth. Practice precise, honest speech."
    },
    3: {
        "name": "Effort & Communication", 
        "impact": "Courage, initiative, and peer-networks.",
        "if_strong": "High-execution bias. Excels in short-range projects, writing, and hands-on builds.",
        "if_weak": {
            "meaning": "Initiative inertia. Connectivity-friction in short-range projects.",
            "effect": "Start-stop execution cycle. Peer-network entropy.",
            "resolution": "Initialize high-torque physical training. Partner with high-velocity peer groups. Execute on Wednesdays."
        },
        "remedy": "Intense physical training. Action-oriented output on Wednesdays."
    },
    4: {
        "name": "Home & Peace", 
        "impact": "Emotional infrastructure and fixed assets.",
        "if_strong": "Deep stability. High property-coefficient. Secure inner-foundation by default.",
        "if_weak": {
            "meaning": "Infrastructure volatility. Foundation-entropy.",
            "effect": "Restless internal state. High-friction in domestic or fixed-asset acquisition.",
            "resolution": "Environment Design optimization. Create tech-free zones. North-quadrant water-element alignment."
        },
        "remedy": "Water-element alignment in the North. Support maternal figures."
    },
    5: {
        "name": "Intellect & Creativity", 
        "impact": "Speculative logic and legacy-creation.",
        "if_strong": "High-precision intuition. Excels in speculation and complex creative solutions.",
        "if_weak": {
            "meaning": "Logic-fog. Speculative-entropy.",
            "effect": "Decision-delays. Misalignment in complex creative or educational cycles.",
            "resolution": "Implement rigorous checklist-systems. Support educational initiatives. Saffron-tilak alignment."
        },
        "remedy": "Saffron-tilak alignment. Support educational initiatives."
    },
    6: {
        "name": "Daily Work & Adversity", 
        "impact": "Operations, debt, and competition.",
        "if_strong": "High resilience. Thrives on competition. Optimized for managing complex operations.",
        "if_weak": {
            "meaning": "Operational friction. Resistance-gap.",
            "effect": "Low friction-tolerance. Debt-leakage risk. Systemic clutter in daily workflow.",
            "resolution": "Zero-clutter workspace audit. Prioritize gut-health. Maintain strict debt-hygiene."
        },
        "remedy": "Support service animals. Maintain a zero-clutter workspace."
    },
    7: {
        "name": "Partnerships & Public", 
        "impact": "Strategic alliances and public-facing ROI.",
        "if_strong": "Leverage through others. High partnership-coefficient. Excels in public negotiation.",
        "if_weak": {
            "meaning": "Alliance-gap. Boundary-leakage.",
            "effect": "Yield-leakage in public negotiation. Energy-drain through unoptimized partnerships.",
            "resolution": "Strict legal and emotional contract-audits. Daily premium fragrance alignment. White-element donations."
        },
        "remedy": "White-element donations. Daily use of premium fragrances."
    },
    8: {
        "name": "Transformation & Secrets", 
        "impact": "Crisis management and hidden resources.",
        "if_strong": "High-volatility tolerance. Excels in research, depth, and managing external assets.",
        "if_weak": {
            "meaning": "Change-inertia. Volatility-friction.",
            "effect": "Low resilience to sudden data-shifts. Crisis-management latency.",
            "resolution": "Initialize intense focused meditation. Align with transformation-cycles. Build deep-roots through spiritual rigor."
        },
        "remedy": "Intense focused meditation. Align with transformation-cycles."
    },
    9: {
        "name": "Fortune & Wisdom", 
        "impact": "Systemic luck and higher-order logic.",
        "if_strong": "High-order networking. Access to elite mentorship and global opportunities.",
        "if_weak": {
            "meaning": "Luck-friction. Mentorship-gap.",
            "effect": "Information-insulation. High systemic resistance in expansion-ventures.",
            "resolution": "Self-driven technical study. Active respect for mentors. Regular knowledge-center immersion."
        },
        "remedy": "Regular visit to knowledge-centers. Active respect for mentors."
    },
    10: {
        "name": "Career & Status", 
        "impact": "Professional authority and public output.",
        "if_strong": "Built for scale. Natural rise to seniority. High institutional-impact coefficient.",
        "if_weak": {
            "meaning": "Visibility-gap. Authority-entropy.",
            "effect": "Unstable professional path. Latency in institutional recognition.",
            "resolution": "Pivot to Niche-Mastery. Focus on specialized skill-stacks. Career-networking for others to build goodwill."
        },
        "remedy": "Employment-networking for others. Clean, high-light work environment."
    },
    11: {
        "name": "Gains & Network", 
        "impact": "Revenue-flow and social net-worth.",
        "if_strong": "High-yield networking. Financial compounding through social circle. 'Midas' ROI.",
        "if_weak": {
            "meaning": "Yield-gap. Network-friction.",
            "effect": "Unsupportive social circle. Revenue-leakage via social commitments.",
            "resolution": "Quality-over-quantity pivot. Nurture top 3 strategic influencers. Strategic charitable giving on Saturdays."
        },
        "remedy": "Strategic charitable giving on Saturdays. Support siblings."
    },
    12: {
        "name": "Expenses & Growth", 
        "impact": "Revenue leakage and inner-scaling.",
        "if_strong": "Global-scale energy. High-efficiency 'letting go'. Optimized for foreign/remote ROI.",
        "if_weak": {
            "meaning": "Hidden-leakage. Resource-entropy.",
            "effect": "Disturbed rest-cycles. Financial/Legal leakage via unmonitored vectors.",
            "resolution": "Voluntary charity as a strategic shield. South-facing rest alignment. Support hospital/blind-care."
        },
        "remedy": "South-facing rest alignment. Support hospital/blind-care."
    }
}

SIGN_THEMES = {
    "Aries":       {"theme": "Direct Execution",     "energy": "High Torque",         "daily": "Immediate-action window. Skip the permission-phase. Execute the boldest item on your stack now."},
    "Taurus":      {"theme": "Value Compounding",    "energy": "Steady torque",        "daily": "Low-velocity, high-impact day. Build for next year, not next week. Stick to the proven routine."},
    "Gemini":      {"theme": "Data Processing",      "energy": "High Bandwidth",      "daily": "Signal-capture day. Follow high-interest conversations. One interaction may trigger a Q3 pivot."},
    "Cancer":      {"theme": "Intuition-Led Ops",    "energy": "Sub-text Radar",      "daily": "Trust non-linear signals. Logical proof is lagging; move based on gut-security. Optimize home-base."},
    "Leo":         {"theme": "Strategic Visibility", "energy": "Central Authority",   "daily": "Visibility-window. Your authority is the primary leverage today. Direct the room; don't hide."},
    "Virgo":       {"theme": "Process Audit",        "energy": "Precision Logic",     "daily": "Zero-error window. Victory through micro-details. One deliberate, optimized act outweighs 10 fast ones."},
    "Libra":       {"theme": "Strategic Alignment",  "energy": "Diplomatic Leverage", "daily": "Decision-point in a complex balance. Opt for the truthful move, not the popular one. Renegotiate terms."},
    "Scorpio":     {"theme": "Deep Data",            "energy": "Hidden Leverage",     "daily": "Senses sub-surface agendas. You are likely correct. Go deeper; the real ROI isn't visible yet."},
    "Sagittarius": {"theme": "Global Scale",         "energy": "Expansion Logic",     "daily": "Big-picture window. Say yes to the 'too big' opportunity. Growth is found in the furthest reach."},
    "Capricorn":   {"theme": "Execution Endurance",  "energy": "Structural Torque",   "daily": "Compounding-day. Results are lagging but the work is landing. Showing up is 90% of the win today."},
    "Aquarius":    {"theme": "Systems Innovation",   "energy": "Original Logic",      "daily": "Share the disruptive idea. Convention is the bottleneck. You don't need a consensus to proceed."},
    "Pisces":      {"theme": "Non-linear Signal",    "energy": "Fluid Flow",          "daily": "Logic is the secondary tool today. Allow imagination to run. Breakthroughs arrive in the quiet gaps."}
}

SIGN_NATAL = {
    "Aries":       "Natural first-mover. High initiative, high velocity. You initiate ground-breaks where others hesitate.",
    "Taurus":      "Durable builder. Master of material compounding and loyalty-backed builds. You prioritize longevity.",
    "Gemini":      "Bridge-builder. High-bandwidth mind. You connect disparate concepts and networks effortlessly.",
    "Cancer":      "Protective-anchor. High atmospheric sensing. Your instinct is the ultimate security-radar for the team.",
    "Leo":         "Heart-led authority. Warmth-driven leadership. You contribute through presence and creative courage.",
    "Virgo":       "Precision-expert. Gap-closer. You detect and fix the systemic leaks that everyone else ignores.",
    "Libra":       "Equilibrium-expert. Natural diplomat. You harmonize complex friction and restore team balance.",
    "Scorpio":     "Truth-seeker. Unafraid of depth. You transform situations by facing the data that others avoid.",
    "Sagittarius": "Meaning-seeker. Scale-driven mind. You hunt for truth and adventure in the big-picture quest.",
    "Capricorn":   "Endurance-master. Long-range builder. You play the 10-year game with structural patience.",
    "Aquarius":    "Future-seer. Systems-innovator. Your original logic makes radical progress possible.",
    "Pisces":      "Non-linear sensor. High empathy. You perceive the subtle shifts that logic alone will miss."
}

PLANET_ARCHETYPES = {
    "Sun":     {"label": "Core Identity",              "focus": "Authority"},
    "Moon":    {"label": "Mindset",                    "focus": "Processing"},
    "Mars":    {"label": "Drive",                      "focus": "Execution"},
    "Mercury": {"label": "Logic",                      "focus": "Communication"},
    "Jupiter": {"label": "Growth",                     "focus": "Expansion"},
    "Venus":   {"label": "Value",                      "focus": "Relationships"},
    "Saturn":  {"label": "Discipline",                 "focus": "Legacy"},
    "Rahu":    {"label": "Ambition",                   "focus": "Innovation"},
    "Ketu":    {"label": "Mastery",                    "focus": "Insight"}
}

DASHA_THEMES = {
    "Sun":     {"life": "Visibility chapter. High personal authority. Time to step into central leadership and define your brand.", "focus": "Authority & Identity"},
    "Moon":    {"life": "Internal chapter. Foundation-building time. Prioritize emotional security and domestic stability over public growth.", "focus": "Internal Foundation"},
    "Mars":    {"life": "High-torque chapter. Immediate execution bias. Great time for launches, competition, and rapid movement.", "focus": "Action & Momentum"},
    "Mercury": {"life": "Intellectual chapter. Data-heavy and networked. Time for deep learning, deals, and high-bandwidth communication.", "focus": "Learning & Data"},
    "Jupiter": {"life": "Expansion chapter. High opportunity-coefficient. Say 'yes' to scale and mentorship. Luck is a tailwind here.", "focus": "Growth & Scale"},
    "Venus":   {"life": "Value-creation chapter. Focus on relationships, aesthetics, and revenue-flow. Creative projects have high ROI.", "focus": "Relationships & Value"},
    "Saturn":  {"life": "Structural chapter. Hard, patient builds. Results are delayed but permanent. Master the mundane daily win.", "focus": "Structure & Legacy"},
    "Rahu":    {"life": "Innovation chapter. High hunger for change. Pivot-ready energy. Follow the 'unfamiliar' path for massive upside.", "focus": "Innovation & Change"},
    "Ketu":    {"life": "Mastery chapter. Inward scaling. Time to let go of expired commitments and focus on deep-niche expertise.", "focus": "Insight & Mastery"}
}

AD_STRATEGIES = {
    "Sun":     "Assert leadership. Visibility is your primary leverage right now.",
    "Moon":    "Trust intuitive signals. Your internal radar is the most reliable data today.",
    "Mars":    "Move fast. Execution speed beats perfection in this window.",
    "Mercury": "Execute the deal. Communication lines are clear and optimized.",
    "Jupiter": "Scale up. This window allows for expansion that won't be available later.",
    "Venus":   "Optimize the alliance. Your social capital is your highest ROI asset today.",
    "Saturn":  "Master the boring. Excellence in small tasks leads to a systemic win.",
    "Rahu":    "Test the unconventional. The high-risk, high-reward path has current support.",
    "Ketu":    "Prune the stack. Drop one draining commitment to reclaim bandwidth."
}

DAILY_ACTIONS = {
    "Aries":       ["Execute one bold move today", "Initiate a high-stakes conversation", "Prioritize speed over consensus"],
    "Taurus":      ["Audit one process for durability", "Invest time in long-range builds", "Optimize for physical comfort"],
    "Gemini":      ["Dialogue with an outlier thinker", "Document a recurring high-value idea", "Capture one new data point"],
    "Cancer":      ["Secure one key relationship", "Optimize your work-from-home environment", "Move based on gut-security"],
    "Leo":         ["Speak with absolute directness", "Take credit for a recent team win", "Display your current WIP publicly"],
    "Virgo":       ["Perform a micro-audit of one task", "Let go of an inefficient standard", "Focus on process optimization"],
    "Libra":       ["Close a pending negotiation", "Balance a friction-heavy alliance", "State your needs without softening"],
    "Scorpio":     ["Investigate a hidden bottleneck", "Release a legacy grudge for bandwidth", "Perform deep, focused data-work"],
    "Sagittarius": ["Greenlight a high-scale opportunity", "Consult an expert who inspires growth", "Let a complex problem breathe"],
    "Capricorn":   ["Focus on 90m of deep work", "Deliver on a personal commitment", "Track systemic progress"],
    "Aquarius":    ["Pitch a disruptive concept", "Connect with a systems-thinker", "Carve out space for objective thought"],
    "Pisces":      ["Build a small low-stakes prototype", "Schedule 20m of total silence", "Move based on recent intuitive signal"]
}

# ---------------------------------------------------------------------------
# Impact & Remedial Layer
# ---------------------------------------------------------------------------

_VARSHA_DATA = {
    "Aries": {
        "theme": "Direct Execution & Fresh Starts",
        "what_it_means": "Aries solar-return rises with Mars energy. High-initiative year. Move from planning to launch-mode immediately.",
        "opportunity": "Launch new ventures. Visible leadership. Physical restructuring or relocation.",
        "risk_framework": {
            "meaning": "High-velocity friction. Impatience-leakage.",
            "effect": "Detail-audit failure. Relationship entropy due to excessive force.",
            "resolution": "Implement a 20% deceleration-buffer. Perform redundant audits on all launch-details."
        },
        "focus_areas": ["Career visibility", "Physical energy", "First-mover projects"],
        "remedies": ["Solar alignment", "Red-element focus on Tuesdays", "Audit confrontations for high-torque energy"]
    },
    "Taurus": {
        "theme": "Value Consolidation & Assets",
        "what_it_means": "Venus rules this return. Focus on building durable assets and material compounding.",
        "opportunity": "Long-term financial scaling. Fixed-asset acquisition. Creative projects with high commercial value.",
        "risk_framework": {
            "meaning": "Stagnation-friction. Change-aversion.",
            "effect": "Opportunity-loss through excessive security-seeking. Yield-leakage in stagnant routines.",
            "resolution": "Initialize small controlled volatility tests. Pivot one legacy system to modern tech."
        },
        "focus_areas": ["Savings & Compounding", "Home infrastructure", "Revenue-flow"],
        "remedies": ["Floral environment design", "Venus-alignment on Fridays", "Strategic resource donations"]
    },
    "Gemini": {
        "theme": "Data Networking & Iteration",
        "what_it_means": "Mercury rules this return. High mental bandwidth. Network is the primary engine.",
        "opportunity": "Writing, content-launch, deal-making. Building industry-wide connectivity.",
        "risk_framework": {
            "meaning": "Scattered-focus entropy. High-bandwidth noise.",
            "effect": "Zero closure on projects. Information-overload leading to decisional paralysis.",
            "resolution": "Enforce strict prioritization-rigor. Daily knowledge-capture audit. Delay non-core networking."
        },
        "focus_areas": ["Communication output", "Short-range deals", "Knowledge capture"],
        "remedies": ["Green-element grounding", "Daily rigorous reading", "Wednesday data-donations"]
    },
    "Cancer": {
        "theme": "Inner Infrastructure & Nourishment",
        "what_it_means": "Moon rules this return. Year of inward scaling. Build the secure base first.",
        "opportunity": "Strengthening high-trust bonds. Home-base optimization. Internal healing ROI.",
        "risk_framework": {
            "meaning": "Hyper-sensitivity retreat. Boundary-leakage.",
            "effect": "Inward-looping logic. Reduced visibility in professional domains.",
            "resolution": "Optimize home-office efficiency. Support maternal figures to stabilize foundation. Maintain external-signal logs."
        },
        "focus_areas": ["Emotional security", "Home foundation", "Internal foundation"],
        "remedies": ["Water-element alignment", "Support maternal figures", "Dietary optimization"]
    },
    "Leo": {
        "theme": "Visibility & Authority",
        "what_it_means": "Sun-led return. Visibility-window. The world is auditing your brand; perform.",
        "opportunity": "Public launches. Central leadership. High-confidence brand-building.",
        "risk_framework": {
            "meaning": "Ego-matrix leakage. Recognition-obsession.",
            "effect": "Alienation of support-layers. Brand-friction through over-extension.",
            "resolution": "Lead through service-first logic. Share credit with the support-team. Sunday solar-donations."
        },
        "focus_areas": ["Public reputation", "Creative output", "Executive presence"],
        "remedies": ["Gold-element alignment", "Solar-donations on Sundays", "High-ROI creative work"]
    },
    "Virgo": {
        "theme": "Process Audit & Systems",
        "what_it_means": "Mercury rules this return. Analytical focus. Fix systemic leaks in daily operations.",
        "opportunity": "Health optimization. Skill-upgrades. Process-leveraged efficiency.",
        "risk_framework": {
            "meaning": "Analysis-paralysis. Perfectionism-entropy.",
            "effect": "Missed market-windows. High operational friction in closing projects.",
            "resolution": "Ship the 'good enough' version to capture data. Enforce time-boxes for audit. Vegetable-element donations."
        },
        "focus_areas": ["Operations & Habits", "Work systems", "Deep-skill mastery"],
        "remedies": ["Zero-clutter workspace design", "Vegetable-element donations", "Pre-work logic alignment"]
    },
    "Libra": {
        "theme": "Strategic Alliance & Balance",
        "what_it_means": "Venus rules this return. Growth through others. No solo-projects this year.",
        "opportunity": "New contracts. High-stakes negotiation. Strategic diplomatic leverage.",
        "risk_framework": {
            "meaning": "Decision-indecision. People-pleasing entropy.",
            "effect": "Contractual boundary-leakage. Yield-loss through unoptimized compromise.",
            "resolution": "Audit all legal contracts for absolute clarity. State requirements without softening. Friday revenue-donations."
        },
        "focus_areas": ["Business partnerships", "Legal contracts", "Social net-worth"],
        "remedies": ["White-element focus on Fridays", "Small friction audits", "Friday revenue-donations"]
    },
    "Scorpio": {
        "theme": "Rebirth & Deep Transformation",
        "what_it_means": "Mars/Ketu led return. Stripping of expired commitments. Clearing for the new stack.",
        "opportunity": "Deep research. Financial restructuring. Managing external assets.",
        "risk_framework": {
            "meaning": "Control-obsession friction. Power-struggle noise.",
            "effect": "High interpersonal trust-friction. Crisis-management latency.",
            "resolution": "Initialize total-surrender ROI. Release legacy debt for bandwidth. Saturday oil-donations."
        },
        "focus_areas": ["Joint assets & Debt", "Stack-pruning", "Investigation"],
        "remedies": ["Intense focused meditation", "Saturday oil-donations", "Avoid revenge-driven ROI"]
    },
    "Sagittarius": {
        "theme": "Global Scale & expansion",
        "what_it_means": "Jupiter rules this return. Stretching the range. Opportunities from non-obvious vectors.",
        "opportunity": "Global travel. Education. Publishing. High-range perspective projects.",
        "risk_framework": {
            "meaning": "Expansion-friction. Over-commitment noise.",
            "effect": "Yield-leakage in unmanageable targets. Strategic dilution.",
            "resolution": "Limit expansion-targets to top 3 vectors. Enforce strict resource-allocation audit. Yellow-element donations."
        },
        "focus_areas": ["Learning systems", "International reach", "Higher-order logic"],
        "remedies": ["Visit knowledge-centers", "Active mentor-support", "Yellow-element donations"]
    },
    "Capricorn": {
        "theme": "Institutional Achievement & Legacy",
        "what_it_means": "Saturn rules this return. High-stakes endurance. Gains are proportional to effort.",
        "opportunity": "Career advancement. Building permanent institutions. High-responsibility roles.",
        "risk_framework": {
            "meaning": "Achievement-rigidity friction. Isolation-leakage.",
            "effect": "Burnout-cycle onset. Crowding out of necessary recovery-data.",
            "resolution": "Schedule mandatory recovery-blocks. Delegate non-institutional tasks. Black-element donations."
        },
        "focus_areas": ["Professional standing", "Structural builds", "Discipline"],
        "remedies": ["Saturday morning execution-blocks", "Black-element donations", "Audit shortcuts"]
    },
    "Aquarius": {
        "theme": "Innovation & Systemic Change",
        "what_it_means": "Saturn/Rahu led return. Breaking tradition. Leverage disruptive logic for progress.",
        "opportunity": "Tech innovation. Social-impact scaling. Collective networking.",
        "risk_framework": {
            "meaning": "Rebellion-friction. Support-infrastructure noise.",
            "effect": "Alienation of necessary allies. Fragmented system-builds.",
            "resolution": "Align disruptive logic with collective ROI. Maintain standard communication protocols. Blue-element focus."
        },
        "focus_areas": ["Collective systems", "Innovation", "Impact ROI"],
        "remedies": ["Engage with community ROI", "Blue-element focus on Saturdays", "In-person data-alignment"]
    },
    "Pisces": {
        "theme": "Intuitive Insight & Surrender",
        "what_it_means": "Jupiter/Ketu led return. Inner scaling. Quiet gathering of next-cycle fuel.",
        "opportunity": "Creative prototypes. Spiritual practice ROI. Healing-layer work.",
        "risk_framework": {
            "meaning": "Boundary-leakage entropy. Escapism noise.",
            "effect": "Operational structure dissolution. Data-insulation from external reality.",
            "resolution": "Enforce strict operational time-boxes. Schedule regular external-reality checks. Gratitude-audit nightly."
        },
        "focus_areas": ["Insight gathering", "Creative vision", "Releasing legacy debt"],
        "remedies": ["Time near water", "Gratitude-audit each evening", "Thursday center-donations"]
    }
}

def get_varshaphal_impact(varshaphal: Dict[str, Any]) -> Dict[str, Any]:
    lagna_raw = varshaphal.get("lagna", {})
    lagna = lagna_raw.get("sign", "") if isinstance(lagna_raw, dict) else str(lagna_raw)
    data = _VARSHA_DATA.get(lagna)
    if not data:
        return {
            "theme": "A year of growth and new chapters.",
            "what_it_means": "Your solar return sets the energetic tone for the year ahead.",
            "opportunity": "Stay open to unexpected directions.",
            "risk": "Resistance to change.",
            "focus_areas": ["Personal growth"],
            "remedies": ["Connect with nature regularly"]
        }
    return data

_D9_MEANINGS = {
    "Aries":       "Soul-level warrior. Inner fire drives purpose despite obstacles. Relationships require independent partners.",
    "Taurus":      "Soul-level stability. Craves beauty and permanence. Spiritual progress through stillness and material grounding.",
    "Gemini":      "Soul-level curiosity. Adaptable and iterative. Dharma involves high-bandwidth communication and exchange.",
    "Cancer":      "Soul-level empathy. Safety-driven mindset. Intuition is the primary spiritual instrument.",
    "Leo":         "Soul-level authority. Built for creative leadership. Core need for visibility and recognition.",
    "Virgo":       "Soul-level precision. Fulfillment through service and detail-audit. Relationships require reliability above all.",
    "Libra":       "Soul-level equilibrium. Drawn to partnership as a mirror. Balance is the primary spiritual lesson.",
    "Scorpio":     "Soul-level transformation. Intense reinvention cycles. Relationships require absolute data-transparency.",
    "Sagittarius": "Soul-level expansion. Oriented toward wisdom and scale. Dharma involves teaching or guidance.",
    "Capricorn":   "Soul-level structure. Values discipline and legacy. Growth through sustained duration and effort.",
    "Aquarius":    "Soul-level innovation. Wired for collective progress. Optimized for intellectual or systems-level logic.",
    "Pisces":      "Soul-level sensing. Deeply intuitive and spiritually porous. Requires strict emotional boundaries.",
}

_D10_MEANINGS = {
    "Aries":       "Public-life pioneer. Known for first-mover launches and front-line leadership.",
    "Taurus":      "Career legacy of reliability. Seen as a value-creator and asset-builder. Resource management focus.",
    "Gemini":      "Market mark through ideas and connectivity. mark in media, sales, or networked education.",
    "Cancer":      "Career mark as a protector. Mark through management, public service, or organizational care.",
    "Leo":         "Professional identity tied to visibility. remembered for executive presence and creative command.",
    "Virgo":       "Reputation built on precision. Legacy in operations, research, or quality-audit management.",
    "Libra":       "Legacy of fairness and aesthetic judgment. Mark in law, design, or high-stakes negotiation.",
    "Scorpio":     "Career involves deep investigation. Crisis management, research, or hidden-asset management focus.",
    "Sagittarius": "Public legacy of knowledge and expansion. Global entrepreneurship, consulting, or publishing focus.",
    "Capricorn":   "Sustained rise to authority. Builder of permanent institutions and systemic structures.",
    "Aquarius":    "Known for disruptive innovation. Legacy of social-impact or technological breakthroughs.",
    "Pisces":      "Career legacy of vision and creativity. Drawn to spiritual, humanitarian, or artistic dimensions.",
}

def get_divisional_impact(d9: Dict, d10: Dict) -> Dict:
    d9_lagna = d9.get("lagna", "Aries")
    d10_lagna = d10.get("lagna", "Aries")
    return {
        "d9_impact": _D9_MEANINGS.get(d9_lagna, "Your inner quality is defined by stability and purpose."),
        "d10_impact": _D10_MEANINGS.get(d10_lagna, "Your professional path is set for leadership and growth."),
    }

# ---------------------------------------------------------------------------
# Core Translation Logic
# ---------------------------------------------------------------------------

def detect_stellium(planets: Dict[str, Any]) -> str:
    sign_planets: Dict[str, List[str]] = {}
    for name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if name in planets:
            sign = planets[name]["sign"]
            sign_planets.setdefault(sign, []).append(name)

    for sign, group in sign_planets.items():
        if len(group) >= 3:
            pl_str = ", ".join(group[:-1]) + " and " + group[-1]
            return f"Stellium in {sign}: {pl_str}. High-density focus on {sign} themes. Significant operational edge in this domain."
    return ""


def get_retrograde_note(transit_planets: Dict[str, Any]) -> Dict[str, str]:
    retro = [n for n in ["Mercury", "Mars", "Jupiter", "Venus", "Saturn"]
             if transit_planets.get(n, {}).get("is_retrograde")]
    if not retro:
        return {
            "meaning": "Direct-motion window. High forward momentum.",
            "effect": "Low resistance for new launches and outward expression.",
            "resolution": "Execute high-torque initiatives. Accelerate expansion-cycles."
        }
    
    if "Mercury" in retro:
        return {
            "meaning": "Solar-Mercurial synchronization friction. High communication-latency.",
            "effect": "Audit-delays and contract-friction. Increased noise in data-transmission.",
            "resolution": "Delay high-stakes agreements. Perform redundant audits on all data-outputs."
        }
    
    names = " and ".join(retro)
    verb = "is" if len(retro) == 1 else "are"
    return {
        "meaning": f"{names} {verb} in apparent retrograde. Internal-scaling window.",
        "effect": "Systemic entropy if expansion is forced. Focus turns to process-audit.",
        "resolution": "Arrest the entropy. Prioritize structural debt-clearing over new builds."
    }


def generate_directive(md_lord: str, ad_lord: str, transit_planets: Dict[str, Any],
                       natal_moon_sign: str = None) -> str:
    ad_strategy = AD_STRATEGIES.get(ad_lord, "")
    retro_fw    = get_retrograde_note(transit_planets)
    
    parts = []
    if md_lord and ad_lord and ad_strategy:
        parts.append(f"In your {md_lord}-{ad_lord} cycle: {ad_strategy}")

    if natal_moon_sign:
        moon_trait = SIGN_THEMES.get(natal_moon_sign, {}).get("energy", "")
        if moon_trait:
            parts.append(f"Natal {natal_moon_sign} Moon ({moon_trait}): Primary processing style.")

    # Convert retrograde dict to high-density string for the brief pointer
    parts.append(f"{retro_fw['meaning']} {retro_fw['resolution']}")

    return " ".join(parts)


def generate_coach_insights(natal_planets: Dict[str, Any], lagna: Dict[str, Any],
                             transit_planets: Dict[str, Any] = None,
                             md_lord: str = None, ad_lord: str = None) -> Dict[str, Any]:
    if transit_planets is None:
        transit_planets = natal_planets

    transit_moon_sign = transit_planets["Moon"]["sign"]
    moon_theme = SIGN_THEMES[transit_moon_sign]

    sun_sign = natal_planets["Sun"]["sign"]
    lagna_sign = lagna["sign"]
    natal_moon_sign = natal_planets["Moon"]["sign"]

    stellium_note = detect_stellium(natal_planets)

    def _planet_card(planet: str, sign: str, house: int) -> Dict[str, str]:
        interp = PLANET_SIGN_INTERP.get(planet, {}).get(sign, SIGN_NATAL.get(sign, ""))
        house_domain = HOUSE_SHORT.get(house, "")
        titles = {
            "Sun": "Identity", "Moon": "Mindset",
            "Mars": "Drive", "Jupiter": "Growth", "Saturn": "Discipline"
        }
        title = f"{titles.get(planet, planet)} — {sign}"
        suffix = f" Context: {house_domain}." if house_domain else ""
        return {"title": title, "description": interp + suffix}

    sun_house  = get_house(sun_sign, lagna_sign)
    moon_house = get_house(natal_moon_sign, lagna_sign)

    superpowers = [
        _planet_card("Sun",  sun_sign,        sun_house),
        _planet_card("Moon", natal_moon_sign, moon_house),
    ]

    for pname in ("Mars", "Jupiter", "Saturn"):
        if pname in natal_planets:
            ps = natal_planets[pname]["sign"]
            ph = get_house(ps, lagna_sign)
            superpowers.append(_planet_card(pname, ps, ph))

    if stellium_note:
        superpowers.append({"title": "Power-Spot", "description": stellium_note})

    directive = generate_directive(md_lord, ad_lord, transit_planets, natal_moon_sign)

    return {
        "daily_theme": moon_theme["theme"],
        "energy_signature": f"Moon in {transit_moon_sign} · {moon_theme['energy']}",
        "uplift_narrative": moon_theme["daily"],
        "superpowers": superpowers,
        "operational_pointer": directive,
        "daily_actions": DAILY_ACTIONS.get(transit_moon_sign, []),
        "natal_moon_sign": natal_moon_sign
    }


def generate_business_pulse(dashas: List[Dict], current_date: datetime) -> Dict[str, Any]:
    date_str = current_date.strftime("%Y-%m-%d")

    active_md = next((d for d in dashas if d["start"] <= date_str <= d["end"]), dashas[0])
    active_ad = next((b for b in active_md["bhuktis"] if b["start"] <= date_str <= b["end"]), active_md["bhuktis"][0])

    md_lord = active_md["lord"]
    ad_lord = active_ad["lord"]

    md_theme = DASHA_THEMES.get(md_lord, {"life": "", "focus": ""})
    ad_strategy = AD_STRATEGIES.get(ad_lord, "")

    strategy = f"{md_theme['life']} Current imperative: {ad_strategy}"

    return {
        "active_dasha": f"{md_lord}-{ad_lord}",
        "display_dasha": f"{md_lord} Major Chapter · {ad_lord} Sub-Chapter",
        "focus": md_theme["focus"],
        "target_kpi": f"{md_lord} · {ad_lord} cycle",
        "strategy": strategy
    }



def get_cosmic_schedule_advice(events: List[Dict], transit_planets: Dict[str, Any], active_dasha_lord: str = "") -> List[Dict]:
    advice_list = []
    mercury_retro = transit_planets.get("Mercury", {}).get("is_retrograde", False)
    
    dasha_risk_map = {
        "Saturn": ["negotiation", "contract", "legal", "closure"],
        "Rahu":   ["innovation", "new venture", "tech", "pitch"],
        "Mars":   ["execution", "action", "launch", "competition"],
        "Mercury": ["sales", "communication", "writing", "agreement"]
    }

    for event in events:
        summary = event.get("summary", "")
        is_high_stakes = event.get("is_high_stakes", False)
        summary_lower = summary.lower()

        if mercury_retro and any(kw in summary_lower for kw in ["negotiation", "contract", "legal", "sign"]):
            advice_list.append({
                "event": summary,
                "risk": "High",
                "reason": "Mercury Retrograde affects agreements.",
                "action": "Audit all details. Postpone signing if possible."
            })
            continue

        relevant_keywords = dasha_risk_map.get(active_dasha_lord, [])
        synergy_found = any(kw in summary_lower for kw in relevant_keywords)

        if synergy_found:
            advice_list.append({
                "event": summary,
                "risk": "Low",
                "reason": f"{active_dasha_lord} cycle synergy.",
                "action": "Proceed. High cosmic support for this activity."
            })
            continue

        if is_high_stakes:
            advice_list.append({
                "event": summary,
                "risk": "Moderate",
                "reason": "High-stakes event during neutral window.",
                "action": "Maintain focus. Standard operational rigor required."
            })

    return advice_list
