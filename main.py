import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import pytz
import os
from threading import Thread
from flask import Flask
from notifier import send_whatsapp_message
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, MY_WHATSAPP_NUMBER

# Initialize Flask app
app = Flask(__name__)

def get_top_10_prices():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    url = "https://p2p.binance.com/en/trade/sell/USDT?fiat=ETB&payment=all-payments"
    driver.get(url)
    
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "headline5"))
        )
    except:
        print("⚠️ Timeout waiting for prices to load.")
        driver.quit()
        return None

    soup = BeautifulSoup(driver.page_source, "html.parser")
    price_tags = soup.find_all("div", class_="headline5 mr-4xs text-primaryText")
    prices = [tag.text.strip() for tag in price_tags[:10]]
    driver.quit()

    return prices if prices else None

def get_eur_to_usdt_conversion_rate():
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {'symbol': 'EURUSDT'}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return float(data['price']) if 'price' in data else None
        print(f"⚠️ API Error: {response.status_code}")
        return None
    except Exception as e:
        print(f"⚠️ Conversion rate error: {e}")
        return None

def job():
    prices = get_top_10_prices()
    if prices and len(prices) >= 10:
        print("📢 Latest Top 10 Prices:")
        for idx, price in enumerate(prices, start=1):
            print(f"Price {idx}: {price} ETB")

        conversion_rate = get_eur_to_usdt_conversion_rate()
        if conversion_rate:
            converted_value = 980 * conversion_rate
            second_top_price = float(prices[3].replace(",", ""))
            rr_value = (converted_value * second_top_price) / 1000

            print(f"\n💱 980 EUR → {converted_value:.2f} USDT")
            print(f"📈 RR Value: {rr_value:.1f}")

            try:
                send_whatsapp_message(prices, converted_value, rr_value)
            except Exception as e:
                print(f"⚠️ Notification failed: {e}")
        else:
            print("⚠️ Could not fetch conversion rate.")
    else:
        print("⚠️ Could not fetch prices or insufficient prices!")

def is_sleep_time():
    italian_tz = pytz.timezone("Europe/Rome")
    current_time = datetime.datetime.now(italian_tz).time()
    return current_time >= datetime.time(0, 0) and current_time <= datetime.time(7, 0)

def run_scheduler():
    while True:
        if not is_sleep_time():
            print("\n🕒 Running hourly update...")
            job()
        else:
            current_time = datetime.datetime.now().strftime('%H:%M')
            print(f"⏰ Sleep time ({current_time}), skipping update.")
        
        print("\n⏳ Waiting for next hour...\n")
        time.sleep(3600)

@app.route('/')
def home():
    return "P2P Price Monitor is running", 200

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == "__main__":
    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))