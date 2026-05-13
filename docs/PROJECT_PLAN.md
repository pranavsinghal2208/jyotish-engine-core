# Cosmic OS — Project Plan
## Single Source of Truth for All AI Agents (Claude, Gemini, Kilo, etc.)

> **Rule:** Every AI working on this project MUST read this file first. When new features ship or goals change, update this file.
> **Also read:** `DECISIONS.md` — confirmed decisions with rationale. Check it before changing anything in UI, color, auth, or product copy.
> **Audit rule:** Every feature marked ✅ must have ≥1 passing check in `demos/master_audit.py`. Run `venv/bin/python3 demos/master_audit.py` at session start and after every feature ship. Last score: ✅ 44 / ⚠️ 3 / ❌ 0 (2026-05-14).

---

## Vision
A personal "Cosmic Operating System" for Pranav Singhal — combining Vedic Astrology (Jyotish), Numerology, and Google Calendar into an executive intelligence dashboard. PSBC brand. Apple-grade UI.

---

## Tech Stack
- **Backend:** FastAPI + PySwissEph + SQLAlchemy + SQLite (`cosmic_os.db`)
- **Frontend:** Pure HTML/CSS/JS (no frameworks) at `src/static/`
- **Server:** `source venv/bin/activate && python3 -m src.main` → port 5004
- **Dashboard:** `http://127.0.0.1:5004`
- **Audit:** `venv/bin/python3 demos/master_audit.py` — 7-dimension, 47 checks, headless (fast, ~2 min)
- **Visual walkthrough:** `venv/bin/python3 demos/master_audit.py --visual` (headless=False, slow_mo=1200ms)

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

## PENDING TASKS
*Last cleaned: 2026-05-14. Done items removed. Conflicts resolved.*

---

### 🔴 P0 — Fix Now

**1. ⚠️ Hindi toggle broken**
- Root cause: `_collectTranslatables()` was sending full `el.textContent` (child links/buttons included) → Gemini returned multi-line output → parser misaligned all translations
- Fix deployed (commit 70c761a): direct text nodes only, skips `—`, added `⚠ Retry` error state; `?v=3` cache bust on scripts
- **Next step:** Hard-refresh (Cmd+Shift+R) → click "EN | हिं" → if still broken, open DevTools Console and paste the error

**2. ⚠️ House system — Whole Sign vs Placidus**
- PySwissEph defaults to Placidus; Jyotish requires Whole Sign
- Every house-based interpretation (yoga detection, Sarvashtakavarga, house lords) is potentially wrong until this is fixed
- Must be resolved **before** any KB rules are written — rules depend on correct house assignment
- Fix: set `hsys=b'W'` explicitly in `engine.py` house calculation call

**3. Fix pytest in venv**
- `python3 -m pytest` fails — pytest not installed in venv
- Fix: `source venv/bin/activate && pip install pytest httpx`

---

### 🟡 P1 — Product Depth

**4. Apple Login — complete**
- Stub HTML commented in `index.html` (DECISIONS.md S-002)
- `src/auth/apple_auth.py` exists, `verify_signature: True` already set
- Un-comment button + end-to-end OAuth test

**5. Calendar Alerts — live verification**
- Banner UI shipped. Needs:
  - OAuth token auto-refresh test with a real Google account
  - Live calendar event → high-stakes detection → banner trigger

---

### 🟢 P2 — Ship Readiness

**6. Production deployment on Render**
- `render.yaml` ready, GitHub remote live (`pranavsinghal2208/jyotish-engine-core`)
- Steps: render.com → New → Blueprint → connect repo → set env vars:
  - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
  - `REDIRECT_URI` → `https://cosmic-os.onrender.com/auth/callback`
  - `GEMINI_API_KEY` (required for Hindi toggle on live site)

**7. Conversational Chatbot (private)**
- Natural language Q&A about your chart — "What does my Venus Dasha mean for business?"
- Model: Ollama local (private zone — chart data stays on device)
- Context: natal chart + transits + numerology profile passed as system prompt

---

### 🔵 P3 — Strategic Scale
*Full analysis + moat defense in `docs/STRATEGIC_BLUEPRINT.md`*

**8. Fix transit scoring — house-aware**
- Current bug: `if p in current_planets` ignores house position → Venus 8H (bad for finance) scores same as Venus 2H (good for finance)
- Fix: pass `planet_house` dict from `engine.py` into `timing_advisor._score_action()`, check `planet_house[p] in favorable_houses`
- Blocks: all KB rules that depend on house-specific timing

**9. Outcome feedback loop (the moat)**
- Add "Did this timing work? ✓ / ✗" on each Business Timing card
- Store: `user_id · action_type · score · outcome · date`
- 500 data points = proprietary correlation set no competitor can replicate

**10. Knowledge Base — ingestion form**
- Google Sheets with Section A–D columns (see `STRATEGIC_BLUEPRINT.md` Part 2)
- Target: 500 rules Phase 1 → `scripts/import_kb.py` → SQLite → pgvector Phase 2
- Must come after P0 item 2 (house system fix)

**11. Premium report pipeline**
- Ingestion: yt-dlp + Whisper + Firecrawl + PyMuPDF → raw text
- Parse: Gemini 1.5 Flash (1M ctx) → structured KB entries → human review gate
- Retrieve: pgvector semantic search on natal chart → top-K matching rules
- Synthesize: LLM formats KB text only, never originates claims + mandatory disclaimer
- Output: full Kundli-style report (SVG chart + 9 sections + 90-day action plan)
- Merges with item 7 (chatbot) at the retrieval layer

**12. B2B API**
- Expose `/api/timing/advisor` as webhook-callable with API key auth
- Target: CRM tools, sales teams, project management apps

---

### 🗂 Workspace Infra (pending since May 2)
- Firecrawl API key → firecrawl.dev
- Greptile API key → `GREPTILE_API_KEY` env var
- Postgres connection string
- n8n → `npm install -g n8n`
- Docker Desktop → open once for initial setup

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
- **Always verify** UI changes via `venv/bin/python3 demos/master_audit.py` (headless) or `--visual` flag before marking done
- **Route order:** `app.mount("/", StaticFiles(...))` must be the LAST line in `main.py`
- **Port:** Server runs on 5004 (README says 8000 — outdated, ignore it)
- **Product name:** Cosmic OS. Not "Astro". Not "Jyotish Engine". See DECISIONS.md D-006.
