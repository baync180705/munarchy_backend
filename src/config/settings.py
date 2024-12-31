import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI = os.getenv('MONGO_URI')
    MERCHANT_KEY = os.getenv('MERCHANT_KEY')
    SALT = os.getenv('SALT')
    ENV = os.getenv('ENV')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    EMAIL_SECRET_KEY = os.getenv('EMAIL_SECRET_KEY')
    SSL_CERTFILE = os.getenv('SSL_CERTFILE')
    SSL_KEYFILE = os.getenv('SSL_KEYFILE')
    BASE_URL = os.getenv('BASE_URL')
    SURL = os.getenv('SURL')
    FURL = os.getenv('FURL') 