import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AMAZON_URL = os.getenv("AMAZON_URL")
    AMAZON_SIGNIN_URL = os.getenv("AMAZON_SIGNIN_URL")

settings = Settings()
