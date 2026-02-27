from playwright.sync_api import sync_playwright
import time

def run():
  with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    page=browser.new_page()
    print("Opening the website...")
    page.goto("http://books.toscrape.com/",wait_until="networkidle")

    title=page.title()
    print(f"Title of the page is : {title}")

    page.mouse.wheel(0,500)
    print("Scrolling down...500 pixels")

    time.sleep(3)
    browser.close()
    print("Browser closed.")

if __name__=="__main__":
  run()