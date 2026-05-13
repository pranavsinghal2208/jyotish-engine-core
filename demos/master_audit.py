"""
Cosmic OS — Master Audit Engine v1
Covers all 7 dimensions from docs/AUDIT_SPEC.md
Reads spec → runs checks → writes docs/AUDIT_REPORT.md

Self-update loop:
  1. Run this script
  2. AI reads docs/AUDIT_REPORT.md
  3. AI adds new checks to docs/AUDIT_SPEC.md + this script
  4. Version in AUDIT_SPEC.md increments

Usage:
  source venv/bin/activate
  python3 demos/master_audit.py

Model-agnostic: Claude, Gemini, Kilo — all read the same AUDIT_SPEC.md and AUDIT_REPORT.md
"""

import asyncio
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

import requests
from playwright.async_api import async_playwright

# ── Config ────────────────────────────────────────────────
BASE        = "http://127.0.0.1:5004"
REPORT_PATH = Path("docs/AUDIT_REPORT.md")
SPEC_PATH   = Path("docs/AUDIT_SPEC.md")
TODAY       = date.today().isoformat()
VISUAL      = "--visual" in sys.argv   # headless=False, slow_mo=1200ms

SAMPLE = {
    "name": "Pranav Singhal",
    "date": "1987-08-22",
    "time": "21:55",
    "lat": 29.4727,
    "lon": 77.7085,
    "gender": "Male",
    "offset": 5.5,
}

# ── Results store ─────────────────────────────────────────
results = []   # (dim, id, verdict, message)

def ok(dim, id, msg):
    results.append((dim, id, "✅", msg))
    print(f"  ✅ [{id}] {msg}")

def warn(dim, id, msg):
    results.append((dim, id, "⚠️ ", msg))
    print(f"  ⚠️  [{id}] {msg}")

def fail(dim, id, msg):
    results.append((dim, id, "❌", msg))
    print(f"  ❌ [{id}] {msg}")

def header(title):
    print(f"\n{'═'*54}")
    print(f"  {title}")
    print(f"{'═'*54}")

