import os
from dotenv import load_dotenv

load_dotenv()
# Read API key and base URL from environment variables, with defaults
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")


# Explicit, pre-emptive check to see if API key is valid and present.
if not API_KEY:
    raise RuntimeError(f"EXCHANGE_RATE_API_KEY is either missing from environment"
                       f"or .env file")


# Base URL for the exchange rate API — can be overridden in .env or environment
EXCHANGE_RATE_BASE_URL = os.getenv(
    "EXCHANGE_RATE_BASE_URL",
    "https://v6.exchangerate-api.com/v6"
)


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "app.log")
