import random
from playwright.sync_api import sync_playwright

# DataHarvest PK - Proxy List
PROXIES = [
    "http://144.217.101.245:3128",
    "http://167.71.200.10:8080",
    "http://64.225.4.81:9999"
]

def get_data_with_proxy():
    # LOGIC: Pick a random proxy from the list
    selected_proxy = random.choice(PROXIES)
    print(f"📡 Attempting connection via: {selected_proxy}")

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(
                headless=False, 
                proxy={"server": selected_proxy}
            )
            page = browser.new_page()
            
            # Set a short timeout so we don't wait forever for a dead proxy
            page.goto("https://httpbin.org/ip", timeout=5000) 
            print("✅ Success! IP changed.")
            browser.close()
            
        except Exception as e:
            print(f"❌ Connection failed: {selected_proxy} is likely down.")

# Run the test
get_data_with_proxy()