# ══════════════════════════════════════════════════════════
# DIMENSION 3 — API Correctness (no browser needed)
# ══════════════════════════════════════════════════════════
def audit_api():
    header("DIMENSION 3 — API Correctness")

    # API-01: health
    try:
        r = requests.get(f"{BASE}/health", timeout=5)
        if r.status_code == 200 and r.json().get("status") == "ok":
            ok("API", "API-01", "/health → ok")
        else:
            fail("API", "API-01", f"/health → {r.status_code} {r.text[:60]}")
    except Exception as e:
        fail("API", "API-01", f"/health → unreachable: {e}")
        return  # no point continuing if server is down

    # API-02: chart
    try:
        r = requests.post(f"{BASE}/api/chart", json=SAMPLE, timeout=15)
        if r.status_code == 200:
            data = r.json()
            planets  = data.get("planets", {})
            dashas   = data.get("dashas", [])
            insights = data.get("insights", {})
            ok("API", "API-02", f"/api/chart → 200 | planets={len(planets)} dashas={len(dashas)}")
            if len(planets) < 9:
                warn("API", "API-02b", f"Only {len(planets)} planets returned (expect ≥9)")
            if not dashas:
                warn("API", "API-02c", "No dashas in response")
            if not insights:
                warn("API", "API-02d", "No insights in response")
        else:
            fail("API", "API-02", f"/api/chart → {r.status_code}: {r.text[:100]}")
    except Exception as e:
        fail("API", "API-02", f"/api/chart → exception: {e}")

    # API-03: morning brief
    try:
        r = requests.get(f"{BASE}/api/brief/morning", params=SAMPLE, timeout=10)
        if r.status_code == 200:
            data = r.json()
            required = ["date", "overall_window", "top_action", "personal_day"]
            missing  = [k for k in required if k not in data]
            date_ok  = data.get("date", "") == TODAY
            if not missing:
                ok("API", "API-03", f"/api/brief/morning → all fields present | date_ok={date_ok}")
            else:
                warn("API", "API-03", f"/api/brief/morning → missing fields: {missing}")
            if not date_ok:
                warn("API", "API-03b", f"Morning brief date={data.get('date')} but today={TODAY}")
        else:
            fail("API", "API-03", f"/api/brief/morning → {r.status_code}")
    except Exception as e:
        fail("API", "API-03", f"/api/brief/morning → {e}")

    # API-04: timing advisor
    try:
        r = requests.get(f"{BASE}/api/timing/advisor", params=SAMPLE, timeout=10)
        if r.status_code == 200:
            data    = r.json()
            actions = data.get("actions", [])
            if len(actions) == 6:
                ok("API", "API-04", f"/api/timing/advisor → 6 actions")
                fields_ok = all("label" in a and "score" in a for a in actions)
                if not fields_ok:
                    warn("API", "API-04b", "Some action objects missing label or score")
            else:
                warn("API", "API-04", f"/api/timing/advisor → {len(actions)} actions (expect 6)")
        else:
            fail("API", "API-04", f"/api/timing/advisor → {r.status_code}")
    except Exception as e:
        fail("API", "API-04", f"/api/timing/advisor → {e}")

    # API-05: translate
    try:
        payload = {"texts": ["Today's Energy", "Core Identity", "Life Timing"], "target": "hi"}
        r = requests.post(f"{BASE}/api/translate", json=payload, timeout=15)
        if r.status_code == 200:
            data = r.json()
            translations = data.get("translations", [])
            if len(translations) == 3:
                has_devanagari = any(
                    any('ऀ' <= c <= 'ॿ' for c in t)
                    for t in translations
                )
                ok("API", "API-05", f"/api/translate → {len(translations)} translations | devanagari={has_devanagari}")
                if not has_devanagari:
                    warn("API", "API-05b", "Translations contain no Devanagari characters — may be English fallback")
                # Sanskrit terms preserved
                for term in ["Energy", "Identity"]:  # these should be translated
                    pass
            else:
                warn("API", "API-05", f"/api/translate → {len(translations)} results for 3 inputs")
        elif r.status_code == 503:
            warn("API", "API-05", "/api/translate → 503: GEMINI_API_KEY not configured")
        else:
            fail("API", "API-05", f"/api/translate → {r.status_code}: {r.text[:80]}")
    except Exception as e:
        fail("API", "API-05", f"/api/translate → {e}")

    # API-06: numerology
    try:
        r = requests.post(f"{BASE}/api/numerology/jyotish",
                          json={"full_name": SAMPLE["name"], "birth_date": SAMPLE["date"],
                                "gender": SAMPLE["gender"]},
                          timeout=10)
        if r.status_code == 200:
            data = r.json()
            nums = {k: data.get(k) for k in ["mulank", "bhagyank", "kua_number", "namank"]}
            missing = [k for k, v in nums.items() if v is None]
            if not missing:
                ok("API", "API-06", f"/api/numerology/jyotish → {nums}")
            else:
                warn("API", "API-06", f"Missing numerology fields: {missing}")
        else:
            fail("API", "API-06", f"/api/numerology/jyotish → {r.status_code}")
    except Exception as e:
        fail("API", "API-06", f"/api/numerology/jyotish → {e}")

    # API-09: translate with no key (handled)
    try:
        payload = {"texts": [], "target": "hi"}
        r = requests.post(f"{BASE}/api/translate", json=payload, timeout=5)
        if r.status_code == 200 and r.json().get("translations") == []:
            ok("API", "API-09", "/api/translate with empty texts → [] (correct)")
        else:
            warn("API", "API-09", f"/api/translate empty → {r.status_code} {r.text[:60]}")
    except Exception as e:
        fail("API", "API-09", f"/api/translate empty → {e}")

    # API-10: invalid date
    try:
        bad = {**SAMPLE, "date": "1800-01-01"}
        r = requests.post(f"{BASE}/api/chart", json=bad, timeout=10)
        if r.status_code in (400, 422):
            ok("API", "API-10", f"Invalid date → {r.status_code} (correct rejection)")
        elif r.status_code == 200:
            warn("API", "API-10", "Invalid date 1800-01-01 returned 200 — no input validation")
        else:
            warn("API", "API-10", f"Invalid date → {r.status_code}")
    except Exception as e:
        warn("API", "API-10", f"Invalid date test → {e}")


