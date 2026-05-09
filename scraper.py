import cloudscraper
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_anandabazar_rashifal(url):
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    try:
        response = scraper.get(url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')

        # আনন্দবাজারের টেক্সট খোঁজা
        content_div = soup.find('div', id='story_details')
        if not content_div:
            content_div = soup.find('div', class_='storybody') 

        if content_div:
            paragraphs = content_div.find_all('p')
            rashifal_text = " ".join([p.get_text(strip=True) for p in paragraphs])
            return rashifal_text
        else:
            return "তথ্য পাওয়া যায়নি।"

    except Exception as e:
        return f"Error: {e}"

# ১২টি রাশির তালিকা
rashis = [
    "aries-horoscope-ajker-mesh", "taurus-horoscope-ajker-brisha",
    "gemini-horoscope-ajker-mithun", "cancer-horoscope-ajker-karkat",
    "leo-horoscope-ajker-singha", "virgo-horoscope-ajker-kanya",
    "libra-horoscope-ajker-tula", "scorpio-horoscope-ajker-brischik",
    "sagittarius-horoscope-ajker-dhanu", "capricorn-horoscope-ajker-makar",
    "aquarius-horoscope-ajker-kumbha", "pisces-horoscope-ajker-meen"
]

# আজকের তারিখ অনুযায়ী ডেটা সংগ্রহ
today_str = datetime.now().strftime("%d-%B-%Y").lower()
all_horoscopes = {}

for rashi in rashis:
    url = f"https://www.anandabazar.com/horoscope/todays-{rashi}-rashifal-in-bengali-{today_str}"
    text = scrape_anandabazar_rashifal(url)
    short_name = rashi.split('-')[0] 
    all_horoscopes[short_name] = text

# JSON ফাইল সেভ করা
with open('horoscope.json', 'w', encoding='utf-8') as f:
    json.dump(all_horoscopes, f, ensure_ascii=False, indent=4)
