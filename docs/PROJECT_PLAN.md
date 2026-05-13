# Cosmic OS — Project Plan
## Single Source of Truth for All AI Agents (Claude, Gemini, Kilo, etc.)

> **Rule:** Every AI working on this project MUST read this file first. When new features ship or goals change, update this file.
> **Also read:** `DECISIONS.md` — confirmed decisions with rationale. Check it before changing anything in UI, color, auth, or product copy.

---

## Vision
A personal "Cosmic Operating System" for Pranav Singhal — combining Vedic Astrology (Jyotish), Numerology, and Google Calendar into an executive intelligence dashboard. PSBC brand. Apple-grade UI.

---

## Tech Stack
- **Backend:** FastAPI + PySwissEph + SQLAlchemy + SQLite (`cosmic_os.db`)
- **Frontend:** Pure HTML/CSS/JS (no frameworks) at `src/static/`
- **Server:** `source venv/bin/activate && python3 -m src.main` → port 5004
- **Dashboard:** `http://127.0.0.1:5004`
- **Visual validation:** `python3 demos/visual_demo.py` (headless=False, slow_mo=1500ms)

---

## Feature Status — What Is Done

### ✅ Core Astrology Engine
- Sidereal planetary positions (Lahiri Ayanamsa, PySwissEph), Lagna, Vimshottari Dasha-Bhukti
- Daily transit overlay, Nakshatra, AI "Coach" insights (`src/translator.py`)
- Business ROI Pulse (Dasha + transit correlation)

### ✅ Advanced Astrology Layer (May 9)
- Yoga detection, Sade Sati, Mangal Dosha, Sarvashtakavarga, D-9/D-10, Varshaphal — `src/astro_tools.py`
- Muhurta scanner: `GET /api/chart/muhurta?days=N`
- All rendered in Full Chart tab (Advanced Analysis section)

### ✅ Google Calendar Integration
- OAuth 2.0 flow, credentials persisted in SQLite, Cosmic Schedule advice in `/api/chart`

### ✅ Numerology (Jyotish System, May 9)
- Engine: Mulank, Bhagyank, Gift#, KUA, Namank, Lo Shu Grid — `src/numerology.py`
- 81 DC profiles, missing number remedies — `src/numerology_data.py`
- 142-person internal knowledge base (not user-facing directory)
- Personal Year/Month/Day cycles, Two-Person Compatibility with score + pros/cons
- API: `/api/numerology/profiles`, `/api/numerology/profile/{label}`, `/api/numerology/cycles`, `/api/numerology/compatibility`

### ✅ Business Timing Advisor (May 9)
- `GET /api/timing/advisor` → 6-action grid: Launch / Sign / Hire / Invest / Negotiate / Travel

### ✅ Morning Brief (May 9)
- `GET /api/brief/morning` → date, overall window, personal day, lucky color, top action, transit highlights

### ✅ Multi-User Auth Decoupling (May 10)
- Cookie-based session scoping, real email from Google OAuth token
- Apple Login stub preserved (`src/auth/apple_auth.py`, `verify_signature: True`)

### ✅ Feedback + Analytics Systems
- `src/feedback.py` — auto-categorized feedback, `src/analytics.py` — page views, feature usage

### ✅ UI Overhaul — Dark Cosmic Theme + Polish (May 12)
- Dark cosmic landing (deep indigo hero, gold accents, zodiac ring)
- Dark theme extended to all result pages and numerology tab
- Numerology content bugs fixed, backend interpretation wired to frontend
- Calendar Alert banner (dark theme + connect nudge for unlinked users)
- Google OAuth PKCE bug fixed (code_verifier now persisted in cookie)
- DC Compatibility: directional scores + pros/cons breakdown
- Sarvashtakavarga legend (score out of 56, 28+ = Strong)
- Maha Dasha: discovery hint to tap periods for narrative + practices
- Mobile layout: technical view + city search fixed
- Consent gate + style polish

### ✅ UX Pass — Hook + Orientation (May 13 — this session)
- Landing H1 → "Walk away knowing three things: what today feels like, what to do, and where you are in your life right now."
- Sub → "Takes 30 seconds. Built on 5000 years of Vedic timing science."
- Feature pills → plain English (no astrology symbols)
- Tab labels → Today / Full Chart / Numbers
- Morning Brief moved to top of results (most actionable content first)
- Section labels time-scoped: "Today ·" / "This Week ·"
- TL;DR card — purple banner, first element of results: focus line + lucky number + best move + window

---

## PENDING TASKS — Consolidated & Prioritized
*Sources: DECISIONS.md flags (⚠️), user feedback May 2026, git log scan, this session review.*

---

### 🔴 P0 — Hygiene (Non-negotiable, do first)

**1. Commit staged repo reorganization**
- Large staged commit sitting uncommitted: demos/, docs/, scripts/ dirs + pyproject.toml + CI workflow
- Today's UX changes (index.html, app.js, style.css) need a separate commit on top

**2. Fix stale GEMINI.md**
- File says "Astro" as product name — unauthorized change (DECISIONS.md D-006)
- Correct name: Cosmic OS. Update GEMINI.md

**3. Fix pytest in venv**
- `python3 -m pytest` fails — pytest not installed in venv
- Fix: `source venv/bin/activate && pip install pytest httpx`

---

### 🔴 P1 — UX: Human Depth (In-flight, this week)
*Core principle: every screen must answer "What does this mean for me, right now, and what should I do?"*

**4. Section headers — all 3 tabs**
- Every section needs a visible title (not just a small chip label) + time window
- Today tab: 8 sections to header
- Full Chart tab: 10 sections to header
- Numbers tab: all numerology groups

