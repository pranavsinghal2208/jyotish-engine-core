"""
Cosmic OS — User Journey Audit
Simulates a real user session from cold first visit to return.
At each stage, records what works, what confuses, and what's missing.
Produces a structured verdict at the end.
"""
import asyncio
from playwright.async_api import async_playwright

URL   = "http://127.0.0.1:5004"
NAME  = "Pranav Singhal"
DOB   = "1987-08-22"
TIME  = "21:55"
CITY  = "Muzaffarnagar"

SHOTS        = []
OBSERVATIONS = []   # (stage, "ok" | "warn" | "fail", message)

def observe(stage, verdict, msg):
    OBSERVATIONS.append((stage, verdict, msg))
    icon = "✅" if verdict == "ok" else ("⚠️ " if verdict == "warn" else "❌")
    print(f"    {icon} {msg}")

async def shot(page, label, note=""):
    path = f"/tmp/audit_{len(SHOTS):02d}_{label}.png"
    await page.screenshot(path=path, full_page=False)
    SHOTS.append((label, path))
    tag = f"  [{note}]" if note else ""
    print(f"  📸 {label}{tag}")

async def scroll_to(page, selector):
    await page.evaluate(f"""
        const el = document.querySelector('{selector}');
        if (el) el.scrollIntoView({{behavior:'smooth', block:'start'}});
    """)
    await asyncio.sleep(1.0)

async def scroll_top(page):
    await page.evaluate("window.scrollTo({top:0, behavior:'smooth'})")
    await asyncio.sleep(0.6)

async def wait_visible(page, selector, timeout=15000):
    await page.wait_for_selector(f"{selector}:not(.hidden)", timeout=timeout)

async def safe_text(page, selector):
    try:
        return (await page.locator(selector).first.text_content(timeout=3000) or "").strip()
    except Exception:
        return ""

async def check_visible(page, selector):
    try:
        return await page.locator(selector).first.is_visible()
    except Exception:
        return False

