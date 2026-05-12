from typing import Dict, Any, List
from datetime import datetime

# ---------------------------------------------------------------------------
# "Normal" Language Interpretation Layer
# ---------------------------------------------------------------------------

HOUSE_MEANINGS = {
    1: {
        "name": "Self & Health", 
        "impact": "Your personality and physical energy.",
        "if_strong": "You have a natural 'presence.' People trust you easily. Use this to lead projects and take physical risks. You bounce back from illness fast.",
        "if_weak": "You might feel easily drained by others. Focus on strict 'Energy Hygiene' — sleep more, avoid energy-vampires, and don't take on too much at once.",
        "remedy": "Offer water to the Sun in the morning. Wear a ruby or red thread on your wrist."
    },
    2: {
        "name": "Wealth & Family", 
        "impact": "Your savings and early family life.",
        "if_strong": "Money tends to stick to you. You have a 'Wealth Container' that doesn't leak. Great for long-term investments and building a family legacy.",
        "if_weak": "Money might come in, but it leaves just as fast. You might feel 'speech-blocked' or disconnected from family. Focus on automated savings — don't trust your impulse.",
        "remedy": "Keep a small silver coin in your wallet. Avoid lying or harsh speech. Chant 'Om Mahalakshmyai Namah'."
    },
    3: {
        "name": "Effort & Hobbies", 
        "impact": "Your courage and self-effort.",
        "if_strong": "You are a 'Doer.' You don't wait for luck; you make it. You excel in short-term projects, writing, and hands-on skills. Your siblings or peers support you.",
        "if_weak": "You might start things with fire but lose steam halfway. You might feel 'courage-poor' when facing big tasks. Partner with high-energy people who can push you.",
        "remedy": "Physical exercise is your best remedy. Donate green items on Wednesdays."
    },
    4: {
        "name": "Home & Peace", 
        "impact": "Your inner peace and home life.",
        "if_strong": "Your home is your sanctuary. You have deep emotional stability and likely own property or vehicles easily. You have a 'Happy Heart' by default.",
        "if_weak": "You might feel restless even in a beautiful house. Inner peace feels like a struggle. Focus on 'Inner Landscaping' — meditation and making your bedroom a tech-free zone.",
        "remedy": "Keep a pot of water in the Northeast of your house. Respect your mother and mother-figures."
    },
    5: {
        "name": "Intellect & Kids", 
        "impact": "Creativity and education.",
        "if_strong": "You have 'Cosmic Luck.' Your gut feelings are 90% right. You excel in speculation, creative arts, and parenting. Solutions come to you in dreams.",
        "if_white": "You might feel 'brain-fog' during big decisions. Education or creative projects might face delays. Use systems and checklists rather than relying on 'luck' or intuition.",
        "remedy": "Apply a saffron (kesar) tilak on your forehead. Help students with their books or fees."
    },
    6: {
        "name": "Daily Work & Health", 
        "impact": "Daily routine and obstacles.",
        "if_strong": "You are a 'Warrior.' Obstacles don't stop you — they train you. You excel at managing debts, winning competitions, and handling high-pressure daily work.",
        "if_weak": "Small problems feel like mountains. You might get sick often from stress. Simplify your life. Don't take loans unless absolutely necessary. Focus on gut health.",
        "remedy": "Feed a black dog on Saturdays. Keep your workplace clutter-free."
    },
    7: {
        "name": "Partnerships & Marriage", 
        "impact": "Your spouse and business partners.",
        "if_strong": "You gain through others. Your partners (life or business) act as your 'Mirror of Growth.' You excel in public-facing roles and negotiations.",
        "if_weak": "Relationships might feel draining or confusing. You might lose your identity in others. Learn to set clear boundaries and don't rush into legal partnerships.",
        "remedy": "Donate white clothes or sweets on Fridays. Use a pleasant fragrance daily."
    },
    8: {
        "name": "Changes & Secrets", 
        "impact": "Sudden ups and downs.",
        "if_strong": "You are 'Unstoppable.' You can handle crises that would break others. You have a gift for research, occult, and managing other people's money.",
        "if_weak": "You might fear change or feel hit by 'sudden bad luck.' Your energy might feel low. Focus on 'Deep Roots' — spiritual practices that keep you grounded during storms.",
        "remedy": "Chant 'Om Namah Shivaya'. Donate oil or black til on Saturdays."
    },
    9: {
        "name": "Fortune & Wisdom", 
        "impact": "Higher learning and good luck.",
        "if_strong": "The 'Divine Hand' is on your shoulder. You find the right teacher at the right time. Travel and higher education bring you massive gains.",
        "if_weak": "Luck might feel like it's 'always next door' but never in your house. You might struggle with traditional beliefs. Focus on 'Self-Study' and practical wisdom over blind faith.",
        "remedy": "Visit a place of worship regularly. Respect your elders and mentors."
    },
    10: {
        "name": "Career & Status", 
        "impact": "Your professional life and status.",
        "if_strong": "You are built for the top. Career growth comes naturally. The world sees you as an authority. Use this power to build institutions, not just jobs.",
        "if_weak": "You might feel 'invisible' at work or struggle to find your true calling. Career paths might be unstable. Focus on 'Niche Mastery' — be so good they can't ignore you.",
        "remedy": "Help people find jobs. Keep a clean, well-lit office space."
    },
    11: {
        "name": "Gains & Social Circle", 
        "impact": "Fulfillment of desires.",
        "if_strong": "You are a 'Wish-Fulfiller.' Your social circle is your net worth. Money and friends come easily. You have the 'Midas Touch' for business networking.",
        "if_weak": "You might work hard but feel the 'Gains' are low. Your social circle might be small or unsupportive. Focus on 'Quality over Quantity' — nurture 2-3 key influencers.",
        "remedy": "Donate to a charity of your choice on Saturdays. Be kind to your elder siblings."
    },
    12: {
        "name": "Expenses & Solitude", 
        "impact": "Spending and inner growth.",
        "if_strong": "You have 'Global Energy.' You excel in foreign lands, hospitals, or spiritual retreats. You know how to 'let go' and move on without baggage.",
        "if_weak": "Money might leak through 'hidden' expenses (medical, legal, or waste). Sleep might be disturbed. Focus on 'Charity as a Shield' — give voluntarily so the universe doesn't take.",
        "remedy": "Sleep with your head toward the South. Donate to hospitals or blind schools."
    }
}

