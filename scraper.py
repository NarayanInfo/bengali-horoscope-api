import requests
from bs4 import BeautifulSoup
import json

def scrape_horoscope():
    url = "https://bangla.hindustantimes.com/astrology/horoscope" # Example source
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Logic to find the Bengali text for each Rashi
    # This part depends on the specific website's HTML structure
    data = {
        "date": "2026-05-09",
        "aries": "আজকের দিনটি...",
        "taurus": "আপনার আর্থিক দিক..."
    }

    with open('horoscope.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

scrape_horoscope()
