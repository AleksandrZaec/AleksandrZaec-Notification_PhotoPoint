import requests
from config.settings import SMSC_LOGIN, SMSC_PASSWORD

def send_sms_smsc(phone_number, message):
    if not phone_number:
        return False, "No phone number"

    url = "https://smsc.ru/sys/send.php"
    params = {
        'login': SMSC_LOGIN,
        'psw': SMSC_PASSWORD,
        'phones': phone_number,
        'mes': message,
        'fmt': 3,
    }

    try:
        response = requests.post(url, data=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 'OK':
            return True, f"SMS sent, id: {data.get('id')}"
        else:
            return False, data.get('status_text', 'Unknown error')
    except Exception as e:
        return False, str(e)

def send_sms(recipient, message):
    if not recipient.phone_number:
        return False, "No phone number"
    return send_sms_smsc(recipient.phone_number, message)