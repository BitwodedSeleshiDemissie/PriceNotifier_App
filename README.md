# PriceNotifier_App

This app scrapes **crypto and P2P EUR–USDT prices** and notifies you on WhatsApp when prices meet your set conditions.  
It’s designed as a hosted web app (e.g. Render, Heroku) so it can run continuously without needing to keep a local script active.

---

## Features

- Scrapes market data using **Selenium + BeautifulSoup**  
- Runs automatically at safe intervals (default: every 60 minutes)  
- Sends WhatsApp alerts via **Twilio API**  
- Hosted as a web app with a `/` route so external uptime services can ping it to keep it awake  

---

## Installation

```bash
# Clone the repo
git clone https://github.com/BitwodedSeleshiDemissie/PriceNotifier_App.git
cd PriceNotifier_App

# Install dependencies
pip install -r requirements.txt