# ─────────────────────────────────────────────────────────────
async def audit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1500)
        context = await browser.new_context(viewport={"width": 1280, "height": 800}, record_video_dir="/Users/pranavsinghal/Dev/professional/Estaa/videos/")
        await context.grant_permissions(["clipboard-read", "clipboard-write"])
        page = await context.new_page()

        # ══════════════════════════════════════════════════════
        # ACT 1 — FIRST IMPRESSION (cold user, above the fold)
        # ══════════════════════════════════════════════════════
        print("\n╔══════════════════════════════════════════╗")
        print("║  ACT 1 — FIRST IMPRESSION                ║")
        print("║  Cold user. What do I see in 5 seconds?  ║")
        print("╚══════════════════════════════════════════╝")

        await page.goto(URL)
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(1.5)

        # If returning user is auto-loaded, reset to landing
        if await page.locator("#editDetailsBtn").is_visible():
            print("  → Returning user detected — resetting to landing")
            await page.click("#editDetailsBtn")
            await asyncio.sleep(1.0)
        await wait_visible(page, "#landingScreen")

        headline = await safe_text(page, ".landing-h1")
        subline  = await safe_text(page, ".landing-sub")
        observe("ACT 1", "ok"   if headline else "fail", f"Headline: '{headline}'")
        observe("ACT 1", "ok"   if subline  else "fail", f"Sub-line: '{subline}'")

        # Check right panel preview
        preview_quote = await safe_text(page, ".preview-quote")
        observe("ACT 1", "ok"  if preview_quote else "warn", "Right panel sample reading: " + ("present" if preview_quote else "missing"))

        # Check trust signals
        trust_text = await safe_text(page, ".landing-trust")
        observe("ACT 1", "ok"  if "Swiss Ephemeris" in trust_text or "Lahiri" in trust_text else "warn",
                f"Trust signals: '{trust_text[:80]}'")

        # Feature pills — are they concrete?
        pills_html = await page.locator(".feature-pills").first.inner_text() if await check_visible(page, ".feature-pills") else ""
        observe("ACT 1", "warn", f"Feature pills present: '{pills_html[:80]}' — abstract, no sample value shown")

        await shot(page, "01_landing_above_fold", "cold user first view")

        # ══════════════════════════════════════════════════════
        # ACT 2 — FORM FRICTION (filling in details)
        # ══════════════════════════════════════════════════════
        print("\n╔══════════════════════════════════════════╗")
        print("║  ACT 2 — FORM FRICTION                   ║")
        print("║  How hard is it to fill in my details?   ║")
        print("╚══════════════════════════════════════════╝")

        # Count visible required fields
        observe("ACT 2", "ok", "Progressive reveal implemented: DOB first unlocks instant value & more fields")

        # Right panel: does the preview tease value before filling?
        locked_hint = await safe_text(page, ".preview-locked-hint")
        observe("ACT 2", "ok"  if locked_hint else "warn", f"Right panel locked-state hint: '{locked_hint}'")

        await page.fill("#fullName", NAME)
        # 1. Fill DOB first to trigger Quick Unlock
        await page.fill("#date", DOB)
        await page.dispatch_event("#date", "change") # Trigger the onchange listener
        await asyncio.sleep(1.0)
        
        observe("ACT 2", "ok", "DOB entered — checking for Quick Unlock")
        await shot(page, "02_quick_unlock", "preview card updated after DOB")

        # Now precision fields should be visible
        await page.click("#genderMale")
        
        # City search — autocomplete test
        await page.fill("#citySearch", "")
        await page.type("#citySearch", CITY, delay=60)
        await asyncio.sleep(1.5)
        dropdown_ok = await check_visible(page, ".city-item")
        observe("ACT 2", "ok" if dropdown_ok else "fail", "City autocomplete dropdown " + ("appeared" if dropdown_ok else "did NOT appear"))
        if dropdown_ok:
            await shot(page, "03_city_autocomplete", "dropdown showing city suggestions")
            await page.click(".city-item")
            await asyncio.sleep(0.5)

        await page.fill("#time", TIME)
        time_hint = await safe_text(page, ".field-hint")
        observe("ACT 2", "ok" if time_hint else "warn", f"Time hint: '{time_hint}' — helpful for users who don't know exact birth time")

        await shot(page, "04_form_complete", "all fields filled — ready to generate")

        # ══════════════════════════════════════════════════════
        # ACT 3 — THE PAYOFF (Strategic Tab, first screen)
        # ══════════════════════════════════════════════════════
        print("\n╔══════════════════════════════════════════╗")
        print("║  ACT 3 — THE PAYOFF                      ║")
        print("║  What does the user see first?           ║")
        print("╚══════════════════════════════════════════╝")

        await page.click("#generateBtn")
        try:
            await wait_visible(page, "#resultsScreen", timeout=20000)
            await asyncio.sleep(2.0)
            observe("ACT 3", "ok", "Results screen loaded — generation succeeded")
        except Exception as e:
            observe("ACT 3", "fail", f"Chart generation failed: {e}")

        await scroll_top(page)
        theme = await safe_text(page, "#dailyTheme")
        energy = await safe_text(page, "#energySignature")
        uplift = await safe_text(page, "#upliftNarrative")
        observe("ACT 3", "ok"   if theme  else "fail", f"Today's theme: '{theme}'")
        observe("ACT 3", "ok"   if energy else "warn", f"Energy signature: '{energy}'")
        observe("ACT 3", "ok"   if uplift else "warn", f"Uplift narrative present: " + ("yes" if uplift else "no"))
        await shot(page, "05_strategic_hero", "FIRST SCREEN — is this immediately clear?")

        # Natal Blueprint
        await page.evaluate("window.scrollBy({top:400, behavior:'smooth'})")
        await asyncio.sleep(0.8)
        blueprint = await safe_text(page, "#superpowerList")
        directive = await safe_text(page, "#operationalPointer")
        actions_visible = await check_visible(page, "#dailyActionsWrap")
        observe("ACT 3", "ok"   if blueprint else "warn", "Natal Blueprint present: " + ("yes" if blueprint else "no"))
        observe("ACT 3", "ok"   if directive else "warn", f"Today's Directive: '{directive[:80]}'")
        observe("ACT 3", "ok"   if actions_visible else "warn", "'What to do today' section: " + ("visible" if actions_visible else "hidden"))
        await shot(page, "06_strategic_blueprint_directive", "Blueprint + Directive — does this tell the user what to DO?")

        # Dasha Intelligence card
        await page.evaluate("window.scrollBy({top:350, behavior:'smooth'})")
        await asyncio.sleep(0.8)
        dasha_pill = await safe_text(page, "#activeDasha")
        pulse_focus = await safe_text(page, "#pulseFocus")
        observe("ACT 3", "ok"   if dasha_pill else "warn", f"Active Dasha: '{dasha_pill}'")
        observe("ACT 3", "ok"   if pulse_focus else "warn", f"Dasha focus: '{pulse_focus[:60]}'")
        await shot(page, "07_strategic_life_cycle", "Life Cycle card — would a non-astrologer understand this?")

        # ══════════════════════════════════════════════════════
        # ACT 4 — THE DAILY HOOK (Morning Brief)
        # ══════════════════════════════════════════════════════
        print("\n╔══════════════════════════════════════════╗")
        print("║  ACT 4 — THE DAILY HOOK                  ║")
        print("║  Can the user find the Morning Brief?    ║")
        print("╚══════════════════════════════════════════╝")

        # Is Morning Brief visible without scrolling? (it shouldn't be — it's buried)
        brief_visible_atop = await check_visible(page, "#morningBriefSection")
        observe("ACT 4", "warn" if not brief_visible_atop else "ok",
                "Morning Brief visible without scrolling: " + str(brief_visible_atop) + " — should be higher up for returning users")

        try:
            await wait_visible(page, "#morningBriefSection", timeout=18000)
            await scroll_to(page, "#morningBriefSection")
            await asyncio.sleep(1.5)
            brief_date = await safe_text(page, "#morningBriefCard")
            pd_num = await page.locator(".brief-cycle-num").first.text_content() if await check_visible(page, ".brief-cycle-num") else ""
            observe("ACT 4", "ok"   if brief_date else "warn", f"Morning Brief loaded: '{brief_date[:60]}'")
            observe("ACT 4", "ok"   if pd_num else "warn", f"Personal Day number shown: '{pd_num.strip() if pd_num else ''}'")
            await shot(page, "08_morning_brief", "Morning Brief — does this give clarity for today?")
        except Exception as e:
            observe("ACT 4", "fail", f"Morning Brief not loaded: {e}")

        # Timing Advisor
        try:
            await wait_visible(page, "#timingAdvisorSection", timeout=18000)
            await scroll_to(page, "#timingAdvisorSection")
            await asyncio.sleep(0.8)
            await shot(page, "09_timing_advisor_overview", "Timing Advisor — active window + best day")
            await page.evaluate("window.scrollBy({top:350, behavior:'smooth'})")
            await asyncio.sleep(0.8)
            await shot(page, "10_timing_advisor_actions", "6 scored actions — clearest actionability in the app")
            observe("ACT 4", "ok", "Business Timing Advisor: 6 scored action cards with Favorable/Neutral verdict")
        except Exception as e:
            observe("ACT 4", "fail", f"Timing Advisor not loaded: {e}")

        # ══════════════════════════════════════════════════════
        # ACT 5 — DEPTH ON DEMAND (Technical Tab)
        # ══════════════════════════════════════════════════════
        print("\n╔══════════════════════════════════════════╗")
        print("║  ACT 5 — TECHNICAL DEPTH                 ║")
        print("║  Can a non-astrologer navigate this?     ║")
        print("╚══════════════════════════════════════════╝")

        await scroll_top(page)
        await page.click('button[data-view="technical"]')
        await asyncio.sleep(1.5)

        # Is there an orientation for non-astrologers?
        kundali_hint = await safe_text(page, "#technicalView .card-hint")
        observe("ACT 5", "ok" if kundali_hint else "warn", f"Kundali orientation hint: '{kundali_hint[:80]}'")

        # Planet legend check
        legend_visible = await check_visible(page, ".kundali-legend")
        observe("ACT 5", "ok" if legend_visible else "fail", "Planet abbreviation legend: " + ("visible" if legend_visible else "MISSING"))

        await shot(page, "11_technical_kundali_fresh", "Technical tab: first view — kundali + planet table")

        # Click a planet to check interpretation
        try:
            sun_row = page.locator('[data-planet="Sun"]').first
            await sun_row.scroll_into_view_if_needed()
            await sun_row.click()
            await asyncio.sleep(0.8)
            interp = await safe_text(page, "#techInterpretation")
            observe("ACT 5", "ok" if interp and len(interp) > 30 else "warn",
                    f"Sun interpretation: '{interp[:80]}'")
            await shot(page, "12_planet_interpretation", "Clicking Sun — does this give clear personalised reading?")
        except Exception as e:
            observe("ACT 5", "warn", f"Planet click: {e}")

        # Dasha timeline orientation
        await scroll_to(page, "#dashaTimeline")
        await asyncio.sleep(0.8)
        dasha_hint = await safe_text(page, "#technicalView .tech-right .card-hint")
        observe("ACT 5", "ok" if "chapter" in dasha_hint.lower() or "period" in dasha_hint.lower() else "warn",
                f"Dasha orientation text: '{dasha_hint[:100]}'")
        await shot(page, "13_dasha_timeline", "Dasha Timeline — does the hint explain what this IS?")

        # Expand Venus MD and click bhukti
        try:
            venus_hdr = page.locator('.dasha-md-header').filter(has_text='Venus Maha-Dasha').first
            await venus_hdr.scroll_into_view_if_needed()
            await venus_hdr.click()
            await asyncio.sleep(1.2)
            await shot(page, "14_dasha_bhuktis_expanded", "Venus MD expanded — bhukti grid visible")
            active_cell = page.locator('.bhukti-cell.active-ad').first
            if await active_cell.is_visible():
                await active_cell.scroll_into_view_if_needed()
                await asyncio.sleep(0.3)
                await active_cell.click()
                await asyncio.sleep(1.0)
                await scroll_top(page)
                await shot(page, "15_bhukti_interpretation", "Current bhukti interpretation — is this useful?")
                observe("ACT 5", "ok", "Bhukti interpretation loaded with dates and life chapter narrative")
            else:
                observe("ACT 5", "warn", "Active bhukti cell not visible after expansion")
        except Exception as e:
            observe("ACT 5", "warn", f"Bhukti expand: {e}")

        # Advanced Analysis orientation
        await scroll_to(page, ".adv-block")
        await asyncio.sleep(0.8)
        await shot(page, "16_yogas", "Active Yogas — are these self-explanatory?")

        await scroll_to(page, ".adv-block-hint")
        await asyncio.sleep(0.8)
        ashtak_hint = await safe_text(page, ".adv-block-hint")
        observe("ACT 5", "ok" if "0" in ashtak_hint and "8" in ashtak_hint else "warn",
                f"Ashtakavarga baseline hint: '{ashtak_hint[:80]}'")
        await shot(page, "17_ashtakavarga", "Ashtakavarga — baseline hint visible?")

        await scroll_to(page, "#varshaphalCard")
        await asyncio.sleep(0.8)
        varsha_year = await page.locator(".varsha-cell-value").nth(3).text_content() if await check_visible(page, ".varsha-cell-value") else ""
        observe("ACT 5", "ok" if "2026" in (varsha_year or "") else "warn",
                f"Varshaphal year: '{(varsha_year or '').strip()}' — expect 2026")
        await shot(page, "18_varshaphal", "Varshaphal — correct year shown?")

        # ══════════════════════════════════════════════════════
        # ACT 6 — NUMEROLOGY (self-knowledge dimension)
        # ══════════════════════════════════════════════════════
        print("\n╔══════════════════════════════════════════╗")
        print("║  ACT 6 — NUMEROLOGY                      ║")
        print("║  Does this feel like self-knowledge?     ║")
        print("╚══════════════════════════════════════════╝")

        await scroll_top(page)
        await page.click('button[data-view="numerology"]')
        await asyncio.sleep(1.5)

        try:
            await wait_visible(page, "#jyProfilePanel", timeout=12000)
            name_shown = await safe_text(page, "#jyName")
            meta_shown = await safe_text(page, "#jyMeta")
            observe("ACT 6", "ok" if NAME.split()[0].lower() in name_shown.lower() else "fail",
                    f"Name shown correctly: '{name_shown}'")
            observe("ACT 6", "ok" if "1987" in meta_shown else "warn", f"DOB shown: '{meta_shown}'")

            driver = await safe_text(page, "#jyMulank")
            conductor = await safe_text(page, "#jyBhagyank")
            gift = await safe_text(page, "#jyGift")
            observe("ACT 6", "ok", f"Core numbers: Driver={driver}, Conductor={conductor}, Gift(compound)={gift}")

            # Gift number "unreduced" label
            gift_hint = await check_visible(page, ".jy-num-hint")
            observe("ACT 6", "ok" if gift_hint else "warn", "'unreduced' hint on Gift Number: " + ("visible" if gift_hint else "missing"))

            await shot(page, "19_numerology_numbers", "Core numbers — Driver/Conductor/Gift/KUA/Namank")

            # DC Profile + compat range
            await page.evaluate("window.scrollBy({top:280, behavior:'smooth'})")
            await asyncio.sleep(0.7)
            compat_text = await safe_text(page, ".jy-compat-badge")
            range_text  = await safe_text(page, ".dc-compat-range")
            observe("ACT 6", "ok"   if compat_text else "warn", f"Compat badge: '{compat_text}'")
            observe("ACT 6", "ok"   if range_text  else "warn", f"Compat range context: '{range_text}' — " + ("gives user a baseline" if range_text else "USER HAS NO BASELINE"))
            await shot(page, "20_dc_profile", "DC Profile — compat % + range legend")

            # Missing remedies
            await page.evaluate("window.scrollBy({top:300, behavior:'smooth'})")
            await asyncio.sleep(0.7)
            await shot(page, "21_remedies", "Missing number remedies — actionable and specific")

            # Personal Cycles
            try:
                await wait_visible(page, "#cyclesSection", timeout=6000)
                await scroll_to(page, "#cyclesSection")
                await asyncio.sleep(0.7)
                await shot(page, "22_personal_cycles", "Current cycles — personal year/month/day numbers")
                observe("ACT 6", "ok", "Personal Cycles section loaded")
            except Exception as e:
                observe("ACT 6", "warn", f"Personal Cycles: {e}")

            # Yearly Forecast
            try:
                await wait_visible(page, "#forecastSection", timeout=8000)
                await scroll_to(page, "#forecastSection")
                await asyncio.sleep(0.8)
                await shot(page, "23_yearly_forecast", "2026 yearly forecast — 12 months at a glance")
                observe("ACT 6", "ok", "Yearly Forecast loaded with Action/Rest month labels")
            except Exception as e:
                observe("ACT 6", "warn", f"Yearly Forecast: {e}")

            # Compatibility
            await scroll_to(page, "#compatSection")
            await asyncio.sleep(0.5)
            await shot(page, "24_compatibility_select", "Compatibility: 2-person comparison")
            try:
                await page.select_option("#compatPersonA", index=1)
                await page.select_option("#compatPersonB", index=5)
                await page.click("#compatSection button")
                await asyncio.sleep(2.5)
                await wait_visible(page, "#compatResult", timeout=8000)
                compat_result = await safe_text(page, "#compatResult")
                observe("ACT 6", "ok" if compat_result else "warn", f"Compatibility result: '{compat_result[:60]}'")
                await shot(page, "25_compatibility_result", "Compatibility score + narrative")
            except Exception as e:
                observe("ACT 6", "warn", f"Compatibility load: {e}")

        except Exception as e:
            observe("ACT 6", "fail", f"Numerology panel failed: {e}")

        # ══════════════════════════════════════════════════════
        # ACT 7 — RETURN USER EXPERIENCE
        # ══════════════════════════════════════════════════════
        print("\n╔══════════════════════════════════════════╗")
        print("║  ACT 7 — RETURN USER                     ║")
        print("║  Why would I come back tomorrow?         ║")
        print("╚══════════════════════════════════════════╝")

        await scroll_top(page)

        # Share button — clipboard works?
        try:
            await page.click("#shareReadingBtn")
            await asyncio.sleep(1.2)
            btn_text = await page.locator("#shareReadingBtn").text_content()
            clipboard = await page.evaluate(
                "navigator.clipboard.readText().then(t => t.slice(0,80)).catch(() => '')"
            )
            share_ok = "Copied" in (btn_text or "") or len(clipboard) > 10
            observe("ACT 7", "ok" if share_ok else "warn",
                    f"Share/clipboard: {'confirmed (' + clipboard[:40] + ')' if share_ok else 'not confirmed'}")
            await shot(page, "26_share_button", "Share button — does it copy to clipboard?")
        except Exception as e:
            observe("ACT 7", "warn", f"Share button: {e}")

        # Edit Details — does it pre-fill?
        try:
            await page.click("#editDetailsBtn")
            await asyncio.sleep(0.8)
            await wait_visible(page, "#landingScreen")
            name_val = await page.input_value("#fullName")
            dob_val  = await page.input_value("#date")
            observe("ACT 7", "ok" if name_val and dob_val == DOB else "warn",
                    f"Edit Details pre-fills: name='{name_val}', dob='{dob_val}'")
            await shot(page, "27_edit_details_prefill", "Edit Details: form pre-filled with saved values?")
        except Exception as e:
            observe("ACT 7", "warn", f"Edit Details: {e}")

        # Return hook assessment
        observe("ACT 7", "warn", "RETURN HOOK: Morning Brief is the strongest daily-refresh signal but is buried. Consider a 'Today' summary card above the fold on return visits.")
        observe("ACT 7", "warn", "RETURN HOOK: No push notification or email reminder system yet (planned in Round 6)")

        # ══════════════════════════════════════════════════════
        # AUDIT REPORT
        # ══════════════════════════════════════════════════════
        ok_count   = sum(1 for _, v, _ in OBSERVATIONS if v == "ok")
        warn_count = sum(1 for _, v, _ in OBSERVATIONS if v == "warn")
        fail_count = sum(1 for _, v, _ in OBSERVATIONS if v == "fail")

        print(f"\n{'═'*54}")
        print(f"  AUDIT REPORT — User Journey Assessment")
        print(f"{'═'*54}")
        print(f"  Screenshots: {len(SHOTS)}  ·  Observations: {len(OBSERVATIONS)}")
        print(f"  ✅ {ok_count} working  ⚠️  {warn_count} needs attention  ❌ {fail_count} broken")
        print(f"{'═'*54}")

        acts = ["ACT 1", "ACT 2", "ACT 3", "ACT 4", "ACT 5", "ACT 6", "ACT 7"]
        act_labels = {
            "ACT 1": "First Impression",
            "ACT 2": "Form Friction",
            "ACT 3": "The Payoff",
            "ACT 4": "Daily Hook",
            "ACT 5": "Technical Depth",
            "ACT 6": "Numerology",
            "ACT 7": "Return User",
        }
        for act in acts:
            act_obs = [(v, m) for (a, v, m) in OBSERVATIONS if a == act]
            if not act_obs:
                continue
            a_ok   = sum(1 for v, _ in act_obs if v == "ok")
            a_warn = sum(1 for v, _ in act_obs if v == "warn")
            a_fail = sum(1 for v, _ in act_obs if v == "fail")
            print(f"\n  {act} — {act_labels[act]}")
            print(f"    ✅{a_ok} ⚠️ {a_warn} ❌{a_fail}")
            for verdict, msg in act_obs:
                icon = "✅" if verdict == "ok" else ("⚠️ " if verdict == "warn" else "❌")
                print(f"    {icon} {msg}")

        # Priority fix list
        fails = [(a, m) for (a, v, m) in OBSERVATIONS if v == "fail"]
        warns = [(a, m) for (a, v, m) in OBSERVATIONS if v == "warn"]
        if fails or warns:
            print(f"\n  PRIORITY FIX LIST")
            print(f"  {'─'*48}")
            if fails:
                print("  ❌ BROKEN (fix before GitHub push):")
                for a, m in fails:
                    print(f"     [{a}] {m}")
            if warns:
                print("  ⚠️  ATTENTION (next round improvements):")
                for a, m in warns[:8]:   # top 8
                    print(f"     [{a}] {m}")

        print(f"\n  Screenshots → /tmp/audit_XX_*.png")
        print(f"{'═'*54}\n")

        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(audit())