SIGN_THEMES = {
    "Aries":       {"theme": "New Starts",           "energy": "Bold & Ready",        "daily": "You're feeling ready to leap today. Don't wait for permission — that small bold move you've been thinking about is the right one."},
    "Taurus":      {"theme": "Building Value",       "energy": "Slow & Steady",       "daily": "Take your time today. What you build slowly and carefully will last much longer than anything rushed. Stick to your routine."},
    "Gemini":      {"theme": "Quick Ideas",          "energy": "Active Mind",         "daily": "Your mind is racing with signals. Follow that one interesting conversation — it might lead to a big change next month."},
    "Cancer":      {"theme": "Home & Gut Feeling",   "energy": "Strong Intuition",    "daily": "Trust that quiet feeling in your stomach today. You don't need an explanation yet. Spend time in spaces where you feel safe."},
    "Leo":         {"theme": "Warm Leadership",      "energy": "Confident Heart",     "daily": "It's okay to be seen today. Your warmth and generosity are your superpowers right now. Show the world what you're really capable of."},
    "Virgo":       {"theme": "Focus & Care",         "energy": "Quiet Precision",     "daily": "Don't skip the small details today. Giving something your full attention is how you'll win. One small, deliberate act is enough."},
    "Libra":       {"theme": "Fairness & Balance",   "energy": "Graceful Clarity",    "daily": "That situation you've been balancing is ready for a decision. You don't have to pick a side, just pick what's true. Be honest but gentle."},
    "Scorpio":     {"theme": "Deep Truths",          "energy": "Inner Knowing",       "daily": "You can sense what others aren't saying. You're probably right. Go deeper today — the real answer isn't on the surface."},
    "Sagittarius": {"theme": "Big Picture",          "energy": "Optimistic Spirit",   "daily": "Something bigger is trying to reach you. Say yes to the thing that feels slightly too big or too far. That's where your growth is."},
    "Capricorn":   {"theme": "Patient Progress",     "energy": "Calm Endurance",      "daily": "The hard work is paying off, even if you can't see it yet. Stay on your path. Just showing up today is a massive win."},
    "Aquarius":    {"theme": "New Thinking",         "energy": "Original Ideas",      "daily": "That 'weird' idea you have? It's actually ahead of its time. Share it. You don't need someone else to tell you it's okay."},
    "Pisces":      {"theme": "Dreaming & Sensing",   "energy": "Gentle Flow",         "daily": "Logic matters less than how you feel today. Let your imagination run. The answer you're looking for will come in the quiet moments."}
}