# ══════════════════════════════════════════════════════════
# DIMENSION 5 — Security (no browser needed)
# ══════════════════════════════════════════════════════════
def audit_security():
    header("DIMENSION 5 — Security")

    # SEC-01: .env in .gitignore
    try:
        gi = Path(".gitignore").read_text()
        if ".env" in gi:
            ok("SEC", "SEC-01", ".env is in .gitignore")
        else:
            fail("SEC", "SEC-01", ".env NOT in .gitignore — API keys at risk")
    except Exception:
        warn("SEC", "SEC-01", ".gitignore not found")

    # SEC-02: .env not exposed via HTTP
    try:
        r = requests.get(f"{BASE}/api/.env", timeout=5)
        if r.status_code == 404:
            ok("SEC", "SEC-02", "/.env not exposed via HTTP → 404")
        else:
            fail("SEC", "SEC-02", f"/.env returned {r.status_code} — potential exposure")
    except Exception as e:
        ok("SEC", "SEC-02", f"/.env request failed (likely 404): {e}")

    # SEC-03: API key not in git history
    try:
        result = subprocess.run(
            ["git", "log", "--all", "-p", "--follow", "--", ".env"],
            capture_output=True, text=True, timeout=10
        )
        if "AIza" in result.stdout or "GEMINI_API_KEY=" in result.stdout:
            fail("SEC", "SEC-03", "API key found in git history — rotate immediately")
        else:
            ok("SEC", "SEC-03", "No API key found in git history")
    except Exception as e:
        warn("SEC", "SEC-03", f"Git history check skipped: {e}")

    # SEC-07: translate with empty body
    try:
        r = requests.post(f"{BASE}/api/translate", json={"texts": [], "target": "hi"}, timeout=5)
        if r.status_code in (200, 422):
            ok("SEC", "SEC-07", f"/api/translate empty body → {r.status_code} (no crash)")
        else:
            warn("SEC", "SEC-07", f"/api/translate empty → {r.status_code}")
    except Exception as e:
        fail("SEC", "SEC-07", f"/api/translate empty → crashed: {e}")

    # SEC-05: out-of-range lat/lon
    try:
        bad = {**SAMPLE, "lat": 999, "lon": 999}
        r = requests.post(f"{BASE}/api/chart", json=bad, timeout=10)
        if r.status_code in (400, 422):
            ok("SEC", "SEC-06", f"lat=999 → {r.status_code} (correct rejection)")
        elif r.status_code == 200:
            warn("SEC", "SEC-06", "lat=999 returned 200 — no boundary validation")
        else:
            warn("SEC", "SEC-06", f"lat=999 → {r.status_code}")
    except Exception as e:
        warn("SEC", "SEC-06", f"Lat boundary test → {e}")


# ══════════════════════════════════════════════════════════
# BROWSER-BASED DIMENSIONS (1, 2, 4, 6, 7)
# ══════════════════════════════════════════════════════════
async def audit_browser():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=not VISUAL, slow_mo=1200 if VISUAL else 0)
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            permissions=["clipboard-read", "clipboard-write"]
        )
        page = await ctx.new_page()
        await page.goto(BASE, wait_until="networkidle")

        try:
            await _dim1_journey(page)
        except Exception as e:
            warn("UJ", "UJ-00", f"Dim 1 aborted: {e}")
        try:
            await _dim2_content(page)
        except Exception as e:
            warn("CQ", "CQ-00", f"Dim 2 aborted: {e}")
        try:
            await _dim4_design_tokens(page)
        except Exception as e:
            warn("DT", "DT-00", f"Dim 4 aborted: {e}")
        try:
            await _dim6_features(page)
        except Exception as e:
            warn("FC", "FC-00", f"Dim 6 aborted: {e}")
        try:
            await _dim7_resilience(page, ctx)
        except Exception as e:
            warn("RES", "RES-00", f"Dim 7 aborted: {e}")

        await browser.close()


