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
- **Visual validation:** `python3 visual_demo.py` (headless=False, slow_mo=1500ms)

---

## Feature Status

### ✅ DONE — Core Astrology
- Sidereal planetary positions (Lahiri Ayanamsa, PySwissEph)
- Lagna (Ascendant) calculation
- Vimshottari Dasha-Bhukti mapping
- Daily transit overlay on natal chart
- AI "Coach" insights via `src/translator.py`
- Business ROI Pulse (Dasha + transit correlation)
- Nakshatra calculation

### ✅ DONE — Google Calendar Integration
- OAuth 2.0 flow (`/auth/google/login`, `/auth/google/callback`)
- Credentials persisted in SQLite
- Upcoming events fetched, analyzed for "cosmic priority"
- Cosmic Schedule advice returned in `/api/chart`

### ✅ DONE — Numerology (Jyotish System)
- **Engine:** `src/numerology.py` — Mulank, Bhagyank, Gift#, KUA, Namank, Birth Year#, Lo Shu Grid
- **Data:** `src/numerology_data.py` — 81 Driver~Conductor profiles, missing number remedies, number meanings
- **Database:** `NumerologyProfile` table in `src/database/models.py` — 142 people seeded
- **Seed script:** `seed_numerology_profiles.py`
- **API endpoints:**
  - `GET /api/numerology/profiles` — list all 142 people
  - `GET /api/numerology/profile/{label}` — full Jyotish reading by label
  - `POST /api/numerology` — legacy Western numerology (Life Path, Expression, Soul Urge)
- **Frontend status:** ✅ CONNECTED — auto-loads user's own Jyotish profile on tab click. 142-person DB is internal knowledge base only (backend endpoints kept, not user-facing)

### ✅ DONE — Feedback System
- `src/feedback.py` — auto-categorization (sentiment, priority, topics)
- DB model: `Feedback` table
- Endpoints: `POST /api/feedback`, `GET /api/feedback/stats`, `GET /api/feedback/recent`

### ✅ DONE — Analytics
- `src/analytics.py` — page views, feature usage, conversions
- Endpoints: `POST /api/analytics/track`, `GET /api/analytics/summary`

---

## PENDING / WISHLIST (priority order)

### ✅ DONE — Numerology UI
Fully wired. Auto-loads user's own Jyotish profile from birth details. Lo Shu Grid, DC Profile card, Missing Number Remedies — verified via visual demo 2026-05-09.

### ✅ DONE — Numerology Extensions + Timing + Morning Brief (2026-05-09)
- **#8 Personal Year/Month/Day** — `GET /api/numerology/cycles` → Current Cycles widget in Numerology tab
- **#10 Two-Person Compatibility** — `GET /api/numerology/compatibility?label_a=X&label_b=Y` → 142-person DB comparison panel with score, dynamics, pros/cons
- **#13 Business Timing Advisor** — `GET /api/timing/advisor` → 6-action grid (Launch/Sign/Hire/Invest/Negotiate/Travel) scored by Dasha + transits
- **#15 Morning Brief** — `GET /api/brief/morning` → auto-shown card in Strategic tab after chart generation

### ✅ DONE — Astrology Calculation Layer
All 7 tools implemented, wired to `/api/chart`, rendered in Technical tab Advanced Analysis section. Verified via visual demo 2026-05-09.
- `src/astro_tools.py` — Yoga detection, Sade Sati, Mangal Dosha, Sarvashtakavarga, D-9/D-10 divisional charts, Varshaphal (Solar Return)
- `GET /api/chart/muhurta?days=N` — Auspicious window scanner
- Technical tab: Active Yogas grid, Sade Sati + Mangal Dosha cards, House Strength grid, Navamsa/Dasamsa tables, Varshaphal panel

### ✅ DONE — Multi-User Auth Decoupling 
Transitioned to cookie-based session scoping (decoupled default@psbc.com).
- Extract real user email from Google OAuth token (already in callback, just parse it)
- All DB queries scoped to real user
- Apple Login SSO

### 🟡 P2 — Real-Time Calendar Alerts
- Verify OAuth token auto-refresh works without manual re-auth
- Test with live calendar events
- Show "upcoming high-stakes event" banner on dashboard

### 🟡 P2 — AI People Compatibility
- Given two labels from the NumerologyProfile directory
- Calculate DC compatibility between two people
- Show relationship dynamics (pro/con overlap, number resonance)

### 🟡 P2 — Yearly Forecast
- Personal Year Number (Bhagyank + current year)
- Month-by-month breakdown in Lo Shu cycle
- Export as PDF report

### 🟢 P3 — Production Deployment
- HTTPS hosting (Railway / Render)
- Domain setup
- `git init` + GitHub repo (currently no version control)

### 🟢 P3 — Chatbot / RAG
- Ask natural language questions about your chart
- Answer based on natal chart + current transits + numerology profile

---

## Design Standards (PSBC Premium)
- Background: `#DCE6F2` outer, `#ffffff` cards
- Accent: `#635bff`
- Font: Inter, -0.022em tracking
- Style: Minimalist, Apple-inspired, clean white cards, massive whitespace
- Tone: "Operational Sanctuary" — Strategy Consultant vocabulary

---

## File Map
```
src/
  main.py              — All FastAPI routes
  engine.py            — Jyotish (PySwissEph) calculations
  translator.py        — AI coach + business insights (single source of truth)
  numerology.py        — Jyotish numerology engine
  numerology_data.py   — 81 DC profiles, remedies, number meanings
  feedback.py          — Feedback management
  analytics.py         — Analytics tracker + dashboard
  auth/
    google_auth.py     — Google OAuth manager
  integrations/
    gcal.py            — Google Calendar manager
  database/
    models.py          — SQLAlchemy models (User, OAuthCredential, Feedback, NumerologyProfile)
    session.py         — DB session + init_db()
  static/
    index.html         — Main dashboard UI
    app.js             — Core dashboard JS
    style.css          — Main styles
    numerology-feedback.js  — Numerology + feedback JS
    numerology-feedback.css — Numerology + feedback styles
    analytics.js       — Analytics tracker JS
    analytics-dashboard.js  — Analytics dashboard JS
```

---

## AI Agent Instructions
- **Never hardcode** user data — always read from DB or user input
- **Never send** client names, PII, or financials to cloud AIs — private zone only
- **Always verify** UI changes with `python3 visual_demo.py` before marking done
- **Routing rule:** In FastAPI, `app.mount("/", StaticFiles(...))` must be the LAST line — it is a catch-all that swallows all routes defined after it
- **Port:** Server runs on 5004 (not 8000 as README says — README is outdated)