SIGN_NATAL = {
    "Aries":       "You're a natural-born leader who likes to move first. You have a fire in you that wants to break new ground and get things moving.",
    "Taurus":      "You have the rare gift of patience. You know how to build things that actually last, and you're incredibly loyal to the people you care about.",
    "Gemini":      "Your mind is a bridge between different worlds. You can connect people and ideas that others wouldn't even think to put together.",
    "Cancer":      "You're the protector. You can feel the 'vibe' of any room instantly, and your deep instinct is to make everyone feel safe and cared for.",
    "Leo":         "You lead with your heart. Your warmth and generosity aren't just personality traits — they're the way you make the world a better place.",
    "Virgo":       "You're the one who makes things perfect. You see the gaps that others miss and you close them with care and quiet precision.",
    "Libra":       "You have a natural sense of fairness. You're the one who can make a messy situation feel balanced and a broken team feel whole again.",
    "Scorpio":     "You're unafraid of the deep stuff. You can handle the truth, no matter how hard it is, and you have the power to transform any situation.",
    "Sagittarius": "You're a seeker of truth. You have a hunger for meaning and adventure that keeps you moving toward the big, important things in life.",
    "Capricorn":   "You have incredible endurance. You're building something for the long term, and you have the patience to see it through to the end.",
    "Aquarius":    "You see the future. You know that the world can be different, and your original thinking is what makes real change possible.",
    "Pisces":      "You feel what others can't. Your sensitivity is your greatest strength — it lets you see things that logic alone will always miss."
}

PLANET_ARCHETYPES = {
    "Sun":     {"label": "The Real You",               "focus": "Who you are"},
    "Moon":    {"label": "Your Mindset",               "focus": "How you feel"},
    "Mars":    {"label": "Your Drive",                 "focus": "How you act"},
    "Mercury": {"label": "Mind & Logic",               "focus": "How you think"},
    "Jupiter": {"label": "Your Growth",                "focus": "How you expand"},
    "Venus":   {"label": "Love & Money",               "focus": "What you value"},
    "Saturn":  {"label": "Your Discipline",            "focus": "Your legacy"},
    "Rahu":    {"label": "Your Ambition",              "focus": "New goals"},
    "Ketu":    {"label": "Your Mastery",               "focus": "Deep wisdom"}
}

