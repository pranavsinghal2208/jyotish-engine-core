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
        "name": "Self & Vitality", 
        "impact": "Your physical energy, presence, and personal boundaries.",
        "if_strong": "Natural confidence, high stamina, and clear self-direction. Perfect for leading others and taking bold leaps.",
        "if_weak": {
            "meaning": "Physical fatigue, low motivation, or feeling easily drained by other people's stress.",
            "effect": "Struggles with self-starting, self-doubt, or losing track of your own goals.",
            "resolution": "Implement solid energy hygiene. Protect your boundaries, stand tall, and get early morning sun to recharge."
        },
        "remedy": "Solar alignment. Secure early morning sunlight. Maintain a tall, open posture."
    },
    2: {
        "name": "Wealth & Expression", 
        "impact": "Savings, speech, and early family roots.",
        "if_strong": "Durable savings habits, clear and persuasive communication, and deep ancestral pride.",
        "if_weak": {
            "meaning": "Impulsive spending under emotional pressure, or talking too fast when anxious.",
            "effect": "Financial leakages on comfort items, or being misunderstood during sensitive discussions.",
            "resolution": "Set automated savings to bypass impulse buy urges, practice slow and mindful speech, and place a small silver element near your work desk."
        },
        "remedy": "Keep a silver coin on your desk. Practice slow, mindful breathing before speaking."
    },
    3: {
        "name": "Effort & Courage", 
        "impact": "Initiative, micro-projects, and peer networks.",
        "if_strong": "Action-biased execution. Excels in getting things off the ground, writing, and peer connection.",
        "if_weak": {
            "meaning": "Initiative inertia, creative blocks, or constant start-stop routine cycles.",
            "effect": "Procrastination on critical tasks, or feeling distant from your core friends.",
            "resolution": "Start your day with physical movement, break big goals into a single 15-minute micro-action, and schedule collaborative peer work."
        },
        "remedy": "Intense morning physical movement. Check off one micro-goal before noon."
    },
    4: {
        "name": "Home & Inner Peace", 
        "impact": "Maternal bond, emotional battery, and domestic stability.",
        "if_strong": "Deep emotional resilience. A peaceful, supportive home environment that acts as your anchor.",
        "if_weak": {
            "meaning": "Restless thoughts, feeling unsettled in your body, or tension in your private space.",
            "effect": "Anxiety during downtime, or domestic distractions that pull you away from focus.",
            "resolution": "Establish tech-free evening wind-down hours, declutter your private space, and place a small glass bowl of fresh water in the quietest north corner of your bedroom to absorb stress."
        },
        "remedy": "Bowl of fresh water in the North corner of your room. Dedicate quality time to maternal figures today."
    },
    5: {
        "name": "Creativity & Instinct", 
        "impact": "Creative flow, learning, and gut intuition.",
        "if_strong": "High creative confidence, sharp intuitive foresight, and a natural capacity to learn complex skills.",
        "if_weak": {
            "meaning": "Analytical overthinking, mental fog, or second-guessing your gut instincts.",
            "effect": "Creative blocks, decision fatigue, or feeling disconnected from play and joy.",
            "resolution": "Implement simple structured checklists, support a local educational cause, and apply a touch of sandalwood or saffron scent to clear the mind."
        },
        "remedy": "Sandalwood scent to ground thoughts. Dedicate 15 minutes to pure, unstructured reading."
    },
    6: {
        "name": "Daily Routine & Resilience", 
        "impact": "Work habits, health, and overcoming obstacles.",
        "if_strong": "High discipline, strong health hygiene, and a natural ability to solve crises under pressure.",
        "if_weak": {
            "meaning": "Clutter in your schedule, low physical battery, or feeling overwhelmed by minor chores.",
            "effect": "Avoidance of daily tasks, gut sensitivity, or letting small administrative issues pile up.",
            "resolution": "Do a thorough 10-minute desk declutter, prioritize raw/light foods for gut health, and avoid short-term debt."
        },
        "remedy": "Clean your desk completely. Support service or shelter animals."
    },
    7: {
        "name": "Partnerships & Alliances", 
        "impact": "Primary relationships—your spouse/partner and co-founders.",
        "if_strong": "Harmonious collaborations, balanced boundaries, and deep mutual trust in business and personal life.",
        "if_weak": {
            "meaning": "Unequal compromises, boundary leakages, or communication gaps in your closest circles.",
            "effect": "Feeling unappreciated by your partner, or getting exhausted by public-facing roles.",
            "resolution": "Draft clear, open-hearted agreements with key partners, wear a soothing natural floral fragrance, and dedicate a quiet evening to a deep-listening date."
        },
        "remedy": "Natural floral fragrance. Conduct an open-hearted listening session with a key partner."
    },
    8: {
        "name": "Transformation & Depth", 
        "impact": "Managing unexpected shifts, deep research, and long-term security.",
        "if_strong": "Superb crisis resilience. Highly capable of transmuting difficult moments into personal growth.",
        "if_weak": {
            "meaning": "Resistance to change, fear of sudden shifts, or chronic stress/exhaustion.",
            "effect": "Feeling stuck in outdated situations, or panic when faced with volatility.",
            "resolution": "Practice 5 minutes of quiet box-breathing, let go of what you cannot control, and dive into a research subject that fascinates you."
        },
        "remedy": "5 minutes of quiet box-breathing. Release attachment to the day's outcomes."
    },
    9: {
        "name": "Wisdom & Purpose", 
        "impact": "Higher learning, mentorship, and life perspective.",
        "if_strong": "Aligned sense of purpose, supportive mentors, and an optimistic, big-picture view of your path.",
        "if_weak": {
            "meaning": "Feeling disconnected from a larger purpose, or a lack of real guidance and direction.",
            "effect": "Cynicism, feeling spiritually dry, or struggle in finding expansion opportunities.",
            "resolution": "Nurture connection with a wise elder or mentor, read a chapter from a classic text, and immerse yourself in inspiring knowledge environments."
        },
        "remedy": "Read a page of timeless wisdom. Write down three things you are deeply grateful for."
    },
    10: {
        "name": "Career & Output", 
        "impact": "Professional path, career standing, and public output.",
        "if_strong": "Natural leadership presence, stable career trajectory, and a focus on long-term systemic impact.",
        "if_weak": {
            "meaning": "Feeling invisible or unappreciated at work, or feeling unaligned with your current career track.",
            "effect": "Struggles with motivation at work, or anxiety about public standing.",
            "resolution": "Declutter your workspace to let light in, focus on mastering one highly specialized skills-stack, and network by helping others secure jobs."
        },
        "remedy": "Clean your keyboard and monitor. Brighten your workspace with natural light."
    },
    11: {
        "name": "Gains & Social Connections", 
        "impact": "True friendships, support networks, and social flow.",
        "if_strong": "High-trust friendships, supportive groups, and ease in materializing long-term aspirations.",
        "if_weak": {
            "meaning": "Superficial connections, feeling isolated in crowds, or social circles that drain your battery.",
            "effect": "Wasting energy on social commitments you don't care about, or lack of support from peers.",
            "resolution": "Focus heavily on quality over quantity. Deepen your relationship with your top 3 close friends, and support a charitable cause on Saturdays."
        },
        "remedy": "Support a local community cause on Saturdays. Call an old friend just to check in."
    },
    12: {
        "name": "Rest & Letting Go", 
        "impact": "Sleep quality, letting go of control, and private self-care.",
        "if_strong": "Superb sleep quality, ability to detach and surrender control, and rich inner fantasy/creativity.",
        "if_weak": {
            "meaning": "Disturbed sleep cycles, high nighttime anxiety, or sudden unexpected costs.",
            "effect": "Worrying in the dark, inability to relax, or feeling a drain on your vital reserves.",
            "resolution": "Set up a clean screen-free bedroom environment, sleep with your head facing South to align with electromagnetic fields, and practice voluntary charitable giving."
        },
        "remedy": "Sleep with your head facing South. Do a 15-minute screen-free wind-down routine tonight."
    }
}

