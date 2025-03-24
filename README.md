### Price Updater App

Tired of constantly checking the market values for cryptocurrencies and EUR/USDT exchange rates for my part-time forex job, I decided to automate the process.

Since Binance doesn't provide an API for their P2P platform, I created a web scraping solution using BeautifulSoup and Selenium to extract the data I need.

I made sure the scraping follows ethical guidelines by limiting it to once every 60 minutes to avoid overloading the system.

To receive updates seamlessly, I integrated the free WhatsApp messaging API, Twilio, since I use WhatsApp daily to communicate with my family and friends(This way I stay informed even without planning to!).

Instead of paying an extra $7 per month to host it as a background service on Render (which only offers a free version with limited features for web applications), I wrapped the app in a web application format.

Since websites on Render go to sleep if not used, I utilized an external service that pings my website periodically to keep it awake and running.

Enjoy :)