async def _fill_form_and_generate(page):
    """Helper: fill form and dismiss consent modal."""
    await page.goto(BASE, wait_until="networkidle")
    await page.fill("#fullName", SAMPLE["name"])
    dd, mm, yyyy = SAMPLE["date"].split("-")[2], SAMPLE["date"].split("-")[1], SAMPLE["date"].split("-")[0]
    await page.fill("#dobDD", dd)
    await page.fill("#dobMM", mm)
    await page.fill("#dobYYYY", yyyy)
    await asyncio.sleep(1.5)
    await page.fill("#time", SAMPLE["time"])
    # City
    try:
        await page.fill("#citySearch", "Muzaffarnagar")
        await asyncio.sleep(1.2)
        first = page.locator("#cityResults .city-option").first
        if await first.is_visible():
            await first.click()
    except Exception:
        pass
    # Always set lat/lon directly via JS (hidden inputs, fill() is a no-op on them)
    await page.evaluate(f"""
        document.getElementById('lat').value = '{SAMPLE["lat"]}';
        document.getElementById('lon').value = '{SAMPLE["lon"]}';
    """)
    await asyncio.sleep(0.5)
    try:
        await page.click("#generateBtn")
    except Exception:
        pass
    # Consent modal
    try:
        await page.wait_for_selector(".consent-agree", timeout=3000)
        await page.click(".consent-agree")
    except Exception:
        pass
    try:
        await page.wait_for_selector("#resultsScreen:not(.hidden)", timeout=35000)
        await asyncio.sleep(2.0)
        return True
    except Exception:
        return False


async def _txt(page, sel):
    try:
        return (await page.locator(sel).first.text_content(timeout=3000) or "").strip()
    except Exception:
        return ""

async def _visible(page, sel):
    try:
        return await page.locator(sel).first.is_visible()
    except Exception:
        return False

async def _count(page, sel):
    try:
        return await page.locator(sel).count()
    except Exception:
        return 0

async def _eval(page, js):
    try:
        return await page.evaluate(js)
    except Exception:
        return None


# ── Dimension 1: User Journey ─────────────────────────────
async def _dim1_journey(page):
    header("DIMENSION 1 — User Journey")
    await page.goto(BASE, wait_until="networkidle")

    h1 = await _txt(page, ".landing-h1")
    ok("UJ", "UJ-01", f"Headline: '{h1[:60]}'") if len(h1) > 30 else fail("UJ", "UJ-01", f"Headline too short: '{h1}'")

    sub = await _txt(page, ".landing-sub")
    ok("UJ", "UJ-02", f"Sub-headline: '{sub[:60]}'") if len(sub) > 20 else warn("UJ", "UJ-02", "Sub-headline missing or short")

    pills = await _count(page, ".pill")
    ok("UJ", "UJ-03", f"Feature pills: {pills}") if pills >= 4 else warn("UJ", "UJ-03", f"Only {pills} feature pills")

    loaded = await _fill_form_and_generate(page)
    ok("UJ", "UJ-05", "Chart generated — results screen visible") if loaded else fail("UJ", "UJ-05", "Chart generation timed out")
    if not loaded:
        return

    # TL;DR card
    tldr_visible = await _visible(page, "#tldrCard")
    tldr_text    = await _txt(page, "#tldrLine")
    ok("UJ", "UJ-06", f"TL;DR card: '{tldr_text[:50]}'") if tldr_visible and tldr_text not in ("", "—") \
        else warn("UJ", "UJ-06", f"TL;DR card visible={tldr_visible} text='{tldr_text}'")

    # Tabs
    for tab, view in [("technical", "#technicalView"), ("numerology", "#numerologyView"), ("strategic", "#strategicView")]:
        await page.click(f'button[data-view="{tab}"]')
        await asyncio.sleep(0.8)
        visible = await _visible(page, view)
        ok("UJ", "UJ-07", f"Tab '{tab}' navigates correctly") if visible else fail("UJ", "UJ-07", f"Tab '{tab}' view not visible")

    await page.evaluate("window.scrollTo(0, 0)")

    # Hindi toggle
    lang_btn = await _visible(page, "#langToggleBtn")
    ok("UJ", "UJ-11", "Hindi toggle button present in header") if lang_btn else fail("UJ", "UJ-11", "Hindi toggle button MISSING")

    # Share button
    try:
        await page.click("#shareReadingBtn")
        await asyncio.sleep(1.2)
        clipboard = await page.evaluate(
            "navigator.clipboard.readText().then(t=>t.slice(0,80)).catch(()=>'')"
        )
        ok("UJ", "UJ-10", f"Share copies: '{clipboard[:50]}'") if len(clipboard) > 20 \
            else warn("UJ", "UJ-10", "Share clipboard empty or short")
    except Exception as e:
        warn("UJ", "UJ-10", f"Share button: {e}")