SIGN_THEMES = {
    "Aries":       {"theme": "Bold Initiative",      "energy": "Physical battery active", "daily": "A powerful window for bold starts. Skip the doubts, stand tall, and tackle the most challenging conversation or initiative on your plate first."},
    "Taurus":      {"theme": "Steady Growth",        "energy": "Grounded pace",       "daily": "A low-speed, high-impact day. Build for the long haul rather than looking for immediate dopamine wins. Stick to a cozy, supportive routine."},
    "Gemini":      {"theme": "Signal Capture",       "energy": "Mental curiosity",     "daily": "An information-rich day. Follow high-interest conversations and read deeply. A single conversation today could trigger a beautiful personal pivot."},
    "Cancer":      {"theme": "Intuitive Recharge",   "energy": "Sub-text sensitivity",  "daily": "Trust your gut sensations today. If your emotional battery feels low, withdraw slightly to secure your home foundation and family connection."},
    "Leo":         {"theme": "Creative Play",        "energy": "Radiant expression",  "daily": "Command your space with warm, generous energy. Express your creative ideas openly and uplift the people around you with authentic recognition."},
    "Virgo":       {"theme": "Mindful Organization",  "energy": "Detail focus",        "daily": "A perfect day for inner and outer alignment. Declutter your desk, organize your physical space, and forgive yourself for what didn’t get completed yesterday."},
    "Libra":       {"theme": "Harmonious Dialogue",  "energy": "Strategic connection", "daily": "Focus heavily on win-win partnerships. Schedule quiet, deep-listening sessions with close partners or co-founders to rebuild alignment."},
    "Scorpio":     {"theme": "Deep Transmutation",   "energy": "High resilience",     "daily": "A high-intensity day. You are uniquely equipped to process stress and transform volatility into personal power. Let go of what you cannot control."},
    "Sagittarius": {"theme": "Expansive Vision",     "energy": "Big-picture optimism", "daily": "A great day for big-picture thinking and perspective resets. Read wisdom literature, plan long-range journeys, and let go of minor daily annoyances."},
    "Capricorn":   {"theme": "Systemic Grounding",   "energy": "Sustained discipline", "daily": "Durable effort is your superpower today. Put in solid work toward structural foundations, and remember that real mastery takes duration."},
    "Aquarius":    {"theme": "Impact & Networks",    "energy": "Visionary logic",     "daily": "Connect with forward-thinking friends or communities. Look at how your efforts serve the collective good, and explore unique creative ideas."},
    "Pisces":      {"theme": "Flow & Sensing",       "energy": "Fluid sensing",       "daily": "Non-linear thoughts and rich imagination rule today. Do not force logical rigidity; let your mind wander, rest your eyes, and listen to inspiring music."}
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

    # -----------------------------------------------------------------------
    # Gemini-Powered Narrative Synthesis (Unified Executive Briefing)
    # -----------------------------------------------------------------------
    import os
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key:
        try:
            from google import genai as gai
            from google.genai import types
            from pydantic import BaseModel, Field
            from typing import List

            class SuperpowerCard(BaseModel):
                title: str = Field(description="Strategic title of the placement, e.g. 'Identity Drive — Sun in Leo (10H)'")
                description: str = Field(description="1-2 sentences translating this placement into their active strategic asset for today's cycles.")

            class CoachInsightsSchema(BaseModel):
                daily_theme: str = Field(description="Short 2-3 word theme, e.g. 'Structural Arbitrage'")
                energy_signature: str = Field(description="Transit description, e.g. 'Moon in Scorpio · High-Leverage Depth'")
                uplift_narrative: str = Field(description="Unified, 2-3 sentence strategic executive overview providing deep, empathetic, doable clarity.")
                superpowers: List[SuperpowerCard] = Field(description="Exactly 3 dynamic natal placements that are actively triggered by today's cycles.")
                operational_pointer: str = Field(description="1-2 sentence high-stakes daily directive.")
                daily_actions: List[str] = Field(description="Exactly 3 highly specific, actionable operational daily tasks.")

            # Compile raw coordinates to pass in the prompt (No Hallucination Zone)
            natal_str = f"Lagna (Ascendant): {lagna_sign}\n"
            for pname in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
                if pname in natal_planets:
                    ps = natal_planets[pname]["sign"]
                    ph = get_house(ps, lagna_sign)
                    natal_str += f"- {pname} in {ps} ({ph}H)\n"

            transit_str = f"Moon is in {transit_moon_sign}\n"
            retro_planets = [p for p, data in transit_planets.items() if data.get("is_retrograde")]
            if retro_planets:
                transit_str += f"- Retrograde transiting planets: {', '.join(retro_planets)}\n"

            prompt = (
                "Construct a highly personalized, warm, and evocative blended life strategist brief for the user Pranav Singhal.\n"
                "You are the PSBC Personal Executive & Life Coach for Cosmic OS. Speak in a deeply empathetic, soulful, and warm performance-coach voice—like a personal letter from a wise mentor (the 'Micro-Journal' style).\n"
                "The target user is an overwhelmed high-achiever seeking deep emotional clarity and gentle decisional support. Seamlessly blend professional execution (career, co-founder dynamics, capital momentum) and personal well-being (emotional battery, physical rest, family peace).\n"
                "ABSOLUTELY BAN all cold, dry, mechanical, or overly technical jargon (e.g., do not say 'systemic debt', 'operational battery-leakage', 'capital-retention friction', 'speculative-entropy', or 'alignment-gap'). Keep everything clear, relatable, and deeply human.\n\n"
                "Raw Astrological Coordinates (Do not invent or change these facts):\n"
                f"1. Natal Placements:\n{natal_str}\n"
                f"2. Active Dasha Cycle: Major Chapter rules {md_lord}, Sub-Chapter rules {ad_lord} ({md_lord}-{ad_lord} cycle).\n"
                f"3. Today's Sky Transits:\n{transit_str}\n\n"
                "Instructions:\n"
                "- Daily Theme: Synthesize a warm, evocative 2-3 word theme (e.g., 'The Heavy Lift', 'Grounded Focus', 'The Quiet Anchor', 'The Open Door').\n"
                "- Energy Signature: Highlight the primary transit signature in warm, human-first terms.\n"
                "- Uplift Narrative: 2-3 sentences max. Write a beautiful, poetic, yet highly practical message synthesizing their active planetary energies into a highly coherent daily guide. Direct it straight to their emotional/decisional challenges today, providing instant peace and motivating execution.\n"
                "- Superpowers: Highlight exactly 3 natal placements that are currently activated by today's transits or active Dasha. Explain how they can use them as active leverage in both their work and personal connection today, in plain, jargon-free English.\n"
                "- Operational Pointer: A single, high-stakes tactical directive (1-2 sentences) balancing personal peace and work actions.\n"
                "- Daily Actions: Exactly 3 highly specific, actionable daily tasks (life hacks) blending personal harmony and work priorities (e.g. 'Conduct a 15-minute desk declutter to refresh your mind', 'Align terms with your highest-stakes partner over an open, relaxed conversation', 'Spend 5 minutes in quiet box-breathing to reset your physical battery before lunch'). Never use generic placeholders."
            )

            client = gai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=CoachInsightsSchema,
                    temperature=0.2
                ),
            )
            import json
            data = json.loads(response.text)
            
            # Map back to our exact output format
            return {
                "daily_theme": data.get("daily_theme", moon_theme["theme"]),
                "energy_signature": data.get("energy_signature", f"Moon in {transit_moon_sign} · {moon_theme['energy']}"),
                "uplift_narrative": data.get("uplift_narrative", moon_theme["daily"]),
                "superpowers": [dict(s) for s in data.get("superpowers", [])],
                "operational_pointer": data.get("operational_pointer", directive),
                "daily_actions": data.get("daily_actions", DAILY_ACTIONS.get(transit_moon_sign, [])),
                "natal_moon_sign": natal_moon_sign
            }
        except Exception as e:
            # Silent fallback to rule-based system
            print(f"Gemini Synthesis Fallback Triggered: {e}")

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
