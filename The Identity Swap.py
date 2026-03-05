from playwright.sync_api import sync_playwright

def run_stealth():
    # A real User-Agent from a MacBook Pro
    REAL_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # We set the User-Agent in the 'context' (The browser's memory)
        context = browser.new_context(user_agent=REAL_USER_AGENT)
        page = context.new_page()
        
        page.goto("https://httpbin.org/user-agent")
        print("🕵️ Browser is now disguised as a MacBook!")
        print(page.inner_text("body"))
        
        browser.close()

run_stealth()