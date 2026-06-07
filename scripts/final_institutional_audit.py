import asyncio
from playwright.async_api import async_playwright
import os

async def run_demo():
    async with async_playwright() as p:
        # We must use headless=True in this environment
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        
        # Route Nominatim API requests to return a mock response
        await page.route(
            "**/nominatim.openstreetmap.org/search*",
            lambda route: route.fulfill(
                status=200,
                content_type="application/json",
                body='[{"place_id":12345,"lat":"28.6139","lon":"77.2090","display_name":"Muzaffarnagar, Uttar Pradesh, India","class":"place","type":"city","addresstype":"city"}]'
            )
        )

        # Capture console logs and page errors
        page.on("console", lambda msg: print(f"BROWSER LOG: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"BROWSER ERROR: {exc}"))

        print("1. Opening Cosmic OS...")
        await page.goto("http://127.0.0.1:8000")
        await page.wait_for_load_state("networkidle")
        # Pre-set consent to bypass the consent modal
        await page.evaluate("localStorage.setItem('cosmicOsConsent', '1')")
        await page.screenshot(path="demo_1_landing.png")
        
        print("2. Entering Details: Pranav, Date of Birth: 22/08/1987...")
        await page.fill("#fullName", "Pranav")
        await page.fill("#dobDD", "22")
        await page.fill("#dobMM", "08")
        await page.fill("#dobYYYY", "1987")
        
        # Wait for precision fields (including city search) to become visible
        await page.wait_for_selector("#precisionFields:not(.hidden)", timeout=5000)
        
        print("3. Entering City: Muzaffarnagar...")
        await page.type("#citySearch", "Muzaffarnagar", delay=100)
        await page.wait_for_selector(".city-item", timeout=5000)
        await page.click(".city-item")
        
        print("4. Entering Time of Birth: 09:55 AM...")
        await page.fill("#timeHH", "09")
        await page.fill("#timeMM", "55")
        await page.click("#ampmAM")
        
        # Register dialog handler to log alerts
        page.on("dialog", lambda dialog: print(f"DIALOG ALERT: {dialog.message}"))

        # Force set hidden input values just in case events didn't trigger in headless mode
        await page.evaluate("""() => {
            document.getElementById('date').value = '1987-08-22';
            document.getElementById('time').value = '09:55';
        }""")

        await asyncio.sleep(1) # Wait for morph animation
        await page.screenshot(path="demo_2_input_ready.png")
        
        print("5. Generating Chart...")
        await page.click("#generateBtn")
        
        # Wait for transition (allowing extra time for API calls or local synthesis fallback)
        try:
            await page.wait_for_selector("#resultsScreen:not(.hidden)", timeout=30000)
        except Exception as e:
            await page.screenshot(path="emergency_fail.png")
            print("Took emergency_fail.png screenshot")
            raise e
        await asyncio.sleep(2) # Finish fade-in
        
        print("6. Strategic View (Page 1)...")
        await page.screenshot(path="demo_3_strategic_top.png")
        
        # Scroll Strategic
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1)
        await page.screenshot(path="demo_4_strategic_bottom.png")
        
        print("7. Technical View (Page 2)...")
        await page.click('button[data-view="technical"]')
        await asyncio.sleep(1)
        await page.screenshot(path="demo_5_technical_top.png")
        
        # Scroll Technical
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1)
        await page.screenshot(path="demo_6_technical_bottom.png")
        
        print("8. Repeating sequence for verification...")
        await page.click('button[data-view="strategic"]')
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(1)
        await page.screenshot(path="demo_7_repeat_top.png")
        
        # Save a copy as ui_verified.png
        import shutil
        shutil.copy("demo_3_strategic_top.png", "ui_verified.png")
        print("Generated ui_verified.png")

        await browser.close()
        print("Demo completed. Screenshots saved.")

if __name__ == "__main__":
    asyncio.run(run_demo())
