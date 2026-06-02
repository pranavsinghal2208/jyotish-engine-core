import asyncio
import json
import re
from playwright.async_api import async_playwright

async def live_demo():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})

        # Capture browser logs for diagnostic clarity
        page.on("console", lambda msg: print(f"    [Browser Console]: {msg.text}"))
        page.on("pageerror", lambda err: print(f"    [Browser JS Error]: {err}"))

        # Intercept and mock Nominatim API requests for offline stability
        async def mock_nominatim(route):
            print(f"    [Mocking Nominatim Request]: {route.request.url}")
            mock_response = [
                {
                    "place_id": 12345,
                    "lat": "29.4727",
                    "lon": "77.7085",
                    "display_name": "Muzaffarnagar, Uttar Pradesh, India",
                    "class": "boundary",
                    "type": "administrative",
                    "addresstype": "city",
                    "address": {
                        "city": "Muzaffarnagar",
                        "state": "Uttar Pradesh",
                        "country": "India",
                        "country_code": "in"
                    }
                }
            ]
            await route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(mock_response)
            )
        await page.route(re.compile(r"nominatim\.openstreetmap\.org/search"), mock_nominatim)

        print("Opening browser for integrated functionality testing...")
        await page.goto("http://127.0.0.1:5004")
        await asyncio.sleep(2)

        # Clear local storage or click editDetailsBtn to ensure a clean starting point
        try:
            if await page.locator("#editDetailsBtn").is_visible():
                print("    [Returning User Profile Detected] - Resetting to landing screen...")
                await page.click("#editDetailsBtn")
                await asyncio.sleep(1.5)
        except Exception as e:
            print(f"    [Profile reset check info]: {e}")

        # Add name entry
        print("Entering name for personalized numerology...")
        await page.fill("#fullName", "Test User")
        await asyncio.sleep(1)

        print("Entering date for 1987-08-22 (Triggers progressive reveal)...")
        # Populate DD/MM/YYYY inputs and hidden date field, then invoke quickUnlock
        await page.evaluate("""
            document.getElementById('dobDD').value = '22';
            document.getElementById('dobMM').value = '08';
            document.getElementById('dobYYYY').value = '1987';
            document.getElementById('date').value = '1987-08-22';
        """)
        # Trigger quickUnlock to reveal the rest of the form
        try:
            await page.evaluate("quickUnlock();")
        except Exception:
            pass
        await asyncio.sleep(1.5)

        # Searching by Pincode for extreme precision
        print("Searching by Pincode 251001 (MuzaffarNagar)...")
        await page.fill("#citySearch", "")
        await page.type("#citySearch", "251001", delay=100)
        await page.wait_for_selector(".city-item")
        await asyncio.sleep(1)

        print("Selecting high-precision result...")
        await page.click(".city-item")
        await asyncio.sleep(1)

        print("Entering time for 9:55 PM...")
        await page.evaluate("document.getElementById('time').value = '21:55';")
        await asyncio.sleep(1)

        print("Generating refined report...")
        await page.click("#generateBtn")

        # Dismiss consent modal if it appears
        try:
            await page.wait_for_selector(".consent-agree", timeout=3000)
            print("    [Consent Modal Detected] - Dismissing...")
            await page.click(".consent-agree")
        except Exception:
            pass

        await page.wait_for_selector("#resultsScreen:not(.hidden)")
        print("Observing Coach Insights (Fixed Data Format)...")
        await asyncio.sleep(6)

        # Switch to numerology tab after generating chart
        print("Switching to numerology tab for enhanced insights...")
        await page.click("[data-view='numerology']")
        await asyncio.sleep(3)

        print("Testing numerology tab features...")
        await page.wait_for_selector("#numerologyView")
        await asyncio.sleep(3)

        # Test feedback submission
        print("Testing feedback widget submission...")
        await page.evaluate("document.querySelector('#feedbackWidget .feedback-toggle').click()")
        await asyncio.sleep(1)
        await page.evaluate("document.querySelector('.stars .star[data-rating=\"5\"]').click()")
        await asyncio.sleep(1)
        await page.select_option("#featureUsed", "numerology")
        await asyncio.sleep(1)
        await page.fill("#feedbackText", "Excellent numerology integration! The new features work perfectly.")
        await asyncio.sleep(1)
        await page.evaluate("document.querySelector('.feedback-actions .btn-primary').click()")
        await asyncio.sleep(3)

        print("Feedback submitted successfully. Testing complete.")
        await browser.close()

async def run_multiple_demos(num_runs=3):
    for i in range(num_runs):
        print(f"\n--- Starting Demo Run {i+1} ---")
        await live_demo()
        print(f"--- Demo Run {i+1} Complete ---\n")
        await asyncio.sleep(2)  # Brief pause between runs

if __name__ == "__main__":
    asyncio.run(run_multiple_demos())
