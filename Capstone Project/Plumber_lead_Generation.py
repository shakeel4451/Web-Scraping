from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random

def scrape_yellow_pages():
    leads = []
    # Using a modern User-Agent
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    with sync_playwright() as p:
        # NOTICE: No 'proxy' dictionary here because we are using your Phone's data
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process"
            ]
        )

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=USER_AGENT,
            extra_http_headers={"Referer": "https://www.google.com/"}
        )

        page = context.new_page()

        # Stealth Script
        page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")

        try:
            print("🌍 Step 1: Visiting Google...")
            page.goto("https://www.google.com", timeout=60000)
            time.sleep(random.uniform(2, 4))

            print("🚀 Step 2: Navigating to Yellow Pages...")
            url = "https://www.yellowpages.com/search?search_terms=plumber&geo_location_terms=San+Francisco%2C+CA"
            
            # Use 'networkidle' to ensure everything (including scripts) is loaded
            page.goto(url, wait_until="networkidle", timeout=60000)
            #page.screenshot(path="hotspot_check.png")

            current_page=1
            max_pages=3

            while current_page <= max_pages:
              page.wait_for_selector(".result", timeout=10000)
              cards = page.locator(".result").all()

              if not cards:
                print("❌ No cards found on this page.Might be blocked or empty.")
                break
              
              for i, card in enumerate(cards):
                try:
                  name = card.locator(".business-name").first.inner_text(timeout=2000).strip()
                  phone_locator=card.locator(".phones").first
                  phone = phone_locator.inner_text(timeout=2000).strip() if phone_locator.is_visible() else "No Phone"
                  leads.append({"Business Name": name, "Phone Number": phone})
                  print(f"Harvested: {name}")
                  time.sleep(random.uniform(0.5, 1.5))
                except Exception as e:
                  continue

              next_button=page.locator("a.next")
              if current_page < max_pages and next_button.is_visible():
                 print("Clicking Next page....")
                 next_button.click()
                 time.sleep(random.uniform(3,5))
                 current_page+=1
              else:
                print("Reached Max pages or no Next button found.Ending scrape loop.")
                break
            if leads:
                df=pd.DataFrame(leads)
                df.to_excel("Plumbing_Leads_Multipage.xlsx", index=False)
                print(f"📊 Saved {len(leads)}  Total leads across {current_page} pages.")
            else:
               print("No data Harvested.")
        except Exception as e:
            print(f"❌ Error: {e}")

        browser.close()

scrape_yellow_pages()