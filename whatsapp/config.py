import os
from dotenv import load_dotenv

load_dotenv()

# Whatsapp bot
WHATSAPP_TOKEN = os.environ["WHATSAPP_TOKEN"]
WHATSAPP_API_VERSION = os.environ["WHATSAPP_API_VERSION"]
WHATSAPP_PHONE_NUMBER_ID = os.environ["WHATSAPP_PHONE_NUMBER_ID"]
WHATSAPP_VERIFY_TOKEN = os.environ["WHATSAPP_VERIFY_TOKEN"]
