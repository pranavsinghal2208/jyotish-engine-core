# Astro: Project Instructions (GEMINI.md)

## Core Mandates
- **Brand Identity:** Astro (formerly Cosmic OS). 
- **Design Standard:** PSBC Premium Minimalism. Inter font, -0.022em tracking, massive whitespace, monochromatic base (#ffffff/#fbfbfd), PSBC accent (#635bff).
- **Tone:** "Operational Sanctuary" for the Overwhelmed Achiever. Use "Strategy Consultant" terminology (e.g., Information Arbitrage, System Precision).
- **Logic:** Swiss Ephemeris (Lahiri Ayanamsa) calculating Dasha-Bhukti and real-time transits.

## Validation Protocol: Visual Satisfaction Loop
- **Requirement:** Every UI change or logic update that affects the user journey MUST be verified using the "Visual Satisfaction Loop."
- **Command:** `python3 visual_demo.py` (or the current session's audit script).
- **Settings:** Headless: FALSE, Slow_mo: 1500ms.
- **Criteria:** The agent must act as Coder, Critic, and Auditor. The walkthrough must be "calm" and "institutionally satisfying."

## Engineering Patterns
- **Database:** Persistent SQLite (`cosmic_os.db`) stores natal data and OAuth tokens.
- **Translator:** `src/translator.py` is the single source of truth for "Coach" and "Business" insights.
- **Frontend:** Pure Canvas (Zero-UI) landing. Transitions must feel like "Morphs," not page loads.

## Reference Documents
- **Decision Log:** `DECISIONS.md` — confirmed design, architecture, and UX decisions with rationale. **Read before touching UI, color, auth, or product copy.** If something seems wrong, check here before overriding it.
- **Global Skills:** `~/Dev/GLOBAL_SKILLS.md` — cross-project learnings, proven practices, context-sensitive rules (read this too!)
- **Unified Project Plan:** `PROJECT_PLAN.md` — feature status, wishlist, file map (read this first!)
- **Customer Profile:** `.gemini/tmp/pranavsinghal/memory/customer_profile.md`
- **Feature Matrix:** `.gemini/tmp/pranavsinghal/f3aef365-f8da-453d-9814-b0412e25245f/plans/tabular-feature-matrix.md`
