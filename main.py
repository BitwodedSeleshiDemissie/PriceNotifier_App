import schedule
import time
from scraper import get_top_5_prices
from notifier import send_whatsapp_message


def job():
    prices = get_top_5_prices()
    if prices:
        send_whatsapp_message(prices)
    else:
        print("⚠️ Could not fetch prices!")

schedule.every(1).hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
