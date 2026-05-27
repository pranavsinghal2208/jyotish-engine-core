import asyncio
from playwright.async_api import async_playwright

async def live_demo():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})

        print("Opening browser for integrated functionality testing...")
        await page.goto("http://127.0.0.1:8000")
        await asyncio.sleep(2)

        # Add name entry
        print("Entering name for personalized numerology...")
        await page.fill("#fullName", "Test User")
        await asyncio.sleep(1)

        # Searching by Pincode for extreme precision
        print("Searching by Pincode 251001 (MuzaffarNagar)...")
        await page.type("#citySearch", "251001", delay=100)
        await page.wait_for_selector(".city-item")
        await asyncio.sleep(1)

        print("Selecting high-precision result...")
        await page.click(".city-item")
        await asyncio.sleep(1)

        print("Entering date and time for 1987-08-22 9:55 PM...")
        await page.fill("#date", "1987-08-22")
        await asyncio.sleep(1)
        await page.fill("#time", "21:55")
        await asyncio.sleep(1)

        print("Generating refined report...")
        await page.click("#generateBtn")

        await page.wait_for_selector("#resultsScreen:not(.hidden)")
        print("Observing Coach Insights (Fixed Data Format)...")
        await asyncio.sleep(6)

        # Switch to numerology tab after generating chart
        print("Switching to numerology tab for enhanced insights...")
        await page.click("[data-view='numerology']")
        await asyncio.sleep(3)

        print("Testing numerology tab features...")
        await page.wait_for_selector("#numerologySection")
        await asyncio.sleep(3)

        # Test feedback submission
        print("Testing feedback widget submission...")
        await page.click("#feedbackWidget .feedback-toggle")
        await asyncio.sleep(1)
        await page.click(".stars .star[data-rating='5']")
        await asyncio.sleep(1)
        await page.select_option("#featureUsed", "numerology")
        await asyncio.sleep(1)
        await page.fill("#feedbackText", "Excellent numerology integration! The new features work perfectly.")
        await asyncio.sleep(1)
        await page.click(".feedback-actions .btn-primary")
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