DASHA_THEMES = {
    "Sun":     {"life": "This chapter is all about you — who you are, what you want to be known for, and stepping into your own light.", "focus": "Purpose & Identity"},
    "Moon":    {"life": "This is a quiet, internal time. Your home and how you feel inside matter more right now than what the world thinks of you.", "focus": "Feelings & Home"},
    "Mars":    {"life": "This is a high-energy chapter. You'll feel the urge to act fast and build big. It's a great time to move before you're 'ready'.", "focus": "Action & Momentum"},
    "Mercury": {"life": "Your brain is in high gear. This is a time for learning, talking, and connecting your ideas with the world.", "focus": "Learning & Connection"},
    "Jupiter": {"life": "Doors are opening for you. This is a lucky chapter where things seem to fall into place. Say 'yes' to big opportunities.", "focus": "Growth & Luck"},
    "Venus":   {"life": "This chapter is about love, comfort, and the good things in life. Your relationships and creative projects take center stage.", "focus": "Love & Creativity"},
    "Saturn":  {"life": "This is the time for hard, patient work. What you build now will last forever. Just keep showing up every single day.", "focus": "Discipline & Hard Work"},
    "Rahu":    {"life": "You'll feel a huge hunger for change and new goals. You might move to a new place or start a totally different career. Follow the hunger.", "focus": "Ambition & Change"},
    "Ketu":    {"life": "This is a time to look inward and master what you already know. Let go of what you don't need anymore and focus on your inner peace.", "focus": "Inner Peace & Mastery"}
}

AD_STRATEGIES = {
    "Sun":     "Step into a leadership role you've been thinking about. People can see you clearly right now — use that attention.",
    "Moon":    "Trust that gut feeling you keep having. Your intuition is your best guide in this window.",
    "Mars":    "Stop planning and start doing. Moving fast is more important than being perfect right now.",
    "Mercury": "Write that email, send that text, or sign that deal. Communication is crystal clear for you right now.",
    "Jupiter": "Say yes to that one big opportunity. This window opens doors that might not stay open forever.",
    "Venus":   "Spend time with someone you care about — just to connect. Your relationships are your biggest asset today.",
    "Saturn":  "Finish that one boring task you've been putting off. Doing the small things right will lead to a massive win later.",
    "Rahu":    "Try something totally new, even if it feels a bit scary. The 'unfamiliar' path is where your luck is right now.",
    "Ketu":    "Drop one commitment that's draining your energy. Focus only on what's truly essential to you."
}

DAILY_ACTIONS = {
    "Aries":       ["Do that one bold thing you've been putting off", "Be the first one to start a conversation today", "Stop overthinking and just move"],
    "Taurus":      ["Take care of one task slowly and perfectly", "Invest time in something that will still matter next year", "Enjoy a real moment of comfort — you've earned it"],
    "Gemini":      ["Talk to someone who thinks differently than you", "Write down that one recurring idea", "Learn one new thing today"],
    "Cancer":      ["Check in on a friend you've been thinking about", "Spend time in a place where you feel totally safe", "Trust your gut feeling today"],
    "Leo":         ["Say exactly what you mean, don't soften it", "Be proud of how much you've been carrying lately", "Show someone what you're working on"],
    "Virgo":       ["Focus on just one task and do it with full care", "Let go of a standard that's just exhausting you", "Notice what's working well in your life"],
    "Libra":       ["Make that decision you've been balancing", "Fix a relationship that really matters to you", "Ask for exactly what you need today"],
    "Scorpio":     ["Look into that one thing everyone else is ignoring", "Let go of an old grudge — it's costing you too much", "Do the deep work today"],
    "Sagittarius": ["Say yes to a big, slightly scary opportunity", "Spend time with someone who inspires you to grow", "Don't try to solve everything today — just let it breathe"],
    "Capricorn":   ["Spend 90 minutes on your most important work", "Keep a promise you made to yourself", "Notice the small progress you've made"],
    "Aquarius":    ["Share your 'weird' idea with someone", "Connect with an original thinker", "Give yourself some space to just think"],
    "Pisces":      ["Create something small just for fun", "Spend 20 minutes in total silence", "Trust the intuition you've been having lately"]
}

# ---------------------------------------------------------------------------
# Impact & Remedial Layer
# ---------------------------------------------------------------------------

