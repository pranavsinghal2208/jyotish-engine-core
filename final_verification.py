import asyncio
from playwright.async_api import async_playwright

async def final_verification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        
        print("🚀 Launching Final Verification for Cosmic OS...")
        await page.goto("http://127.0.0.1:8000")
        await asyncio.sleep(2)
        
        # Audit Onboarding UI (T4)
        print("👀 Auditing 'Mass-Scale' Onboarding Interface...")
        await page.evaluate("document.getElementById('authContainer').scrollInto_view = true")
        await asyncio.sleep(3)
        
        # Instructions for the user
        print("\n--- ACTION REQUIRED ---")
        print("1. In the browser window, click 'Continue with Google'.")
        print("2. Authenticate your account.")
        print("3. Once the 'Cosmic OS Connected' badge appears green, come back here.")
        
        # Wait for the user to perform the action (timeout 2 mins)
        print("\nWaiting for authentication success...")
        try:
            await page.wait_for_selector("#authStatus:not(.hidden)", timeout=120000)
            print("\n✅ AUTHENTICATION VERIFIED: 'Cosmic OS' is now connected to your live data.")
            
            # Step 2: Final Report Generation
            print("⌨️ Generating Integrated Performance Report...")
            await page.type("#citySearch", "251001", delay=100)
            await page.wait_for_selector(".city-item")
            await page.click(".city-item")
            await page.fill("#date", "1987-08-22")
            await page.fill("#time", "21:55")
            await page.click("#generateBtn")
            
            await page.wait_for_selector("#results:not(.hidden)")
            print("\n🌌 INTEGRATED REPORT GENERATED.")
            print("You can now see your actual meetings cross-referenced with your planetary strengths.")
            await asyncio.sleep(10)
            
        except Exception as e:
            print(f"\n❌ Verification Timed Out or Error: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(final_verification())
