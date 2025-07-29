"""Environment configuration and validation."""

import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

LOG_DIR: Path = Path("logs")  # Name of directory where logs will be stored.
LOG_FILE: Path = LOG_DIR / "converter.log"  # Name of logs

# Ensure logs directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Required API key
API_KEY: str = os.getenv("EXCHANGE_RATE_API_KEY")
if not API_KEY:
    raise ValueError("Missing EXCHANGE_RATE_API_KEY in environment.")

# Logging level validation
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()  # determines level of
# verbosity of the log levels
VALID_LOG_LEVELS: set[str] = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
# Specify permitted log levels.
if LOG_LEVEL not in VALID_LOG_LEVELS:
    raise ValueError(f"Invalid LOG_LEVEL: '{LOG_LEVEL}'. Must be one of: "
                     f"{', '.join(VALID_LOG_LEVELS)}")

# Optional: Discord webhook for logging
DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL", "").strip()


def get_env_int(key: str, default: int) -> int:
    """Utility function to get an integer from environment or default."""
    try:
        return int(os.getenv(key, default))
    except (ValueError, TypeError):
        return default
