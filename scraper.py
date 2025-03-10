from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_top_5_prices():
    # Set up Selenium with Chrome options to run headless (without opening a browser window)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headlessly
    driver = webdriver.Chrome(options=chrome_options)

    url = "https://p2p.binance.com/en/trade/sell/USDT?fiat=ETB&payment=all-payments"
    driver.get(url)
    
    # Wait for the page to load completely (adjust the sleep time if necessary)
    time.sleep(5)  # Sleep for 5 seconds to wait for JS to load the content

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Find the price elements
    price_tags = soup.find_all("div", class_="headline5 mr-4xs text-primaryText")
    prices = [tag.text.strip() for tag in price_tags[:5]]

    driver.quit()  # Close the browser

    return prices if prices else None
