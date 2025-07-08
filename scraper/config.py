# Load .env and export vars
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))
CACHE_DIR = os.getenv("CACHE_DIR", "./cached_pages")

os.makedirs(CACHE_DIR, exist_ok=True)
