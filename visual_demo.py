import asyncio
from playwright.async_api import async_playwright

SHOTS = []

async def shot(page, label):
    path = f"/tmp/cosmic_{len(SHOTS):02d}_{label}.png"
    await page.screenshot(path=path, full_page=False)
    SHOTS.append((label, path))
    print(f"  📸 {label} → {path}")

async def visual_satisfaction_loop():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=800)
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})

        # ── STEP 1: Landing page ──────────────────────────────────────────
        print("\n[1] Opening Cosmic OS...")
        await page.goto("http://127.0.0.1:5004")
        await page.wait_for_load_state("networkidle")
        await shot(page, "landing_empty")

        # ── STEP 2: Fill name ─────────────────────────────────────────────
        print("[2] Entering name: Pranav...")
        await page.fill("#fullName", "Pranav")
        await shot(page, "name_filled")

        # ── STEP 3: City search ───────────────────────────────────────────
        print("[3] Typing city: Muzaffarnagar...")
        await page.type("#citySearch", "Muzaffarnagar", delay=60)
        await asyncio.sleep(1)
        await page.wait_for_selector(".city-item", timeout=6000)
        await shot(page, "city_dropdown")

        print("[3b] Selecting first city result...")
        await page.click(".city-item")
        await asyncio.sleep(0.5)
        await shot(page, "city_selected")

        # ── STEP 4: Date + Time ───────────────────────────────────────────
        print("[4] Entering DOB: 22 Aug 1987, 21:55...")
        await page.fill("#date", "1987-08-22")
        await page.fill("#time", "21:55")
        await shot(page, "datetime_filled")

        # ── STEP 5: Generate ──────────────────────────────────────────────
        print("[5] Clicking Generate My Chart...")
        await page.click("#generateBtn")
        await page.wait_for_selector("#resultsScreen:not(.hidden)", timeout=15000)
        await asyncio.sleep(1.5)
        await shot(page, "strategic_top")

        # ── STEP 6: Scroll strategic view ────────────────────────────────
        print("[6] Scrolling Strategic View...")
        await page.evaluate("window.scrollTo({top: 400, behavior: 'smooth'})")
        await asyncio.sleep(1.2)
        await shot(page, "strategic_mid")

        await page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
        await asyncio.sleep(1.2)
        await shot(page, "strategic_bottom")

        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await asyncio.sleep(0.8)

        # ── STEP 7: Switch to Technical view ─────────────────────────────
        print("[7] Switching to Technical View...")
        await page.click('button[data-view="technical"]')
        await asyncio.sleep(1.2)
        await shot(page, "technical_top")

        # ── STEP 8: Tap Sun planet row ────────────────────────────────────
        print("[8] Tapping Sun planet row...")
        sun_row = page.locator('[data-planet="Sun"]')
        await sun_row.scroll_into_view_if_needed()
        await sun_row.click()
        await asyncio.sleep(1)
        await shot(page, "planet_sun_interp")

        print("[8b] Tapping Venus planet row...")
        venus_row = page.locator('[data-planet="Venus"]')
        await venus_row.scroll_into_view_if_needed()
        await venus_row.click()
        await asyncio.sleep(1)
        await shot(page, "planet_venus_interp")

        # ── STEP 9: Scroll to Dasha timeline ─────────────────────────────
        print("[9] Scrolling to Dasha timeline...")
        await page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
        await asyncio.sleep(1.2)
        await shot(page, "dasha_timeline")

        # ── STEP 10: Tap Venus Maha-Dasha header (shows MD interpretation) ──
        print("[10] Tapping Venus Maha-Dasha header...")
        venus_md = page.locator('.dasha-md-header').filter(has_text='Venus').first
        await venus_md.scroll_into_view_if_needed()
        await venus_md.click()
        await asyncio.sleep(1.5)
        # Scroll back to top to see interpretation panel
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await asyncio.sleep(1)
        await shot(page, "dasha_venus_md_interp")

        # ── STEP 11: Tap Saturn Bhukti inside Venus MD ───────────────────
        print("[11] Scrolling to Venus MD bhukti grid and tapping Saturn...")
        await asyncio.sleep(0.5)
        # Target the Venus MD item specifically
        venus_item = page.locator('.dasha-md-item').filter(has_text='Venus Maha-Dasha')
        venus_grid = venus_item.locator('.bhukti-grid')
        await venus_grid.scroll_into_view_if_needed()
        await asyncio.sleep(0.8)
        await shot(page, "dasha_bhuktis_visible")

        # Click the active Saturn bhukti (highlighted cell)
        try:
            saturn_cell = venus_item.locator('.bhukti-cell.active-ad')
            await saturn_cell.click(timeout=5000)
            await asyncio.sleep(1.5)
            await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
            await asyncio.sleep(1)
            await shot(page, "dasha_saturn_interp")
        except Exception as e:
            print(f"  (Saturn active-ad: {e})")
            # Fallback: first visible bhukti cell in Venus MD
            try:
                cell = venus_item.locator('.bhukti-cell').first
                await cell.click(timeout=3000)
                await asyncio.sleep(1.5)
                await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
                await asyncio.sleep(1)
                await shot(page, "dasha_bhukti_interp")
            except Exception as e2:
                print(f"  (bhukti fallback: {e2})")

        # ── STEP 12: Advanced Analysis in Technical tab ──────────────────
        print("[12] Scrolling to Advanced Analysis section...")
        await page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
        await asyncio.sleep(1.5)
        await shot(page, "advanced_analysis_yogas")

        # Scroll deeper to see Sade Sati + Mangal Dosha
        await page.evaluate("window.scrollBy({top: 600, behavior: 'smooth'})")
        await asyncio.sleep(1.2)
        await shot(page, "advanced_analysis_conditions")

        # Scroll to Ashtakavarga
        await page.evaluate("window.scrollBy({top: 600, behavior: 'smooth'})")
        await asyncio.sleep(1.2)
        await shot(page, "advanced_analysis_ashtakavarga")

        # Scroll to Divisional + Varshaphal
        await page.evaluate("window.scrollBy({top: 600, behavior: 'smooth'})")
        await asyncio.sleep(1.2)
        await shot(page, "advanced_analysis_varshaphal")

        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await asyncio.sleep(0.8)

        # ── STEP 13: Morning Brief + Timing Advisor in Strategic tab ─────
        print("[13] Viewing Morning Brief + Timing Advisor...")
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await asyncio.sleep(0.8)
        await page.click('button[data-view="strategic"]')
        await asyncio.sleep(2)
        await page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
        await asyncio.sleep(1.5)
        await shot(page, "morning_brief")
        await page.evaluate("window.scrollBy({top: 600, behavior: 'smooth'})")
        await asyncio.sleep(1.2)
        await shot(page, "timing_advisor_top")
        await page.evaluate("window.scrollBy({top: 600, behavior: 'smooth'})")
        await asyncio.sleep(1.2)
        await shot(page, "timing_advisor_grid")

        # ── STEP 14: Numerology tab ───────────────────────────────────────
        print("[14] Switching to Numerology tab...")
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await asyncio.sleep(0.8)
        await page.click('button[data-view="numerology"]')
        await asyncio.sleep(1.5)
        await shot(page, "numerology_tab_initial")

        # Wait for personal profile to auto-load
        try:
            await page.wait_for_selector('#jyProfilePanel:not(.hidden)', timeout=8000)
            print("  ✅ Personal numerology profile loaded")
            await shot(page, "numerology_profile_loaded")
            # Scroll to Personal Cycles
            await page.evaluate("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
            await asyncio.sleep(1.5)
            await shot(page, "personal_cycles")
            # Scroll to Compatibility section
            await page.evaluate("window.scrollBy({top: 600, behavior: 'smooth'})")
            await asyncio.sleep(1.2)
            await shot(page, "compatibility_section")
            # Click Compare
            try:
                await page.click('#compatSection .jy-load-btn', timeout=3000)
                await asyncio.sleep(2)
                await shot(page, "compatibility_result")
            except Exception as ce:
                print(f"  (compat click: {ce})")
        except Exception as e:
            print(f"  ⚠️  Profile did not load: {e}")
            await shot(page, "numerology_load_failed")

        print("\n✅ Visual Demo Complete.")
        print(f"   {len(SHOTS)} screenshots captured:\n")
        for label, path in SHOTS:
            print(f"   {path}")

        await asyncio.sleep(4)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(visual_satisfaction_loop())
