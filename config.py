import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Load API Key
API_KEY = os.getenv("EXCHANGE_API_KEY")
if not API_KEY:
    raise ValueError("Missing EXCHANGE_API_KEY in environment.")

# Setup logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = "logs/converter.log"

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # Also logs to console
    ]
)
