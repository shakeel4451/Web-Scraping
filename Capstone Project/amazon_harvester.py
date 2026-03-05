from playwright.sync_api import sync_playwright
import time
import random

def run_amazon_scraper(laptop):
    # DataHarvest PK Stealth Config
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    with sync_playwright() as p:
        # Launch headed so you can see if a CAPTCHA appears
        browser = p.chromium.launch(headless=False)
        
        # LOGIC: Create a context with a real screen size and User-Agent
        context = browser.new_context(
            user_agent=USER_AGENT,
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()

        print(f"🔍 Searching Amazon UK for: {laptop}")
        page.goto("https://www.amazon.co.uk", wait_until="domcontentloaded")
        
        # GUARD: Handle the "Accept Cookies" popup if it appears
        try:
            if page.is_visible("#sp-cc-accept"):
                page.click("#sp-cc-accept")
                print("🍪 Cookies accepted.")
        except:
            pass

        # ACTION: Search for the item
        page.fill("#twotabsearchtextbox", laptop)
        time.sleep(random.uniform(1, 2)) # Human-like pause
        page.keyboard.press("Enter")
        
        # WAIT: For results to load
        page.wait_for_selector(".s-result-item")
        print("✅ Results loaded!")

        # HARVEST: Get titles and prices of the first 5 items
        items = page.locator(".s-result-item[data-component-type='s-search-result']").all()
        
        for i, item in enumerate(items[:5]):
            title = item.locator("h2").inner_text()
            # LOGIC: Some items don't have prices (out of stock)
            try:
                price = item.locator(".a-price-whole").inner_text()
                print(f"{i+1}. {title} - £{price}")
            except:
                print(f"{i+1}. {title} - (Price not found/Out of Stock)")

        browser.close()

run_amazon_scraper("laptop")