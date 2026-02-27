import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def clean_zameen_price(price_str):
    # Search for the number (handles decimals like 3.85)
    number_match = re.search(r"(\d+\.?\d*)", price_str)
    if not number_match:
        return 0
    
    value = float(number_match.group(1))
    
    # Logic to convert the units to PKR
    if "Crore" in price_str:
        return int(value * 10000000)
    elif "Lakh" in price_str:
        return int(value * 100000)
    else:
        return int(value)

def extract_marla(title_str):
    # Concept: Extracting the plot size from the title string
    # "5 Marla Residential Plot" -> 5.0
    match = re.search(r"(\d+\.?\d*)\s*Marla", title_str, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None

def scrape_lahore_homes():
    # URL updated for Johar Town Plots
    url = "https://www.zameen.com/Plots/Lahore_Johar_Town-93-1.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    print(f"Connecting to Zameen (Johar Town Plots)...")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Blocked! Status code: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all("li", {"aria-label": "Listing"})
        print(f"Found {len(listings)} plots on this page.\n")

        results = []

        for item in listings:
            price_element = item.find("span", {"aria-label": "Price"})
            location_element = item.find("div", {"aria-label": "Location"})
            title_element = item.find("h2")

            if price_element and location_element:
                raw_price = price_element.text.strip()
                raw_title = title_element.text.strip() if title_element else "N/A"
                
                # --- APPLYING THE CLEANING FUNCTIONS ---
                numeric_price = clean_zameen_price(raw_price)
                marla_size = extract_marla(raw_title)
                
                # Calculate Price per Marla (Advanced Concept: Derived Data)
                price_per_marla = None
                if numeric_price and marla_size:
                    price_per_marla = int(numeric_price / marla_size)

                data = {
                    "Title": raw_title,
                    "Marla": marla_size,
                    "Price_Raw": raw_price,
                    "Price_PKR": numeric_price,
                    "Price_Per_Marla": price_per_marla,
                    "Location": location_element.text.strip()
                }
                results.append(data)
                print(f"Saved: {raw_price} | Size: {marla_size} Marla")

        # Save to CSV
        df = pd.DataFrame(results)
        df.to_csv("johar_town_plots.csv", index=False)
        print(f"\nSuccess! {len(results)} rows saved to 'johar_town_plots.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_lahore_homes()