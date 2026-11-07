# loads .env, creates the Hindsight client, bank name
import atexit
import os
from functools import lru_cache
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()
BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
API_KEY = os.getenv("HINDSIGHT_API_KEY", "")
BANK = os.getenv("HINDSIGHT_BANK", "team-acme")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
@lru_cache(maxsize=1)
def get_client():
    client = Hindsight(base_url=BASE_URL, api_key=API_KEY)
    atexit.register(client.close)
    return client