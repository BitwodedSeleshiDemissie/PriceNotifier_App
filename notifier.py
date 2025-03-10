from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import config

def send_whatsapp_message(prices, converted_value, rr_value):
    try:
        client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
        
        message_body = (
            "Hello Lord Bit, I am here with my hourly update!\n\n"
            f"💱 980 EUR → {converted_value:.2f} USDT\n"
            f"📈 RR Value: {rr_value:.1f}\n\n"
            "🔝 Top 10 Prices:\n" +
            "\n".join([f"🏷️ Price {i+1}: {price} ETB" for i, price in enumerate(prices)])
        )

        message = client.messages.create(
            body=message_body,
            from_=config.TWILIO_PHONE_NUMBER,
            to=config.MY_WHATSAPP_NUMBER
        )
        print(f"✅ WhatsApp message sent! SID: {message.sid}")
        return True
        
    except TwilioRestException as e:
        print(f"🚨 Twilio Error: {e}")
        return False
    except Exception as e:
        print(f"🚨 General Error: {e}")
        return False