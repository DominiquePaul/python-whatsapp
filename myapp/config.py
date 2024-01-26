import os
from dotenv import load_dotenv

load_dotenv()

# Whatsapp bot
WHATSAPP_TOKEN = os.environ["WHATSAPP_TOKEN"]
APP_ID = os.environ["APP_ID"]
APP_SECRET = os.environ["APP_SECRET"]
WHATSAPP_API_VERSION = os.environ["WHATSAPP_API_VERSION"]
PHONE_NUMBER_ID = os.environ["PHONE_NUMBER_ID"]
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]
