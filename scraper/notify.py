import requests
import logging
from .config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def send_message(text):
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        resp = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
        if resp.status_code != 200:
            logger.error(f"Telegram fallo: {resp.text}")
    except Exception as e:
        logger.error(f"Exception enviando Telegram: {e}")
