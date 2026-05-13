# Cosmic OS — Living Audit Specification
## Version: 3 | Last run: 2026-05-14 | Next review: after next feature ship

> **Self-update rule for any AI reading this:**
> After every run of `demos/master_audit.py`:
> 1. Read `docs/AUDIT_REPORT.md` — every ❌ or ⚠️ needs a tighter check added below
> 2. Every feature shipped (see PROJECT_PLAN.md ✅ list) must have ≥1 check per dimension
> 3. Increment the version number above
> 4. Add the date to "Last run"
> 5. Never remove old checks — mark them `[DEPRECATED]` if superseded

---

## DIMENSION 1 — User Journey
_Can a real user complete the full flow without confusion?_

| ID | Check | How | Pass Criterion |
|----|-------|-----|----------------|
| UJ-01 | Landing headline present and compelling | Playwright | `.landing-h1` text > 30 chars |
| UJ-02 | Sub-headline reinforces value | Playwright | `.landing-sub` text > 20 chars |
| UJ-03 | Feature pills visible | Playwright | ≥4 `.pill` elements |
| UJ-04 | Consent modal dismissible | Playwright | `.consent-agree` click → modal hidden |
| UJ-05 | Chart generates after form fill | Playwright | `#resultsScreen` visible within 20s |
| UJ-06 | TL;DR card populated (not "—") | Playwright | `#tldrLine` text ≠ "—" |
| UJ-07 | All 3 tabs navigate correctly | Playwright | Today / Full Chart / Numbers all switch |
| UJ-08 | Edit Details pre-fills saved data | Playwright | Name + DOB restored correctly |
| UJ-09 | Morning Brief visible above fold | Playwright | `#morningBriefSection` in viewport |
| UJ-10 | Share button copies meaningful text | Playwright | Clipboard text > 50 chars |
| UJ-11 | Hindi toggle visible in header | Playwright | `#langToggleBtn` present |

---

## DIMENSION 2 — Content Quality
_Is every section populated with personalized, actionable, on-tone content?_

| ID | Check | How | Pass Criterion |
|----|-------|-----|----------------|
| CQ-01 | Daily theme references actual planet/sign | Playwright | `#dailyTheme` contains sign name (Aries/Leo etc.) or planet |
| CQ-02 | Directive references actual Dasha lord | Playwright | `#operationalPointer` contains planet name |
| CQ-03 | Morning Brief has today's date | Playwright | `#morningBriefCard` contains current YYYY-MM-DD |
| CQ-04 | No "—" placeholders in visible sections | Playwright | Zero visible `—` text in TL;DR chips |
| CQ-05 | Section titles non-empty | Playwright | All `.section-title` elements have text > 3 chars |
| CQ-06 | ? tooltips have meaningful text | Playwright | All `[data-tooltip]` attrs length > 20 chars |
| CQ-07 | Hindi toggle translates ≥5 elements | API + Playwright | `/api/translate` returns non-Latin characters |
| CQ-08 | Sanskrit terms preserved in Hindi | API | Response to translate retains "Dasha", "Bhukti", "Nakshatra" |
| CQ-09 | Numerology name matches input | Playwright | `#jyName` contains entered name |
| CQ-10 | DC Profile compatibility % is a number | Playwright | `.jy-compat-badge` matches `\d+%` pattern |

---

## DIMENSION 3 — API Correctness
_Do all endpoints return valid, complete, personalized data?_

