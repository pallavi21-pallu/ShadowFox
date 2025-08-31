import requests
from bs4 import BeautifulSoup
import csv

url = "https://shadowfox.in/"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Scrape Headings
    headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]

    # Scrape Paragraphs
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]

    # Scrape Links
    links = [a["href"] for a in soup.find_all("a", href=True)]

    # Scrape Images
    images = [img["src"] for img in soup.find_all("img", src=True)]

    # Save everything in CSV
    with open("shadowfox_large_scrape.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Type", "Content"])

        for h in headings:
            writer.writerow(["Heading", h])

        for p in paragraphs:
            writer.writerow(["Paragraph", p])

        for l in links:
            writer.writerow(["Link", l])

        for img in images:
            writer.writerow(["Image", img])

    print("✅ Large scraping completed! Data saved in shadowfox_large_scrape.csv")

except requests.exceptions.RequestException as e:
    print("⚠️ Error while scraping:", e)
