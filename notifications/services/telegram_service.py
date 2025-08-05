import requests
from config.settings import TELEGRAM_BOT_TOKEN


def send_telegram(recipient, message):
    if not recipient.telegram_id:
        return False, "No telegram ID"

    chat_id = recipient.telegram_id
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            return True, None
        else:
            return False, f"Telegram API error: {resp.status_code} {resp.text}"
    except Exception as e:
        return False, str(e)
