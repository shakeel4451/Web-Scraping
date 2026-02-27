from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 1. Go to the practice login page
        page.goto("https://practicetestautomation.com/practice-test-login/")
        
        # 2. Fill in the details (Correct: student / Password123)
        print("Typing credentials...")
        page.fill("#username", "student")
        page.fill("#password", "Password123")
        page.click("#submit")
        
        # 3. BRANCHING LOGIC: Check what happened
        # We wait up to 5 seconds for the URL to change or an element to appear
        page.wait_for_load_state("networkidle")
        
        if page.is_visible("text=Logged In Successfully"):
            print("✅ LOGIN SUCCESS: Data harvesting can begin!")
            # Here you would start your scraping logic
        elif page.is_visible("#error"):
            error_text = page.inner_text("#error")
            print(f"❌ LOGIN FAILED: {error_text}")
        
        browser.close()

run()