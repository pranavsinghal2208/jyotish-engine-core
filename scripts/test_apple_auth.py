import asyncio
from playwright.async_api import async_playwright
import sys

async def run_test():
    async with async_playwright() as p:
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

        print("1. Opening Cosmic OS...")
        await page.goto("http://127.0.0.1:8000")
        await page.wait_for_load_state("networkidle")
        
        # Pre-set consent to bypass the consent modal
        await page.evaluate("localStorage.setItem('cosmicOsConsent', '1')")
        
        print("2. Entering details to generate chart...")
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
        
        # Force set hidden input values just in case events didn't trigger in headless mode
        await page.evaluate("""() => {
            document.getElementById('date').value = '1987-08-22';
            document.getElementById('time').value = '09:55';
        }""")
        
        await asyncio.sleep(1) # Wait for morph animation
        
        print("5. Generating Chart to access header...")
        await page.click("#generateBtn")
        
        # Wait for transition to results screen
        await page.wait_for_selector("#resultsScreen:not(.hidden)", timeout=30000)
        
        # Verify Apple Sign In button is present in the header
        print("6. Checking Apple Sign In button...")
        apple_btn = await page.wait_for_selector("#headerAppleLink", timeout=5000)
        assert apple_btn is not None, "Apple Sign In button not found!"
        print("   Apple Sign In button found.")
        
        # Click the Apple Sign In button
        print("7. Clicking Apple Sign In button...")
        await page.click("#headerAppleLink")
        
        # Wait for page redirect/reload to complete
        print("8. Waiting for redirect back to Cosmic OS...")
        await page.wait_for_load_state("networkidle")
        
        # Verify user is logged in by querying /api/auth/status
        print("9. Checking authentication status via API...")
        auth_data = await page.evaluate("async () => { const res = await fetch('/api/auth/status'); return await res.json(); }")
        print(f"   Auth Status Data: {auth_data}")
        
        assert auth_data.get("authenticated") is True, f"User is not authenticated: {auth_data}"
        assert auth_data.get("email") == "apple_pranav@psbc.com", f"Incorrect authenticated email: {auth_data}"
        
        print("\n✅ E2E TEST PASSED: Apple Login OAuth completed successfully!")
        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(run_test())
    except Exception as e:
        print(f"\n❌ E2E TEST FAILED: {e}", file=sys.stderr)
        sys.exit(1)