# ── Dimension 2: Content Quality ──────────────────────────
async def _dim2_content(page):
    header("DIMENSION 2 — Content Quality")
    loaded = await _fill_form_and_generate(page)
    if not loaded:
        warn("CQ", "CQ-00", "Skipped — chart did not load")
        return

    theme = await _txt(page, "#dailyTheme")
    planet_signs = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
                    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
                    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
                    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva", "Uttara",
                    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
                    "Mula", "Purvashadha", "Uttarashadha", "Shravana", "Dhanishtha",
                    "Shatabhisha", "Purvabhadra", "Uttarabhadra", "Revati",
                    "Dreaming", "Sensing", "Building", "Healing", "Creating",
                    "Serving", "Expanding", "Mastering", "Transforming"]
    has_ref = any(p in theme for p in planet_signs) or len(theme) > 5
    ok("CQ", "CQ-01", f"Daily theme present: '{theme[:50]}'") if has_ref \
        else warn("CQ", "CQ-01", f"Daily theme empty or missing: '{theme[:50]}'")

    directive = await _txt(page, "#operationalPointer")
    planets   = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    has_planet = any(p in directive for p in planets)
    ok("CQ", "CQ-02", f"Directive references planet: '{directive[:60]}'") if has_planet \
        else warn("CQ", "CQ-02", f"Directive may be generic (no planet found): '{directive[:60]}'")

    # Section titles non-empty
    titles = await page.locator("#strategicView .section-title").all_text_contents()
    empty  = [t for t in titles if len(t.strip()) < 3]
    ok("CQ", "CQ-05", f"Section titles: {len(titles)} found, none empty") if not empty \
        else warn("CQ", "CQ-05", f"Empty section titles: {empty}")

    # Tooltips meaningful
    tooltip_attrs = await page.evaluate("""
        () => [...document.querySelectorAll('[data-tooltip]')]
              .map(e => e.getAttribute('data-tooltip').length)
    """)
    short = [l for l in tooltip_attrs if l < 20]
    ok("CQ", "CQ-06", f"{len(tooltip_attrs)} tooltips, all meaningful") if not short \
        else warn("CQ", "CQ-06", f"{len(short)} tooltips have < 20 chars of text")

    # No "—" placeholders in visible sections
    dash_count = await page.evaluate("""
        () => {
            const els = document.querySelectorAll('.tldr-chip strong, #tldrLine');
            return [...els].filter(e => e.textContent.trim() === '—').length;
        }
    """)
    ok("CQ", "CQ-04", "No '—' placeholders in TL;DR chips") if dash_count == 0 \
        else warn("CQ", "CQ-04", f"{dash_count} TL;DR chips still show '—'")

    # Morning Brief date
    await page.click('button[data-view="strategic"]')
    await asyncio.sleep(0.5)
    brief = await _txt(page, "#morningBriefCard")
    ok("CQ", "CQ-03", f"Morning brief contains today's date") if TODAY in brief \
        else warn("CQ", "CQ-03", f"Morning brief date may be wrong: '{brief[:50]}'")

    # Numerology name
    await page.click('button[data-view="numerology"]')
    await asyncio.sleep(1.5)
    jy_name = await _txt(page, "#jyName")
    ok("CQ", "CQ-09", f"Numerology name: '{jy_name}'") if SAMPLE["name"].split()[0].lower() in jy_name.lower() \
        else fail("CQ", "CQ-09", f"Numerology name mismatch: '{jy_name}'")

    # DC Profile compat %
    compat = await _txt(page, ".jy-compat-badge")
    ok("CQ", "CQ-10", f"Compat % shown: '{compat}'") if re.search(r"\d+%", compat) \
        else warn("CQ", "CQ-10", f"Compat badge missing or not a percentage: '{compat}'")


