from twilio.rest import Client
import config

def send_whatsapp_message(prices):
    client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

    message_body = "📢 Latest Top 5 Prices:\n" + "\n".join([f"Price {i+1}: {price} ETB" for i, price in enumerate(prices)])

    message = client.messages.create(
        body=message_body,
        from_=config.TWILIO_PHONE_NUMBER,
        to=config.MY_WHATSAPP_NUMBER
    )

    print(f"✅ Message sent! SID: {message.sid}")
