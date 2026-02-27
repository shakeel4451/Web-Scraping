import requests
from bs4 import BeautifulSoup



url="https://www.zameen.com/Houses_Property/Lahore_DHA_Defence-9-1.html"
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        'Accept-Language': 'en-US,en;q=0.9',
    }
response=requests.get(url,headers=headers,timeout=10)
soup=BeautifulSoup(response.text,'html.parser')
listings=soup.find_all("li",{"aria-label":"Listing"})
for item in listings:
  bed_el=item.find("span", {"aria-label": "Beds"})

  if bed_el:
    beds=bed_el.text.strip().split()[0]
  else:
    beds="0"  

  bath_el=item.find("span",{"aria-label":"Baths"})
  if bath_el:
    baths=bath_el.text.strip().split()[0]
  else:
    baths="0"
