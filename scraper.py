import cloudscraper
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_anandabazar_rashifal(url):
    # Create a scraper that perfectly mimics a real Windows Chrome browser
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    try:
        # Notice we use scraper.get() instead of requests.get()
        response = scraper.get(url)
        response.raise_for_status() 

        soup = BeautifulSoup(response.content, 'html.parser')

        content_div = soup.find('div', id='story_details')
        if not content_div:
            content_div = soup.find('div', class_='storybody') 

        if content_div:
            paragraphs = content_div.find_all('p')
            rashifal_text = " ".join([p.get_text(strip=True) for p in paragraphs])
            return rashifal_text
        else:
            return "Error: Could not find the text content on the page."

    except Exception as e:
        return f"Error: {e}"

# --- The Automation Loop ---
rashis = [
    "aries-horoscope-ajker-mesh", 
    "taurus-horoscope-ajker-brisha",
    "gemini-horoscope-ajker-mithun", 
    "cancer-horoscope-ajker-karkat",
    "leo-horoscope-ajker-singha", 
    "virgo-horoscope-ajker-kanya",
    "libra-horoscope-ajker-tula", 
    "scorpio-horoscope-ajker-brischik",
    "sagittarius-horoscope-ajker-dhanu", 
    "capricorn-horoscope-ajker-makar",
    "aquarius-horoscope-ajker-kumbha", 
    "pisces-horoscope-ajker-meen"
]

today_str = datetime.now().strftime("%d-%B-%Y").lower()
all_horoscopes = {}

for rashi in rashis:
    url = f"https://www.anandabazar.com/horoscope/todays-{rashi}-rashifal-in-bengali-{today_str}"
    print(f"Fetching: {url}")
    
    text = scrape_anandabazar_rashifal(url)
    short_name = rashi.split('-')[0] 
    all_horoscopes[short_name] = text

with open('horoscope.json', 'w', encoding='utf-8') as f:
    json.dump(all_horoscopes, f, ensure_ascii=False, indent=4)
    
print("Successfully saved all 12 horoscopes!")
