from dotenv import load_dotenv
from django.conf import settings
import os

load_dotenv()

if settings.PAYMENT_ENV == 'production':
    PAGARME_API_KEY = os.environ['PAGARME_API_KEY_LIVE']
    PAGARME_ENCRYPTION_KEY = os.environ['PAGARME_ENCRYPTION_KEY_LIVE']
else:
    PAGARME_API_KEY = os.environ['PAGARME_API_KEY_TEST']
    PAGARME_ENCRYPTION_KEY = os.environ['PAGARME_ENCRYPTION_KEY_TEST']
