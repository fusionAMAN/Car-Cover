import requests
from bs4 import BeautifulSoup
import csv

# URL for car cover search results on OLX
BASE_URL = "https://www.olx.in/items/q-car-cover"

# Set headers to mimic a browser visit
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def get_olx_listings(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    listings = []

    # Parsing product blocks
    for item in soup.find_all("li", class_="EIR5N"):
        title_tag = item.find("span", class_="_2tW1I")
        price_tag = item.find("span", class_="_89yzn")
        location_tag = item.find("span", class_="_2Vp0i")

        title = title_tag.text if title_tag else "No Title"
        price = price_tag.text if price_tag else "No Price"
        location = location_tag.text if location_tag else "No Location"

        listings.append({
            "Title": title,
            "Price": price,
            "Location": location
        })

    return listings

def save_to_csv(data, filename="olx_car_covers.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Price", "Location"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    print("Fetching OLX car cover listings...")
    results = get_olx_listings(BASE_URL)
    save_to_csv(results)
    print(f"Saved {len(results)} listings to 'olx_car_covers.csv'")