_VARSHA_DATA = {
    "Aries": {
        "theme": "The Pioneer Year — Bold Action & Fresh Starts",
        "what_it_means": "Aries rises with Mars energy — this is a year of movement, initiative, and personal courage. The solar return activates your drive to start things. If you have been waiting, this is the year to stop waiting.",
        "opportunity": "Launch new ventures, take on visible leadership roles, and make bold physical changes — relocating, restructuring, reinventing.",
        "risk": "Impatience and aggression. Moving so fast that you miss important details or damage relationships. Slow down at least 20% before deciding.",
        "focus_areas": ["Career visibility", "Physical health and energy", "Starting the project you've been postponing"],
        "remedies": ["Offer water to the Sun every morning", "Wear red or coral on Tuesdays", "Avoid confrontations on Tuesdays — the energy amplifies them"]
    },
    "Taurus": {
        "theme": "The Consolidation Year — Wealth & Roots",
        "what_it_means": "Venus rules this solar return. The year's energy flows toward building, accumulating, and stabilising. What you plant this year takes root for years to come — make sure it's worth tending.",
        "opportunity": "Long-term financial decisions, property, family investments, creative projects that compound over time.",
        "risk": "Stubbornness and comfort-seeking. Avoiding necessary change because the status quo feels safe. Watch for stagnation.",
        "focus_areas": ["Savings and investments", "Home environment", "Creative work with commercial value"],
        "remedies": ["Keep fresh flowers at home — white or pink", "Chant 'Om Shukraya Namah' on Fridays", "Donate sweets or food on Fridays"]
    },
    "Gemini": {
        "theme": "The Communicator Year — Ideas & Networks",
        "what_it_means": "Mercury rules this return. Your mind is sharper than usual and your network is the engine. Information, communication, and short-distance movement define the year's rhythm.",
        "opportunity": "Writing, speaking, launching content, making deals, building connections across industries.",
        "risk": "Scattered focus. Gemini energy can spread thin — trying to do too many things and finishing none of them.",
        "focus_areas": ["Communication and writing", "Short-term projects and deals", "Building knowledge deliberately"],
        "remedies": ["Carry a green aventurine stone", "Read something challenging every day", "Donate green items on Wednesdays"]
    },
    "Cancer": {
        "theme": "The Roots Year — Home, Family & Inner Nourishment",
        "what_it_means": "The Moon governs this return. The year turns inward — to home, family, and emotional foundations. External achievements feel hollow unless the inner world is stable. Build the home base first.",
        "opportunity": "Strengthening family bonds, resolving old emotional patterns, real estate decisions, and inner healing work.",
        "risk": "Over-sensitivity and retreat. Withdrawing too far from the world can leave opportunities untouched.",
        "focus_areas": ["Home and family", "Emotional health", "Property or living situation"],
        "remedies": ["Place a pot of water in the northeast corner of your home", "Respect your mother — call her more often", "Eat lighter foods, especially in the evening"]
    },
    "Leo": {
        "theme": "The Spotlight Year — Visibility & Authority",
        "what_it_means": "The Sun in its own sign at the solar return is a powerful signal — this year, you are meant to be seen. The world is paying attention. Use it.",
        "opportunity": "Public launches, leadership roles, brand-building, stepping into any role where you represent something bigger than yourself.",
        "risk": "Ego. Leo energy can tip into arrogance or a need for recognition that alienates the very people whose support you need.",
        "focus_areas": ["Career and public reputation", "Creative expression", "Any project requiring confidence and presence"],
        "remedies": ["Wear gold on Sundays", "Donate wheat or jaggery on Sundays", "Spend time daily on something purely creative"]
    },
    "Virgo": {
        "theme": "The Precision Year — Health, Craft & Systems",
        "what_it_means": "Mercury governs this return with Virgo's analytical lens. The year rewards mastery, attention to detail, and systematic improvement. This is the year to fix what is broken in your daily routine.",
        "opportunity": "Health improvements, skill upgrades, process optimisation, and any work requiring sustained precision.",
        "risk": "Perfectionism and worry. Virgo energy can become paralysis — analysing until the window closes.",
        "focus_areas": ["Physical health and daily habits", "Work systems and efficiency", "Learning a specific skill deeply"],
        "remedies": ["Maintain a clean and organised workspace", "Donate green vegetables on Wednesdays", "Practice a brief daily meditation before starting work"]
    },
    "Libra": {
        "theme": "The Partnership Year — Relationships & Balance",
        "what_it_means": "Venus rules this return through Libra. The year's biggest gains come through other people — business partners, life partners, collaborators. Do not try to do this year alone.",
        "opportunity": "New partnerships, contracts, negotiations, and any situation that requires diplomacy and win-win thinking.",
        "risk": "Indecision and people-pleasing. The drive for harmony can prevent you from making necessary hard choices.",
        "focus_areas": ["Business and personal partnerships", "Legal agreements", "Social and professional reputation"],
        "remedies": ["Wear white or pastel on Fridays", "Keep your relationships balanced — address small grievances before they compound", "Donate white items or sugar on Fridays"]
    },
    "Scorpio": {
        "theme": "The Transformation Year — Depth & Rebirth",
        "what_it_means": "Mars and Ketu govern this intense return. What no longer serves you will be stripped away — often suddenly. This is not a punishment; it is a clearing. What remains after this year is what is actually real.",
        "opportunity": "Deep research, financial restructuring, clearing old patterns, inheritance matters, and any work involving investigation or hidden systems.",
        "risk": "Obsession and power struggles. Scorpio energy can become controlling or paranoid — trust needs to be extended consciously.",
        "focus_areas": ["Financial restructuring (debts, investments, joint assets)", "Letting go of what has expired", "Research and depth work"],
        "remedies": ["Chant 'Om Namah Shivaya' — especially on Mondays", "Donate oil on Saturdays", "Avoid revenge-driven decisions — they cost more than they recover"]
    },
    "Sagittarius": {
        "theme": "The Expansion Year — Vision & Higher Learning",
        "what_it_means": "Jupiter rules this return. The year wants to stretch you — geographically, intellectually, and philosophically. The opportunities this year will come from directions you haven't looked before.",
        "opportunity": "Travel, education, publishing, international connections, and any work that requires a long-range view.",
        "risk": "Over-commitment and overconfidence. Jupiter expands everything — including mistakes. Do not over-promise.",
        "focus_areas": ["Education and learning", "Long-distance travel or connections", "Philosophical and spiritual work"],
        "remedies": ["Visit a place of worship or nature regularly", "Respect your teachers and mentors actively", "Donate yellow items or turmeric on Thursdays"]
    },
    "Capricorn": {
        "theme": "The Achievement Year — Career & Long-term Structure",
        "what_it_means": "Saturn governs this return. The year rewards those who show up, do the work, and do not cut corners. The gains are real, lasting, and proportional to the effort put in — nothing more, nothing less.",
        "opportunity": "Career advancement, building lasting systems and institutions, and taking on responsibilities that others avoid.",
        "risk": "Rigidity and isolation. The Capricorn drive for achievement can crowd out relationships and joy. Schedule rest deliberately.",
        "focus_areas": ["Career and professional standing", "Long-term structural goals", "Financial discipline"],
        "remedies": ["Work on Saturday mornings — Saturn rewards consistent early effort", "Donate black sesame seeds (til) on Saturdays", "Avoid shortcuts — this year, they backfire more than usual"]
    },
    "Aquarius": {
        "theme": "The Innovation Year — Original Thinking & Community",
        "what_it_means": "Saturn and Rahu govern this return. The year rewards unconventional thinking and collective action. Your most powerful moves this year will be the ones that break with tradition.",
        "opportunity": "Technology, social causes, innovation, and working with communities or networks toward a shared goal.",
        "risk": "Detachment and rebellion for its own sake. Aquarius energy can push away support structures that are still needed.",
        "focus_areas": ["Community and group work", "Technology and innovation", "Social impact"],
        "remedies": ["Engage with a community cause — volunteer or contribute", "Wear blue on Saturdays", "Stay grounded — schedule regular in-person connection"]
    },
    "Pisces": {
        "theme": "The Surrender Year — Intuition, Spirituality & Inner Depth",
        "what_it_means": "Jupiter and Ketu govern this gentle but powerful return. The year calls you inward. The insights you gather in solitude and reflection will fuel the next major cycle of your outer life.",
        "opportunity": "Creative work, spiritual practice, healing, and any field that benefits from deep intuitive access.",
        "risk": "Escapism and lack of boundaries. Pisces energy can dissolve necessary structure — watch for excessive withdrawal or avoidance.",
        "focus_areas": ["Spiritual and inner work", "Creative and artistic projects", "Healing and releasing old patterns"],
        "remedies": ["Spend time near water regularly", "Practice gratitude journaling each evening", "Donate at a place of worship on Thursdays"]
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
    "Aries":       "You are a warrior at the soul level. Your inner fire keeps you moving toward your purpose, no matter the obstacles. Relationships need a partner who matches your independence.",
    "Taurus":      "Your soul craves security, beauty, and permanence. You give deeply in relationships — and need the same in return. Your spiritual progress accelerates through stillness.",
    "Gemini":      "Your soul is curious, adaptable, and never fully settled. Your dharma involves communication and intellectual exchange. Relationships thrive when there is constant mental stimulation.",
    "Cancer":      "Your soul thrives on emotional connection and safety. Your relationships will feel like a sanctuary after your 30s. Intuition is your greatest spiritual instrument.",
    "Leo":         "Your soul is built for creative expression and leadership. At the core, you need to be seen and to inspire. Relationships flourish when your partner recognises your light.",
    "Virgo":       "Your soul seeks precision, service, and meaning in the details. You find spiritual fulfillment through solving real problems for real people. Partnerships need reliability above romance.",
    "Libra":       "Your soul longs for harmony, fairness, and beauty in all forms. You are drawn to partnerships as a mirror for self-growth. Balance in relationships is your deepest spiritual lesson.",
    "Scorpio":     "Your soul is built for transformation and depth. You will go through intense reinventions — each one making you stronger. Relationships must have complete honesty or they won't survive.",
    "Sagittarius": "Your soul is oriented toward wisdom, travel, and expansion of beliefs. You need a partner who supports your freedom. Your dharma involves teaching or guiding others.",
    "Capricorn":   "Your soul values structure, discipline, and legacy. Your spiritual growth comes through sustained effort over time. You build relationships slowly but they last a lifetime.",
    "Aquarius":    "Your soul is wired for collective progress and unconventional thinking. You are here to contribute to something larger than yourself. Relationships work best with intellectual equals.",
    "Pisces":      "Your soul is deeply empathic, intuitive, and spiritually porous. Your inner world is rich and complex. Relationships require clear boundaries or your energy will be absorbed by others.",
}

_D10_MEANINGS = {
    "Aries":       "In your public life, you are a pioneer. You'll be known for starting new things and leading from the front — often in roles that demand courage and speed.",
    "Taurus":      "Your career legacy is built on reliability and value creation. You are seen as someone who delivers, accumulates, and builds things that last. Finance and resource management suit you.",
    "Gemini":      "You will make your mark through communication, ideas, and connection. Writing, media, sales, or education — any field where words and networks are the product.",
    "Cancer":      "In your career, you are seen as a protector or a nurturer. You'll leave your mark through roles that involve care, management, or public service.",
    "Leo":         "Your professional identity is tied to visibility and authority. You are remembered for presence, creative leadership, and the ability to command a room. Brand and performance roles suit you.",
    "Virgo":       "You build professional reputation through precision, analysis, and flawless execution. Roles in operations, healthcare, research, or quality management are where you leave a lasting mark.",
    "Libra":       "You are known as someone who brings fairness, diplomacy, and aesthetic judgment to everything you touch. Law, design, HR, or client-facing roles will define your legacy.",
    "Scorpio":     "Your career involves deep investigation and transformation — research, finance, psychology, or crisis management. People trust you with what others can't handle.",
    "Sagittarius": "Your professional identity is built around knowledge, expansion, and inspiring others. Teaching, consulting, publishing, or entrepreneurship in global markets will define your public legacy.",
    "Capricorn":   "Your public life is set for sustained rise to authority. You are a builder of institutions and systems. The older you get, the more respected and senior your position becomes.",
    "Aquarius":    "You are known for bringing innovation and social impact to your field. Your professional legacy involves disrupting the status quo or building something that benefits a community.",
    "Pisces":      "Your career legacy is built on creativity, empathy, and vision. You are drawn to work that has a spiritual or humanitarian dimension — arts, healing, or social work.",
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
            return f"You have {pl_str} all in {sign}. This means a huge part of your life energy is focused on {sign}'s themes: it's like a 'power-spot' in your chart that gives you a massive edge."
    return ""


def get_retrograde_note(transit_planets: Dict[str, Any]) -> str:
    retro = [n for n in ["Mercury", "Mars", "Jupiter", "Venus", "Saturn"]
             if transit_planets.get(n, {}).get("is_retrograde")]
    if not retro:
        return "Everything is moving forward today! No cosmic blocks — it's a great time to start something new."
    if "Mercury" in retro:
        return "Mercury is retrograde, which means communication might get a bit messy. Take a breath, double-check your texts, and avoid signing big deals today."
    names = " and ".join(retro)
    verb = "is" if len(retro) == 1 else "are"
    return f"{names} {verb} retrograde. This is a time to look inward and fix things, rather than starting huge new projects. The ground is being prepared."


def generate_directive(md_lord: str, ad_lord: str, transit_planets: Dict[str, Any]) -> str:
    ad_strategy = AD_STRATEGIES.get(ad_lord, "")
    retro_note  = get_retrograde_note(transit_planets)
    all_direct  = "forward momentum" in retro_note.lower()

    parts = []
    if md_lord and ad_lord and ad_strategy:
        parts.append(f"In your current {md_lord}-{ad_lord} chapter, focus on this: {ad_strategy[0].lower() + ad_strategy[1:]}")
    
    if not all_direct:
        parts.append(retro_note)
    elif parts:
        parts.append("The cosmic energy is moving forward today, so go for it.")

    return " ".join(parts) if parts else retro_note


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

    superpowers = [
        {"title": f"The Real You (Sun in {sun_sign})", "description": SIGN_NATAL[sun_sign]},
        {"title": f"How You Appear ({lagna_sign} Rising)", "description": SIGN_NATAL[lagna_sign]}
    ]

    if stellium_note:
        superpowers.append({"title": "Your Power-Spot", "description": stellium_note})

    directive = generate_directive(md_lord, ad_lord, transit_planets)

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

    strategy = f"{md_theme['life']} Focus on this: {ad_strategy}"

    return {
        "active_dasha": f"{md_lord}-{ad_lord}",
        "display_dasha": f"{md_lord} Maha-Dasha · {ad_lord} Bhukti",
        "focus": md_theme["focus"],
        "target_kpi": f"{md_lord} · {ad_lord} sub-cycle",
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
                "reason": "Mercury is retrograde, making agreements a bit tricky.",
                "action": "Double-check every single detail. If you can wait a few days to sign, do it."
            })
            continue

        relevant_keywords = dasha_risk_map.get(active_dasha_lord, [])
        synergy_found = any(kw in summary_lower for kw in relevant_keywords)

        if synergy_found:
            advice_list.append({
                "event": summary,
                "risk": "Low",
                "reason": f"Your current {active_dasha_lord} chapter is great for this kind of work.",
                "action": "Go for it. You have the cosmic wind at your back."
            })
            continue

        if is_high_stakes:
            advice_list.append({
                "event": summary,
                "risk": "Moderate",
                "reason": "This is a big moment for you.",
                "action": "Take a breath, stay calm, and be yourself. You've got this."
            })

    return advice_list
