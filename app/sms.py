import requests
from app.config import settings

TERMII_API_KEY = settings.termii_api_key
TERMII_SENDER_ID = settings.termii_sender_id  
TERMII_SMS_URL = settings.termii_sms_url

def send_sms_termii(to_phone, message):
    url = TERMII_SMS_URL
    payload = {
        "api_key": TERMII_API_KEY,
        "to": [to_phone],
        "from": TERMII_SENDER_ID,
        "sms": message,
        "type": "plain",
        "channel": "generic"
    }
    response = requests.post(url, json=payload)
    print(response.json())
