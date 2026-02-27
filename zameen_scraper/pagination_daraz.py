import requests
import pandas as pd
import time

def scrape_daraz_multi_page(query, total_pages=3):
    all_items = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.daraz.pk/"
    }

    for page in range(1, total_pages + 1):
        # The 'page' variable automatically updates the URL
        url = f"https://www.daraz.pk/catalog/?ajax=true&q={query}&page={page}"
        print(f"Scraping Page {page}...")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('mods', {}).get('listItems', [])
            
            for item in items:
                all_items.append({
                    "Name": item.get('name'),
                    "Price": item.get('price'),
                    "Brand": item.get('brandName'),
                    "Page": page # Good practice to track which page the data came from
                })
            
            # Be polite! Wait 2 seconds between pages to avoid being flagged.
            time.sleep(2) 
        else:
            print(f"Failed to fetch page {page}")
            break

    # Save all results to one file
    df = pd.DataFrame(all_items)
    df.to_csv(f"daraz_{query}_multipage.csv", index=False)
    print(f"\nDone! Scraped {len(all_items)} items across {total_pages} pages.")

if __name__ == "__main__":
    scrape_daraz_multi_page("mechanical+keyboard", total_pages=3)