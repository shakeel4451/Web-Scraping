# ===============================
# IMPORT REQUIRED LIBRARIES
# ===============================

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from datetime import datetime


# ===============================
# PRICE CLEANING FUNCTION
# ===============================

def clean_zameen_price(price_str):
    """
    Converts price text like '3.5 Crore' or '75 Lakh' into PKR number
    """

    match = re.search(r"(\d+\.?\d*)", price_str)

    if not match:
        return 0

    value = float(match.group(1))

    if "Crore" in price_str:
        return int(value * 10000000)
    elif "Lakh" in price_str:
        return int(value * 100000)
    else:
        return int(value)


def is_good_deal(price_per_marla, area_avg):
    """
    Returns True if price is 20% below area average
    """
    return price_per_marla <= area_avg * 0.8

# ===============================
# MARLA EXTRACTION FUNCTION
# ===============================

def extract_marla(title_str):
    """
    Extracts plot size in Marla from listing title
    Example: '5 Marla Residential Plot' → 5.0
    """

    match = re.search(r"(\d+\.?\d*)\s*Marla", title_str, re.IGNORECASE)

    if match:
        return float(match.group(1))
    return None


# ===============================
# FAKE / OUTLIER LISTING FILTER
# ===============================

def is_valid_listing(price, marla):
    """
    Filters out unrealistic or fake listings
    """

    if price < 500000:          # Too cheap to be real
        return False

    if marla is None:           # Size not mentioned
        return False

    if price / marla < 100000:  # Unrealistic price per marla
        return False

    return True


# ===============================
# AREAS TO SCRAPE
# ===============================

AREAS = {
    "Johar Town": "https://www.zameen.com/Plots/Lahore_Johar_Town-93-1.html",
    "DHA": "https://www.zameen.com/Plots/Lahore_DHA_Defence-9-1.html",
    "Bahria Town": "https://www.zameen.com/Plots/Lahore_Bahria_Town-509-1.html"
}


# ===============================
# SCRAPER SETTINGS
# ===============================

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

results = []


# ===============================
# MAIN SCRAPING LOGIC
# ===============================

for area_name, base_url in AREAS.items():
    print(f"\nScraping area: {area_name}")

    for page in range(1, 6):   # Scrape first 5 pages
        url = base_url.replace("-1.html", f"-{page}.html")
        print(f"  Page {page}")

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                print("  Failed to load page")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            listings = soup.find_all("li", {"aria-label": "Listing"})

            for item in listings:
                price_el = item.find("span", {"aria-label": "Price"})
                title_el = item.find("h2")

                if not price_el or not title_el:
                    continue

                raw_price = price_el.text.strip()
                title = title_el.text.strip()

                price = clean_zameen_price(raw_price)
                marla = extract_marla(title)

                if not is_valid_listing(price, marla):
                    continue

                price_per_marla = int(price / marla)

                results.append({
                    "Area": area_name,
                    "Title": title,
                    "Marla": marla,
                    "Price_PKR": price,
                    "Price_Per_Marla": price_per_marla,
                    "Timestamp": datetime.now()
                })

            time.sleep(3)   # IMPORTANT: avoid getting banned

        except Exception as e:
            print("  Error:", e)


# ===============================
# SAVE DATA TO CSV
# ===============================

df = pd.DataFrame(results)
df.to_csv("lahore_market_final.csv", index=False)

print("\nScraping completed successfully!")
print(f"Total listings saved: {len(df)}")

# Calculate average price per marla for each area
area_averages = df.groupby("Area")["Price_Per_Marla"].mean().to_dict()

# Create a new column "Deal"
df["Deal"] = df.apply(
    lambda row: "YES" if is_good_deal(
        row["Price_Per_Marla"],
        area_averages[row["Area"]]
    ) else "NO",
    axis=1
)

df.to_csv("lahore_market_final_with_deals.csv", index=False)
print("Deal Finder applied! File saved as lahore_market_final_with_deals.csv")

deals_only = df[df["Deal"] == "YES"]
deals_only.to_csv("best_property_deals.csv", index=False)

print(f"Total deals found: {len(deals_only)}")


# ===============================
# VISUALIZATION (OPTIONAL)
# ===============================

import matplotlib.pyplot as plt

analysis = df.groupby("Area")["Price_Per_Marla"].mean().sort_values()

analysis.plot(kind="bar")
plt.title("Average Price Per Marla in Lahore")
plt.ylabel("Price in PKR")
plt.xlabel("Area")
plt.tight_layout()
plt.show()