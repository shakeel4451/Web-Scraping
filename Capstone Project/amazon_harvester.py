from playwright.sync_api import sync_playwright
import time
import pandas as pd

def run_amazon_optimized(search_query):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    all_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=USER_AGENT)
        page = context.new_page()

        # Manual Stealth
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print(f"🕵️ Infiltrating Amazon UK for: {search_query}")
        url = f"https://www.amazon.co.uk/s?k={search_query.replace(' ', '+')}"
        page.goto(url, wait_until="networkidle")

        # 1. NEW LOGIC: Click the "Accept" button from your screenshot
        try:
            # Using the 'Accept' text from your image banner
            if page.is_visible("text='Accept'"):
                page.click("text='Accept'")
                print("🍪 Cookie banner cleared!")
                time.sleep(2)
        except:
            pass

        # 2. HARVESTING: Based on your screenshot
        # The product cards are visible in the background
        items = page.locator("[data-component-type='s-search-result']").all()
        print(f"🔍 Found {len(items)} items on screen.")

        for item in items[:10]:
            try:
                title = item.locator("h2").inner_text()
                
                # Logic: In your image, prices are shown as 'PKR 128,318.61'
                # Let's look for the 'a-price' container which is more reliable
                price = item.locator(".a-price").first.inner_text()
                
                # Split and clean the price (Removing 'PKR' or newlines)
                clean_price = price.replace('\n', ' ').strip()
                
                all_data.append({
                    "Product Name": title.strip(),
                    "Price": clean_price
                })
                print(f"✅ Grabbed: {title[:30]}... | {clean_price}")
            except:
                continue

        # 3. SAVE
        if all_data:
            pd.DataFrame(all_data).to_excel("Amazon_PK_Results.xlsx", index=False)
            print(f"📊 Success! Saved to Excel.")
        else:
            print("❌ Still no data. The elements might be loading too slowly.")

        browser.close()

run_amazon_optimized("laptop")