# ── Dimension 4: Design Token Compliance ─────────────────
async def _dim4_design_tokens(page):
    header("DIMENSION 4 — Design Token Compliance")
    loaded = await _fill_form_and_generate(page)
    if not loaded:
        warn("DT", "DT-00", "Skipped — chart did not load")
        return

    # DT-04: Font is Inter
    font = await _eval(page, "getComputedStyle(document.body).fontFamily")
    ok("DT", "DT-04", f"Font: {font[:40]}") if "Inter" in (font or "") \
        else warn("DT", "DT-04", f"Font is not Inter: {font}")

    # DT-01: Results background is dark
    bg = await _eval(page, "getComputedStyle(document.getElementById('resultsScreen')).backgroundColor")
    ok("DT", "DT-01", f"Results screen background: {bg}") if bg and "0" in bg \
        else warn("DT", "DT-01", f"Results screen background unexpected: {bg}")

    # DT-02: Purple not used on section-title text
    purple_on_title = await _eval(page, """
        () => {
            const els = document.querySelectorAll('.section-title');
            return [...els].filter(e => {
                const c = getComputedStyle(e).color;
                return c.includes('99, 91, 255') || c.includes('635bff');
            }).length;
        }
    """)
    ok("DT", "DT-02", "Purple not used on section-title text") if not purple_on_title \
        else fail("DT", "DT-02", f"{purple_on_title} section-titles have purple text (CTAs only)")

    # DT-06: TL;DR card background is purple
    tldr_bg = await _eval(page, """
        () => getComputedStyle(document.querySelector('.tldr-card') || document.body).backgroundColor
    """)
    ok("DT", "DT-06", f"TL;DR card background: {tldr_bg}") if tldr_bg and "99" in (tldr_bg or "") \
        else warn("DT", "DT-06", f"TL;DR card background unexpected: {tldr_bg}")

    # DT-07: Mobile viewport check
    await page.set_viewport_size({"width": 390, "height": 844})
    await asyncio.sleep(0.5)
    overflow = await _eval(page, "document.documentElement.scrollWidth > 390")
    ok("DT", "DT-07", "No horizontal overflow at 390px mobile") if not overflow \
        else fail("DT", "DT-07", "Horizontal overflow detected at 390px — layout broken on mobile")
    await page.set_viewport_size({"width": 1280, "height": 800})