| ID | Endpoint | Required Fields | Pass Criterion |
|----|----------|-----------------|----------------|
| API-01 | `GET /health` | `status` | `{"status":"ok"}` |
| API-02 | `POST /api/chart` | `planets`, `lagna`, `dashas`, `coach_insights` | All keys present, planets has ≥9 entries |
| API-03 | `GET /api/brief/morning` | `date`, `overall_window`, `top_action`, `personal_day` | All keys present, date = today |
| API-04 | `GET /api/timing/advisor` | `actions` | 6 action objects, each with `label`, `score`, `verdict` |
| API-05 | `POST /api/translate` | `translations` | Length matches input, contains Devanagari chars |
| API-06 | `POST /api/numerology/jyotish` | `mulank`, `bhagyank`, `kua`, `namank` | All numbers 1–9 (or master 11/22/33) |
| API-07 | `GET /api/numerology/cycles` | `personal_year`, `personal_month`, `personal_day` | All present |
| API-08 | `GET /api/chart/muhurta` | `windows` | ≥1 window object |
| API-09 | `POST /api/translate` with missing key | `detail` | Returns 503, not 500 crash |
| API-10 | `POST /api/chart` with invalid date | HTTP status | Returns 422 or 400, not 500 |

---

## DIMENSION 4 — Design Token Compliance
_Does every pixel follow DECISIONS.md and PSBC Premium rules?_

| ID | Check | How | Pass Criterion |
|----|-------|-----|----------------|
| DT-01 | Results screen background is `#0C0A1E` | Playwright JS eval | `getComputedStyle(resultsScreen).backgroundColor` matches |
| DT-02 | Purple `#635bff` only on CTA buttons | Playwright JS eval | No `.section-title`, `.card-label` has purple color |
| DT-03 | Gold `#C8A86A` on section-title in dark mode | Playwright JS eval | `.section-title` color = gold in results screen |
| DT-04 | Font is Inter everywhere | Playwright JS eval | `getComputedStyle(body).fontFamily` contains "Inter" |
| DT-05 | Section-title has gold border-left | Playwright JS eval | `.results-screen .section-title` has border-left |
| DT-06 | TL;DR card background is purple `#635bff` | Playwright JS eval | `.tldr-card` background-color = purple |
| DT-07 | Mobile layout not broken at 390px | Playwright viewport | No horizontal overflow at width=390 |
| DT-08 | Cards have ≥24px padding | Playwright JS eval | `.card` padding ≥ 24px |

---

## DIMENSION 5 — Security
_Are user data, API keys, and sessions protected?_

| ID | Check | How | Pass Criterion |
|----|-------|-----|----------------|
| SEC-01 | `.env` is in `.gitignore` | Shell | `grep -q "\.env" .gitignore` exits 0 |
| SEC-02 | `.env` not exposed via any API route | requests | `GET /api/.env` returns 404 |
| SEC-03 | GEMINI_API_KEY not in git history | Shell | `git log -p | grep AIza` returns empty |
| SEC-04 | XSS in name field handled | Playwright | Name `<script>alert(1)</script>` → no alert fires |
| SEC-05 | Invalid birth date returns 4xx | requests | `POST /api/chart` with date `1800-01-01` → 400/422 |
| SEC-06 | Lat/lon out of range returns 4xx | requests | `lat=999` → 400/422 |
| SEC-07 | `/api/translate` with 0 texts returns empty | requests | `texts: []` → `translations: []`, not crash |
| SEC-08 | Cookie is set on session start | requests | Response headers include `Set-Cookie` |

---

## DIMENSION 6 — Feature Completeness
_Does every ✅ feature in PROJECT_PLAN.md actually work end-to-end?_

