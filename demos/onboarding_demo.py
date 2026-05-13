import asyncio
from playwright.async_api import async_playwright
import time

async def onboarding_demo():
    async with async_playwright() as p:
        # Launch browser with "Claude-style" slow_mo for institutional satisfaction
        browser = await p.chromium.launch(headless=False, slow_mo=600)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        print("Opening browser for New User Onboarding Demo...")
        await page.goto("http://127.0.0.1:5004")
        await asyncio.sleep(2)

        # Simulating authentication via cookie with a unique email to trigger "New User" logic
        unique_email = f"executive_{int(time.time())}@psbc.com"
        print(f"Authenticating as new user: {unique_email}")
        await context.add_cookies([{
            "name": "user_email",
            "value": unique_email,
            "url": "http://127.0.0.1:5004"
        }])
        
        print("Reloading to trigger Sanctuary Recognition...")
        await page.reload()
        await asyncio.sleep(3)

        # Check for Welcome Toast
        print("Observing 'Welcome' Sanctuary recognition...")
        await page.wait_for_selector(".welcome-toast", state="attached", timeout=10000)
        await asyncio.sleep(4)

        print("Step 1: Progressive Input - Entering Birth City (Simulated Typing)...")
        # Typing triggers the debounced Nominatim search
        await page.type("#citySearch", "New Delhi", delay=150)
        await page.wait_for_selector(".city-item")
        await asyncio.sleep(1)

        print("Selecting city to reveal progressive Date/Time fields...")
        await page.click(".city-item:first-child")
        await asyncio.sleep(2)

        print("Step 2: Entering Birth Date and Time...")
        await page.fill("#date", "1995-10-15")
        await asyncio.sleep(1)
        await page.fill("#time", "08:15")
        await asyncio.sleep(2)

        print("Step 3: Morphing to Dashboard (The Satisfaction Loop)...")
        await page.click("#generateBtn")

        print("Waiting for Strategic Dashboard reveal...")
        await page.wait_for_selector("#resultsScreen:not(.hidden)")
        await asyncio.sleep(5)

        print("Step 4: Reviewing Strategic Alerts and Morning Brief...")
        await page.evaluate("window.scrollTo({top: 400, behavior: 'smooth'})")
        await asyncio.sleep(6)

        print("Step 5: Verifying Persistent Session (Direct Landing)...")
        await page.goto("http://127.0.0.1:5004")
        await page.wait_for_selector("#resultsScreen:not(.hidden)")
        print("Session persisted. Bypassed landing screen successfully.")
        await asyncio.sleep(4)

        print("Onboarding flow verified. PSBC Premium Standards met.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(onboarding_demo())