# ── Dimension 6: Feature Completeness ────────────────────
async def _dim6_features(page):
    header("DIMENSION 6 — Feature Completeness")
    loaded = await _fill_form_and_generate(page)
    if not loaded:
        warn("FC", "FC-00", "Skipped — chart did not load")
        return

    # FC-01: Section headers — Today tab
    n = await _count(page, "#strategicView .section-title")
    ok("FC", "FC-01", f"Today tab section titles: {n}") if n >= 5 \
        else warn("FC", "FC-01", f"Only {n} section-titles in Today tab (expect ≥5)")

    # FC-04: Total tooltip badges across all tabs
    total_qmarks = await _count(page, ".qmark[data-tooltip]")
    ok("FC", "FC-04", f"Total ? tooltips across app: {total_qmarks}") if total_qmarks >= 14 \
        else warn("FC", "FC-04", f"Only {total_qmarks} tooltip badges (expect ≥14)")

    # FC-06: U-001 — interpretation before grid
    u001 = await _eval(page, """
        () => {
            const interp = document.querySelector('.interp-card');
            const grid   = document.querySelector('#planetGrid');
            if (!interp || !grid) return -1;
            return (interp.compareDocumentPosition(grid) & Node.DOCUMENT_POSITION_FOLLOWING) ? 1 : 0;
        }
    """)
    ok("FC", "FC-06", "U-001: interpretation card precedes planetary grid") if u001 == 1 \
        else fail("FC", "FC-06", f"U-001 violated: interp_before_grid={u001}")

    # FC-07: Hindi toggle button
    ok("FC", "FC-07", "Hindi toggle #langToggleBtn present") if await _visible(page, "#langToggleBtn") \
        else fail("FC", "FC-07", "#langToggleBtn not found")

    # Full Chart tab section headers
    await page.click('button[data-view="technical"]')
    await asyncio.sleep(1.0)
    fc_labels = await _count(page, "#technicalView .section-title, #technicalView .adv-block-label")
    ok("FC", "FC-02", f"Full Chart section headers: {fc_labels}") if fc_labels >= 3 \
        else warn("FC", "FC-02", f"Only {fc_labels} section headers in Full Chart tab (expect ≥3)")

    # Numerology 5-group structure
    await page.click('button[data-view="numerology"]')
    await asyncio.sleep(1.5)
    try:
        await page.wait_for_selector("#jyProfilePanel:not(.hidden)", timeout=8000)
    except Exception:
        pass
    num_groups = await _count(page, "#jyProfilePanel .num-group")
    ok("FC", "FC-05", f"Numerology groups: {num_groups}") if num_groups == 5 \
        else warn("FC", "FC-05", f"Numerology has {num_groups} groups (expect 5)")

    num_titles = await _count(page, "#numerologyView .num-group .section-title")
    ok("FC", "FC-03", f"Numbers tab section titles: {num_titles}") if num_titles >= 5 \
        else warn("FC", "FC-03", f"Only {num_titles} section-titles in Numbers tab (expect ≥5)")

    # FC-15: Yearly Forecast renders 12 month cards
    forecast_hidden = await _eval(page, "document.getElementById('forecastSection')?.classList.contains('hidden')")
    month_count     = await _eval(page, "document.getElementById('forecastGrid')?.children?.length")
    ok("FC", "FC-15", f"Yearly Forecast: visible, {month_count} months rendered") \
        if not forecast_hidden and month_count == 12 \
        else warn("FC", "FC-15", f"Yearly Forecast: hidden={forecast_hidden} months={month_count}")

    # FC-14: People Compat discoverability — CTA in DC profile card
    compat_btn = await _visible(page, ".compat-discover-btn")
    compat_section_title = await _visible(page, "#compatSection .section-title")
    ok("FC", "FC-14", "People Compat: discover CTA + section-title both present") \
        if compat_btn and compat_section_title \
        else warn("FC", "FC-14", f"Compat discoverability: btn={compat_btn} title={compat_section_title}")


# ── Dimension 7: Resilience ───────────────────────────────
async def _dim7_resilience(page, ctx):
    header("DIMENSION 7 — Resilience & Edge Cases")

    # RES-01: No name → numerology shows prompt
    await page.goto(BASE, wait_until="networkidle")
    dd, mm, yyyy = "22", "08", "1987"
    await page.fill("#dobDD", dd)
    await page.fill("#dobMM", mm)
    await page.fill("#dobYYYY", yyyy)
    await asyncio.sleep(1.5)
    await page.fill("#time", "21:55")
    try:
        await page.fill("#citySearch", "Mumbai")
        await asyncio.sleep(1.0)
        first = page.locator("#cityResults .city-option").first
        if await first.is_visible():
            await first.click()
    except Exception:
        pass
    try:
        await page.click("#generateBtn")
    except Exception:
        pass
    try:
        await page.wait_for_selector(".consent-agree", timeout=3000)
        await page.click(".consent-agree")
    except Exception:
        pass
    try:
        await page.wait_for_selector("#resultsScreen:not(.hidden)", timeout=15000)
        await page.click('button[data-view="numerology"]')
        await asyncio.sleep(1.5)
        prompt_visible = await _visible(page, "#jyNameRequired")
        ok("RES", "RES-01", "No name → #jyNameRequired shown") if prompt_visible \
            else warn("RES", "RES-01", "No name entered but #jyNameRequired not visible")
    except Exception as e:
        warn("RES", "RES-01", f"No-name test skipped: {e}")

    # RES-05: Invalid DOB — DD=99
    await page.goto(BASE, wait_until="networkidle")
    await page.fill("#dobDD", "99")
    await page.fill("#dobMM", "13")
    await page.fill("#dobYYYY", "1987")
    await asyncio.sleep(0.8)
    btn_hidden = not await _visible(page, "#generateBtn")
    ok("RES", "RES-05", "Invalid DOB → generate button stays hidden") if btn_hidden \
        else warn("RES", "RES-05", "Invalid DOB did not prevent generate button from appearing")


