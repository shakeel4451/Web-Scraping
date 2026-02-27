from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://quotes.toscrape.com/scroll") # A perfect site for scroll practice
        
        last_height = page.evaluate("document.body.scrollHeight")
        
        while True:
            print("📜 Scrolling down...")
            # Scroll to the bottom
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            
            # Wait for new content to load
            time.sleep(2) 
            
            # Calculate new scroll height and compare with last scroll height
            new_height = page.evaluate("document.body.scrollHeight")
            
            if new_height == last_height:
                print("🏁 Reached the end of the page!")
                break
                
            last_height = new_height

        # Now grab all the items that appeared
        quotes = page.locator(".quote").all_inner_texts()
        print(f"✅ Harvested {len(quotes)} quotes total!")
        
        browser.close()

run()