"""Environment configuration and validation."""

import os
from dotenv import load_dotenv

load_dotenv()

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "converter.log")

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Required API key
API_KEY = os.getenv("EXCHANGE_API_KEY")
if not API_KEY:
    raise ValueError("Missing EXCHANGE_API_KEY in environment.")

# Logging level validation
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
if LOG_LEVEL not in VALID_LOG_LEVELS:
    raise ValueError(f"Invalid LOG_LEVEL: '{LOG_LEVEL}'. Must be one of: {', '.join(VALID_LOG_LEVELS)}")

# Optional: Discord webhook for logging
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "").strip()


def get_env_int(key: str, default: int) -> int:
    """Utility function to get an integer from environment or default."""
    try:
        return int(os.getenv(key, default))
    except (ValueError, TypeError):
        return default