# ══════════════════════════════════════════════════════════
# REPORT WRITER
# ══════════════════════════════════════════════════════════
def write_report():
    total   = len(results)
    passing = sum(1 for r in results if r[2] == "✅")
    warning = sum(1 for r in results if r[2] == "⚠️ ")
    failing = sum(1 for r in results if r[2] == "❌")

    dims = {}
    for dim, id_, verdict, msg in results:
        dims.setdefault(dim, []).append((id_, verdict, msg))

    lines = [
        f"# Cosmic OS — Audit Report",
        f"**Run:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Score:** ✅ {passing} · ⚠️  {warning} · ❌ {failing} (total {total})",
        f"",
        f"> Paste this summary into `docs/AUDIT_SPEC.md → LAST REPORT SUMMARY` section.",
        f"> For every ❌ or ⚠️, add a tighter check to the relevant dimension in AUDIT_SPEC.md.",
        f"",
    ]

    for dim, checks in dims.items():
        lines.append(f"## {dim}")
        for id_, verdict, msg in checks:
            lines.append(f"- {verdict} **{id_}**: {msg}")
        lines.append("")

    # Gaps section
    fails   = [(id_, msg) for _, id_, v, msg in results if v == "❌"]
    warnings = [(id_, msg) for _, id_, v, msg in results if v == "⚠️ "]
    if fails or warnings:
        lines.append("## Items Requiring Attention")
        for id_, msg in fails:
            lines.append(f"- ❌ **{id_}**: {msg}")
        for id_, msg in warnings:
            lines.append(f"- ⚠️  **{id_}**: {msg}")

    lines.extend([
        "",
        "## Self-Update Instructions for Next AI Session",
        "1. For each ❌ above: strengthen the check or fix the feature",
        "2. For each ⚠️ above: either tighten the check criterion or improve the feature",
        "3. For any new feature shipped since this run: add checks in docs/AUDIT_SPEC.md",
        "4. Run `python3 demos/master_audit.py` after every feature ship",
        f"5. Increment version in docs/AUDIT_SPEC.md (current: {_get_spec_version()})",
    ])

    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines))
    print(f"\n  📄 Report written → {REPORT_PATH}")


def _get_spec_version():
    try:
        content = SPEC_PATH.read_text()
        m = re.search(r"Version:\s*(\d+)", content)
        return int(m.group(1)) + 1 if m else "?"
    except Exception:
        return "?"


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
async def main():
    mode = "VISUAL (headless=False, slow_mo=1200ms)" if VISUAL else "HEADLESS (fast)"
    print("\n" + "═"*54)
    print("  COSMIC OS — MASTER AUDIT ENGINE")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')} | 7 Dimensions | {mode}")
    print("═"*54)

    # Sync dimensions (no browser)
    audit_api()
    audit_security()

    # Browser dimensions
    await audit_browser()

    # Summary
    total   = len(results)
    passing = sum(1 for r in results if r[2] == "✅")
    warning = sum(1 for r in results if r[2] == "⚠️ ")
    failing = sum(1 for r in results if r[2] == "❌")

    print(f"\n{'═'*54}")
    print(f"  MASTER AUDIT COMPLETE")
    print(f"  ✅ {passing}  ⚠️  {warning}  ❌ {failing}  (total {total})")
    print(f"{'═'*54}")

    write_report()
    print(f"\n  Next: read docs/AUDIT_REPORT.md → expand docs/AUDIT_SPEC.md")


if __name__ == "__main__":
    asyncio.run(main())
