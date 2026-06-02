# DECISIONS.md — Cosmic OS / Jyotish Engine Core
## Authoritative Decision Log · All AI Agents Must Read This

> **Rule:** Every decision with a non-obvious reason lives here. When a new decision is made, append it. Never overwrite existing entries without noting the reversal and the new reasoning. This file is the single source of truth for *why* things are the way they are.

---

## How to Read This File

Each entry follows this structure:
- **Decision:** What was chosen.
- **Why:** The reasoning behind it — constraints, prior failure, strong preference.
- **Date:** When it was confirmed.
- **Status:** Active / Reversed (if reversed, links to the reversal entry).

---

## Design & Visual Identity

### D-001 · Dual Color System (Gold + Purple)
- **Decision:** Two accent colors are used intentionally. `--accent: #C8A86A` (gold) is used for content — section labels, numbers, active data states. `--cta: #635bff` (PSBC purple) is used for actions only — buttons, CTAs, interactive controls. Never swap them.
- **Why:** `#635bff` on Vedic astrology content reads as a fintech dashboard. Gold communicates cosmic, precious, and ancient — the correct register for life-chart readings. Purple on CTAs maintains PSBC brand. The distinction was tested and confirmed satisfying in Session 3 (2026-05-10).
- **Date:** 2026-05-10
- **Status:** Active

### D-002 · Background Color
- **Decision:** `--bg: #DCE6F2` (PSBC brand blue-grey). Not white. Not `#fbfbfd`.
- **Why:** `#DCE6F2` is the confirmed PSBC brand background across all projects. Apple-style white backgrounds (`#fbfbfd`) make the app feel generic and lose the brand distinctiveness.
- **Date:** 2026-05-10
- **Status:** Active

### D-003 · Hero / Dark Section Background
- **Decision:** `--hero-bg: #1E1A38` (deep indigo-purple). Not Apple-grey `#1d1d1f`.
- **Why:** The dark hero card communicates cosmic depth and urgency. Apple-grey reads as a generic tech product — wrong register for a Vedic intelligence app.
- **Date:** 2026-05-10
- **Status:** Active

### D-004 · Surface and Text Colors
- **Decision:** `--surface: #fffdf9` (warm cream), `--text: #1a1208` (warm near-black), `--muted: #8a7e68` (warm grey). All warm-toned, not cold.
- **Why:** Cold whites and greys (`#ffffff`, `#86868b`) strip the warmth from Vedic content. The warm palette supports the "cosmic sanctuary" feeling. Confirmed as intentional dual system alongside D-001.
- **Date:** 2026-05-10
- **Status:** Active

### D-005 · Typography
- **Decision:** Inter font, `-0.022em` letter-spacing on headers, `-webkit-font-smoothing: antialiased`.
- **Why:** PSBC Premium Minimalism standard across all projects. Tight tracking reads as institutional and precise — matches Strategy Consultant tone.
- **Date:** 2026-05-09
- **Status:** Active

### D-006 · Brand Name
- **Decision:** The app is called **Cosmic OS**. Not "Astro". Not "Jyotish Engine".
- **Why:** "Cosmic OS" is the confirmed product name. "Astro" was briefly added to GEMINI.md in an unauthorized session (2026-05-12) without a product decision — it is not confirmed. Do not rename without explicit user approval.
- **Date:** 2026-05-12
- **Status:** Active · ⚠️ Note: GEMINI.md currently says "Astro" — this is a stale/unauthorized change, not a confirmed decision.

---

## Architecture & Engineering

### A-001 · FastAPI Route Order (Critical)
- **Decision:** `app.mount("/", StaticFiles(...))` must always be the LAST line in `main.py`.
- **Why:** This mount is a catch-all. Any route defined after it is silently swallowed and never reached. Caused real production bugs before this rule was codified.
- **Date:** 2026-05-09
- **Status:** Active

### A-002 · Server Port
- **Decision:** Server runs on port **5004**, not 8000.
- **Why:** Port 8000 is what the README says (outdated). The actual configured port is 5004. The README has not been updated — trust the code (`src/main.py`) over the README.
- **Date:** 2026-05-09
- **Status:** Active

### A-003 · No Frontend Frameworks
- **Decision:** Pure HTML/CSS/JS — no React, Vue, or any framework.
- **Why:** PSBC standard. Keeps the app fast, dependency-free, and portable. The app already has sufficient JS complexity — a framework would add overhead without benefit at this scale.
- **Date:** 2026-05-09
- **Status:** Active

### A-004 · Ayanamsa: Lahiri (Sidereal)
- **Decision:** All planetary calculations use **Lahiri Ayanamsa** (sidereal), not Tropical.
- **Why:** Lahiri is the standard for Jyotish (Vedic astrology). Tropical is the Western system. This app is a Jyotish engine — using Tropical would produce incorrect Vedic readings.
- **Date:** 2026-05-09
- **Status:** Active

### A-005 · Database: SQLite
- **Decision:** SQLite (`cosmic_os.db`) is the database. Not PostgreSQL.
- **Why:** Single-user personal tool. SQLite has zero infrastructure overhead, runs in-process, and is sufficient for the current scale (142 profiles, one real user). Migrate if multi-tenant production scale is ever needed.
- **Date:** 2026-05-09
- **Status:** Active

