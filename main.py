import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

# Function to get the top 5 prices from Binance P2P page
def get_top_5_prices():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    url = "https://p2p.binance.com/en/trade/sell/USDT?fiat=ETB&payment=all-payments"
    driver.get(url)
    
    # Wait for the price elements to appear on the page (max 10 seconds)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "headline5")))
    except:
        print("⚠️ Timeout waiting for prices to load.")
        driver.quit()
        return None

    # Get the page source and parse it
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the price elements
    price_tags = soup.find_all("div", class_="headline5 mr-4xs text-primaryText")
    prices = [tag.text.strip() for tag in price_tags[:5]]

    driver.quit()

    return prices if prices else None

# Function to get the EUR to USDT conversion rate from Binance Ticker Price API
def get_eur_to_usdt_conversion_rate():
    url = "https://api.binance.com/api/v3/ticker/price"
    
    # Parameters for EUR/USDT pair
    params = {
        'symbol': 'EURUSDT'  # EUR/USDT trading pair
    }

    try:
        # Send the request to the Binance API
        response = requests.get(url, params=params)
        
        # Check if the response is successful
        if response.status_code == 200:
            try:
                # Parse the JSON response
                data = response.json()
                
                # Extract the price (conversion rate)
                if 'price' in data:
                    conversion_rate = float(data['price'])
                    return conversion_rate
                else:
                    print("⚠️ Could not fetch the conversion rate!")
                    return None
            except ValueError:
                print("⚠️ Failed to decode JSON response!")
                print("Response Content:", response.text)
                return None
        else:
            print(f"⚠️ Error fetching data: HTTP Status Code {response.status_code}")
            print("Response Content:", response.text)
            return None

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Request failed: {e}")
        return None

# Main function to perform the price update job
def job():
    # Get the top 5 prices
    prices = get_top_5_prices()
    if prices:
        print("📢 Latest Top 5 Prices:")
        for idx, price in enumerate(prices, start=1):
            print(f"Price {idx}: {price} ETB")

        # Get the EUR to USDT conversion rate
        conversion_rate = get_eur_to_usdt_conversion_rate()
        if conversion_rate:
            print(f"Conversion Rate (EUR to USDT): {conversion_rate}")
            
            # Convert 980 EUR to USDT using the conversion rate
            eur_amount = 980
            converted_value = eur_amount * conversion_rate
            print(f"\n980 EUR ->: {converted_value:.2f} USDT")
            
            # Get the second top price (second-highest)
            second_top_price = float(prices[1].replace(",", ""))

            # Calculate RR (second highest price in the formula)
            RR = (converted_value * second_top_price) / 1000
            print(f"\nRR = ({converted_value:.1f} * {second_top_price}) / 1000 = {RR:.1f}")
        else:
            print("⚠️ Could not fetch conversion rate.")
    else:
        print("⚠️ Could not fetch prices!")

# Function to check if the current time is within the restricted sleep period (22:00 to 07:00)
def is_sleep_time():
    current_time = datetime.datetime.now().time()
    # Check if the time is between 22:00 and 07:00
    sleep_start = datetime.time(22, 0)  # 22:00
    sleep_end = datetime.time(7, 0)  # 07:00

    if sleep_start <= current_time or current_time <= sleep_end:
        return True
    return False

# Function to run the job every 1 hour, checking if it's sleep time
def run_every_hour():
    while True:
        if not is_sleep_time():
            job()  # Call the job function
        else:
            print(f"⏰ It's sleep time, skipping this hour. Current time: {datetime.datetime.now().strftime('%H:%M')}")

        print("\nWaiting for the next hour...\n")
        time.sleep(3600)  # Sleep for 1 hour (3600 seconds)

# Run the job every hour
run_every_hour()
