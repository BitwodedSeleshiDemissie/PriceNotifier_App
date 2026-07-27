# PriceNotifier_App

Scrapes crypto / P2P EUR-USDT prices and pings me on WhatsApp when my conditions hit.

Selenium + BeautifulSoup for scraping, Twilio for the WhatsApp message. Runs as a hosted web app (Render/Heroku) so it doesn't need a local script left open. Has a `/` route so an uptime pinger can keep it awake. Checks every 60 min by default.

Setup:
```
git clone https://github.com/BitwodedSeleshiDemissie/PriceNotifier_App.git
cd PriceNotifier_App
pip install -r requirements.txt
```
