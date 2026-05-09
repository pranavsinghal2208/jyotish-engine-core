import asyncio
from playwright.async_api import async_playwright

async def meticulous_audit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=2000)
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        
        # Capture console logs
        page.on("console", lambda msg: print(f"BROWSER LOG: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"BROWSER ERROR: {exc}"))

        print("🔍 Starting Meticulous Audit...")
        await page.goto("http://127.0.0.1:8000")
        
        print("⌨️ Entering Pincode: 251001...")
        await page.type("#citySearch", "251001", delay=200)
        await page.wait_for_selector(".city-item")
        await page.click(".city-item")
        
        print("🗓️ Entering Date & Time for Aug 22, 1987, 9:55 PM...")
        await page.fill("#date", "1987-08-22")
        await page.fill("#time", "21:55")
        await asyncio.sleep(2)
        
        print("🚀 Generating Analysis...")
        await page.click("#generateBtn")
        
        print("⏳ Waiting for Cosmic Engine...")
        try:
            await page.wait_for_selector("#results:not(.hidden)", timeout=30000)
        except Exception as e:
            print(f"❌ TIMEOUT: Results did not appear. Taking emergency screenshot.")
            await page.screenshot(path="emergency_fail.png")
            raise e
        
        print("👀 OBSERVING COACH VIEW...")
        await asyncio.sleep(5)
        
        print("📊 OBSERVING PRO VIEW...")
        await page.click("#proToggle")
        await asyncio.sleep(8)
        
        print("✅ Meticulous Audit Complete.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(meticulous_audit())
