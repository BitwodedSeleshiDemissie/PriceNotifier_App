import requests
from bs4 import BeautifulSoup

def get_top_5_prices():
    url = "https://p2p.binance.com/en/trade/sell/USDT?fiat=ETB&payment=all-payments"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find price elements (adjust if needed)
    price_tags = soup.find_all("span", {"class": "css-1m1f8hn"})  
    prices = [tag.text.strip() for tag in price_tags[:5]]

    return prices if prices else None