**5. Tooltip glossary — `?` hover descriptions**
- Add `?` icon next to every jargon term; on hover: what it is + what this user's value means + action
- Priority order: Mulank · Bhagyank · KUA Number · Lo Shu Grid · Dasha · Bhukti · Nakshatra · Tithi · Yoga · Lagna · Sade Sati · Mangal Dosha · Ashtakavarga · Navamsa · Dasamsa · Varshaphal
- Implementation: CSS `::after` tooltip on `?` span (no JS for basic); popover for mobile

**6. Numerology tab — section categorization**
- Group into named sections with 1-line descriptions:
  - **Core Identity** — Mulank (Driver) + Bhagyank (Conductor): who you are and what drives you
  - **Personality & Compatibility** — KUA Number + DC Profile: how you relate and pair with others
  - **Life Grid** — Lo Shu: the 9-cell map of your strengths and gaps
  - **Name Influence** — Namank: what your name adds or subtracts
  - **Right Now** — Personal Year / Month / Day cycles: where you are in your current rhythm
- Each individual number card gets a `?` tooltip with calculation logic

**7. Full Chart tab — U-001 compliance** *(flagged in DECISIONS.md U-001 as ⚠️ pending)*
- Hierarchy on every section: Theme (1 line) → What it means for you (2 lines) → What to do (3 bullets) → Data
- Current gap: raw planetary grid shown before interpretation card — swap the order

---

### 🟡 P2 — Product Depth (Next sessions)

**8. Apple Login — complete**
- Stub HTML commented in `index.html` (DECISIONS.md S-002)
- `src/auth/apple_auth.py` exists, `verify_signature: True` already set
- Un-comment button + end-to-end test

**9. Calendar Alerts — live verification**
- Banner UI shipped (May 12). Needs:
  - OAuth token auto-refresh test with a real Google account
  - Live calendar event → high-stakes detection → banner trigger

**10. Hindi language toggle**
- Language selector on landing + results pages
- All text, labels, and coach insights translated via Gemini 1.5 Flash (POWER zone — never Groq)
- Numerology Sanskrit terms retain names, explained in Hindi
- Future: Gemini 2.5 Flash Live API for real-time voice Q&A in local language (log only, not P1)

**11. AI People Compatibility — discoverability**
- Backend + score UI shipped (May 12)
- Needs: clearer entry point in the Numbers tab (currently buried)

**12. Yearly Forecast**
- Personal Year Number breakdown, month-by-month Lo Shu cycle, PDF export

---

### 🟢 P3 — Ship Readiness

**13. Production deployment**
- `render.yaml` configured and ready
- Blocker: no GitHub remote yet — add `git remote add origin <repo>` first, then push + connect Render

**14. Chatbot / RAG**
- Natural language Q&A about your chart
- Context: natal chart + transits + numerology profile
- Model: Ollama local (private zone — chart data is personal)

---

### 🗂 Workspace Infra (Separate from Cosmic OS — pending since May 2 session)
- Firecrawl API key → firecrawl.dev (placeholder in Claude settings)
- Greptile API key → GREPTILE_API_KEY env var never set
- Postgres connection string → placeholder in both configs
- n8n → `npm install -g n8n` not done yet
- Docker Desktop → open once to complete initial setup

---

## Design Standards (PSBC Premium)
- Background: `#DCE6F2` outer, `#fffdf9` warm cream cards
- Accent gold: `#C8A86A` (content, section labels, numbers)
- Accent purple: `#635bff` (actions, CTAs only — never on content)
- Hero/dark: `#1E1A38` (deep indigo — not Apple grey)
- Font: Inter, -0.022em tracking, antialiased
- Style: Cosmic sanctuary — warm, ancient, precise. Not fintech.
- Tone: Strategy consultant + Vedic depth. Executive-focused.

---

## File Map
```
src/
  main.py              — All FastAPI routes (StaticFiles mount MUST be last line)
  engine.py            — Jyotish (PySwissEph) calculations
  translator.py        — AI coach + business insights
  numerology.py        — Jyotish numerology engine
  numerology_data.py   — 81 DC profiles, remedies, number meanings
  feedback.py          — Feedback management
  analytics.py         — Analytics tracker + dashboard
  auth/
    google_auth.py     — Google OAuth manager
    apple_auth.py      — Apple Login (stub, not yet wired)
  integrations/
    gcal.py            — Google Calendar manager
  database/
    models.py          — SQLAlchemy models
    session.py         — DB session + init_db()
  static/
    index.html         — Main dashboard UI
    app.js             — Core dashboard JS
    style.css          — Main styles
    numerology-feedback.js  — Numerology + feedback JS
    numerology-feedback.css — Numerology + feedback styles
demos/                 — Visual + feature demo scripts
docs/                  — PROJECT_PLAN, DECISIONS, README, etc.
scripts/               — Audit + seed scripts
tests/unit/            — Unit tests (pytest — currently not runnable, fix venv)
```

---

## AI Agent Instructions
- **Never hardcode** user data — always read from DB or user input
- **Never send** client names, PII, or financials to cloud AIs — private zone only
- **Always verify** UI changes via `python3 demos/visual_demo.py` before marking done
- **Route order:** `app.mount("/", StaticFiles(...))` must be the LAST line in `main.py`
- **Port:** Server runs on 5004 (README says 8000 — outdated, ignore it)
- **Product name:** Cosmic OS. Not "Astro". Not "Jyotish Engine". See DECISIONS.md D-006.
