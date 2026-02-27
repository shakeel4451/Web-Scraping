import requests
import json
import pandas as pd

def scrape_daraz_keyboards():
    # 1. THE HIDDEN LINK: Notice 'ajax=true'. This tells Daraz to send DATA, not a PAGE.
    search_query = "mechanical+keyboard"
    url = f"https://www.daraz.pk/catalog/?ajax=true&q={search_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.daraz.pk/"
    }

    print(f"Requesting data for: {search_query}...")
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # 2. THE TRANSFORMATION: Parse JSON into a Python Dictionary
            full_data = response.json()
            
            # Daraz stores products inside: mods -> listItems
            items = full_data.get('mods', {}).get('listItems', [])
            
            print(f"Found {len(items)} items through the API shortcut.\n")
            
            scraped_data = []
            for item in items:
                # No BeautifulSoup needed! Just key-value pairs.
                info = {
                    "Name": item.get('name'),
                    "Price": item.get('price'),
                    "Brand": item.get('brandName'),
                    "Rating": item.get('ratingScore'),
                    "Reviews": item.get('review'),
                    "Seller": item.get('sellerName')
                }
                scraped_data.append(info)
                print(f"Item: {info['Name'][:40]}... | Rs. {info['Price']}")

            # 3. STORAGE: Save to CSV
            df = pd.DataFrame(scraped_data)
            df.to_csv("daraz_keyboards.csv", index=False)
            print("\nSuccess! Check 'daraz_keyboards.csv'")
            
        else:
            print(f"Request failed. Status: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_daraz_keyboards()