| ID | Feature | Check | Pass Criterion |
|----|---------|-------|----------------|
| FC-01 | P1: Section headers — Today tab | Playwright | ≥5 `.section-title` in `#strategicView` |
| FC-02 | P1: Section headers — Full Chart | Playwright | ≥3 `.section-title` or `.adv-block-label` in `#technicalView` |
| FC-03 | P1: Section headers — Numbers tab | Playwright | ≥5 `.num-group .section-title` in `#numerologyView` |
| FC-04 | P1: 16 tooltip badges | Playwright | Total `.qmark[data-tooltip]` count ≥ 14 |
| FC-05 | P1: Numerology 5-group structure | Playwright | `#jyProfilePanel .num-group` count = 5 |
| FC-06 | P1: U-001 — interpretation before grid | Playwright JS | `.interp-card` precedes `#planetGrid` in DOM |
| FC-07 | P2: Hindi toggle button | Playwright | `#langToggleBtn` visible and clickable |
| FC-08 | P2: Hindi translation API live | API | `/api/translate` returns 200 with Devanagari |
| FC-09 | Core: Vimshottari Dasha present | API | `/api/chart` response has `dashas` array |
| FC-10 | Core: Morning Brief date is today | API | `date` field = today's date |
| FC-11 | Core: 6 Business Timing actions | API | `/api/timing/advisor` has 6 actions |
| FC-12 | Advanced: Yogas detected | API | `/api/chart` has `yogas` array (may be empty) |
| FC-13 | Advanced: Ashtakavarga present | API | `/api/chart` has `ashtakavarga` object |
| FC-14 | P2: People Compat discoverability | Playwright | `.compat-discover-btn` visible in DC card + `#compatSection .section-title` present |
| FC-15 | P2: Yearly Forecast renders | Playwright | `#forecastSection` visible + `#forecastGrid` has 12 child cards |

---

## DIMENSION 7 — Resilience & Edge Cases
_Does the app handle failure gracefully — no blank screens, no silent crashes?_

| ID | Check | How | Pass Criterion |
|----|-------|-----|----------------|
| RES-01 | No name entered → numerology shows prompt | Playwright | `#jyNameRequired` visible, not blank screen |
| RES-02 | Translate fails → button resets, no crash | Playwright | Remove key, click toggle → button text restored |
| RES-03 | Unknown city typed → friendly error | Playwright | Typing "xyzxyz123" → no JS error, graceful UX |
| RES-04 | Chart API slow → loading state visible | Playwright | Spinner or loading indicator appears within 500ms of submit |
| RES-05 | Invalid date → form validation fires | Playwright | DOB "99/99/9999" → button stays disabled or error shown |
| RES-06 | `/api/translate` empty body → 422 | requests | Returns 422, not 500 |
| RES-07 | Numerology with 1-char name | API | `POST /api/numerology/jyotish` with `name="A"` → valid response |

---

## GAPS TO FILL NEXT RUN
_(AI: move items here from the report's ⚠️ list, then add checks above)_

- [ ] **API-02d**: `coach_insights` missing from `/api/chart` response — check if field was removed or renamed
- [ ] **API-06**: `kua` number not returned by `/api/numerology/jyotish` — endpoint may need gender-based KUA calculation fix
- [ ] **API-10**: Invalid date `1800-01-01` returns 200 — add date range validation (1900–2100) to `/api/chart`
- [ ] **SEC-06**: `lat=999` returns 200 — add coordinate boundary check (-90≤lat≤90, -180≤lon≤180)
- [ ] **CQ-01**: Daily theme check looks for planet/sign name but Nakshatra-based themes ("Dreaming & Sensing") are valid — expand check to include Nakshatra names
- [ ] **RES-01**: No-name resilience test — confirm whether name is required for chart generate; if optional, fix test to check numerology tab prompt only
- [ ] **RES-04**: Loading state during chart generation not yet confirmed
- [ ] **SEC-08**: Cookie security attributes not yet validated

---

## LAST REPORT SUMMARY
_Paste the summary block from `docs/AUDIT_REPORT.md` here after each run_

```
Run: 2026-05-14 | master_audit.py — all 7 dimensions
✅ 42 / ⚠️ 3 / ❌ 0  (total 45 checks)
Dimensions covered: ALL 7 (API, Security, Journey, Content, Design Tokens, Features, Resilience)
Executor: demos/master_audit.py (headless Playwright + requests)
Warnings: API-10 (date range), SEC-06 (lat/lon bounds), RES-01 (test logic) — all low priority
```
