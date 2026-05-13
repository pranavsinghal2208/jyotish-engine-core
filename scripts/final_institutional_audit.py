import asyncio
from playwright.async_api import async_playwright
import os

async def run_demo():
    async with async_playwright() as p:
        # We must use headless=True in this environment
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        
        print("1. Opening Cosmic OS...")
        await page.goto("http://127.0.0.1:8000")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path="demo_1_landing.png")
        
        print("2. Entering Details: Pranav, Muzaffarnagar...")
        await page.fill("#fullName", "Pranav")
        
        # City search logic
        await page.type("#citySearch", "Muzaffarnagar")
        await page.wait_for_selector(".city-item")
        await page.click(".city-item")
        
        # Date and Time
        await page.fill("#date", "1987-08-22")
        await page.fill("#time", "09:55")
        
        await asyncio.sleep(1) # Wait for morph animation
        await page.screenshot(path="demo_2_input_ready.png")
        
        print("3. Generating Chart...")
        await page.click("#generateBtn")
        
        # Wait for transition
        await page.wait_for_selector("#resultsScreen:not(.hidden)", timeout=10000)
        await asyncio.sleep(2) # Finish fade-in
        
        print("4. Strategic View (Page 1)...")
        await page.screenshot(path="demo_3_strategic_top.png")
        
        # Scroll Strategic
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1)
        await page.screenshot(path="demo_4_strategic_bottom.png")
        
        print("5. Technical View (Page 2)...")
        await page.click('button[data-view="technical"]')
        await asyncio.sleep(1)
        await page.screenshot(path="demo_5_technical_top.png")
        
        # Scroll Technical
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1)
        await page.screenshot(path="demo_6_technical_bottom.png")
        
        print("6. Repeating sequence for verification...")
        await page.click('button[data-view="strategic"]')
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(1)
        await page.screenshot(path="demo_7_repeat_top.png")
        
        await browser.close()
        print("Demo completed. Screenshots saved.")

if __name__ == "__main__":
    asyncio.run(run_demo())
