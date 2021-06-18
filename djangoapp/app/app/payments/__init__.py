from dotenv import load_dotenv
import os

load_dotenv()

PAGARME_API_KEY = os.environ['PAGARME_API_KEY']
PAGARME_ENCRYPTION_KEY = os.environ['PAGARME_ENCRYPTION_KEY']