### A-006 · Numerology System: Jyotish Only
- **Decision:** The Chaldean numerology engine was removed. Only the Jyotish numerology system (Mulank, Bhagyank, KUA, DC Profiles) is supported.
- **Why:** The Chaldean engine in `numerology-feedback.js` was dead/incorrect code (647 lines → removed, file trimmed to 385). Keeping two systems would cause inconsistency and user confusion. The Jyotish system is the authoritative one for this app.
- **Date:** 2026-05-10
- **Status:** Active

---

## Auth & Security

### S-001 · Session Auth: Cookie-Based
- **Decision:** User sessions use cookie-based auth (not JWT in headers).
- **Why:** Multi-user support requires server-side session scoping. Cookies are simpler and sufficient for this use case.
- **Date:** 2026-05-09
- **Status:** Active

### S-002 · Apple Login: Commented Out, Not Deleted
- **Decision:** The "Connect Apple" button is HTML-commented out (`<!-- ... -->`), not removed from the codebase.
- **Why:** Apple Login integration is planned but not complete. The HTML stub is preserved for when it's implemented. `verify_signature: True` is already set in `apple_auth.py`.
- **Date:** 2026-05-10
- **Status:** Active

### S-003 · Secrets in .env, Never Hardcoded
- **Decision:** All API keys, secrets, and OAuth credentials are in `.env` (gitignored). `env.template` is committed with placeholder values.
- **Why:** Previous sessions had secrets hardcoded in source. Moved to `.env` to prevent accidental exposure via git. `env.template` documents what's needed without leaking values.
- **Date:** 2026-05-10
- **Status:** Active

---

## UX & Content

### U-001 · Clarity Hierarchy: Theme First, Data Last
- **Decision:** Every insight section must follow: Theme (1 line) → What it means for you (2 lines) → What to do (3 bullets) → Supporting data (expandable). Data must never appear before context.
- **Why:** The app was originally built for someone who already knows astrology. First-time users got raw data (Kundali, 9 planets, Dasha) with no orientation — they had no idea what to look at. The Strategic tab already does this correctly; the Technical tab still needs it.
- **Date:** 2026-05-10
- **Status:** Active · ⚠️ Technical tab is not yet fully compliant.

### U-002 · Numerology Atlas: Internal Knowledge Base Only
- **Decision:** The 142-person Numerology Profile DB is an internal knowledge base. It is used for compatibility comparisons and backend intelligence. It is NOT presented as a user-facing "directory" or "explore" feature.
- **Why:** The 142 profiles are pre-seeded reference data (public figures, archetypes). Exposing them as a directory raises privacy perception issues and dilutes the personal-chart focus. Endpoints exist for backend use only.
- **Date:** 2026-05-09
- **Status:** Active

### U-003 · User Count Copy: Real Numbers Only
- **Decision:** The landing page shows real data: "142 profiles in the atlas." Not vanity metrics like "12,847 charts read."
- **Why:** The vanity metric was fabricated. Pranav's explicit preference is for honesty — fake social proof is worse than real (smaller) numbers.
- **Date:** 2026-05-10
- **Status:** Active

### U-004 · Share Flow: Clipboard First, WhatsApp Fallback
- **Decision:** The share button copies to clipboard first. WhatsApp share is the fallback.
- **Why:** Clipboard is universal and doesn't assume the recipient uses WhatsApp. WhatsApp fallback covers mobile users who may not have native clipboard access.
- **Date:** 2026-05-10
- **Status:** Active

### U-005 · Ashtakavarga Baseline Label
- **Decision:** Ashtakavarga grid includes the label: "6+ = Strong · 4–5 = Moderate · 0–3 = Weak"
- **Why:** Without a baseline, users have no reference for whether a score of 5 is good or bad. This was a confirmed clarity gap — non-astrologers were confused by raw numbers.
- **Date:** 2026-05-10
- **Status:** Active

### U-006 · DC Compatibility Badge: Color-Coded with Range
- **Decision:** DC compatibility shows a color-coded badge (green ≥75%, yellow 50–74%, red <50%) with an inline range legend: "Below 50 = tension · 50–75 = workable · 75+ = harmonious."
- **Why:** "67% compatible" with no reference frame is meaningless to most users. Color + label gives instant orientation without requiring astrological knowledge.
- **Date:** 2026-05-10
- **Status:** Active

---

## Validation Protocol

### V-001 · Visual Satisfaction Loop Required
- **Decision:** Every UI change or logic update affecting the user journey must be verified via `python3 visual_demo.py` before marking as done.
- **Why:** Silent UI failures (blank tabs, missing data, broken selectors) have repeatedly slipped through without visual verification. The demo script is the acceptance test for all frontend work.
- **Settings:** `headless=False`, `slow_mo=1500ms`
- **Date:** 2026-05-09
- **Status:** Active

---

## Reversals & Overrides

*None yet. Append here when a prior decision is reversed, with the new reasoning and date.*

---

## How to Append a New Decision

Copy this template and add it to the relevant section:

```
### X-NNN · Short Title
- **Decision:** What was chosen.
- **Why:** The reasoning.
- **Date:** YYYY-MM-DD
- **Status:** Active
```
