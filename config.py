import logging
import os
import json
from logging import StreamHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from dotenv import load_dotenv
import requests
load_dotenv()

# ─────────────────────────────────────────────────────────────
# Config loading
# ─────────────────────────────────────────────────────────────

API_KEY = os.getenv("EXCHANGE_API_KEY")
if not API_KEY:
    raise ValueError("Missing EXCHANGE_API_KEY in environment.")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
if LOG_LEVEL not in VALID_LOG_LEVELS:
    raise ValueError(
        f"Invalid LOG_LEVEL: '{LOG_LEVEL}'. Must be one of: {', '.join(VALID_LOG_LEVELS)}"
    )

LOG_FILE = "logs/converter.log"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "").strip()

# Ensure logs directory exists before file handlers use it
os.makedirs("logs", exist_ok=True)


# -------------------------------------------
# Optional colorlog integration:
# If the user doesn't have the `colorlog` module installed,
# fall back to plain logging.Formatter to avoid crashing.
#
# 1) Try to import colorlog.
# 2) If available, use it for colored console output.
# 3) If not, fall back to standard text formatting.
# -------------------------------------------
# ─────────────────────────────────────────────────────────────
# Formatters
# ─────────────────────────────────────────────────────────────

try:

    from colorlog import ColoredFormatter
    color_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
    },
)

except ImportError:
    print("Colorlog not found. Using basic formatter instead.")
    color_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

file_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

# ─────────────────────────────────────────────────────────────
# Optional Discord Webhook Handler
# ─────────────────────────────────────────────────────────────

def get_discord_handler(log_level=logging.ERROR) -> logging.Handler | None:
    """
       Attempts to create and return a DiscordWebhookHandler for error logging.
       Returns None if the handler is unavailable or misconfigured.
       """
    try:
        from notifications import DiscordWebhookHandler
    except ImportError:
        print("🔕 DiscordWebhookHandler not available. Skipping Discord logging.")
        return None

    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()

    if len(webhook_url) < 60 or not webhook_url.startswith("https://"):
        print("⚠️ Invalid or missing DISCORD_WEBHOOK_URL. Skipping Discord logging.")
        return None

    try:
        handler = DiscordWebhookHandler(webhook_url)
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        ))
        return handler
    except Exception as e:
        print(f"❌ Failed to initialize DiscordWebhookHandler: {e}")
        return None

# ─────────────────────────────────────────────────────────────
# Handler Setup
# ─────────────────────────────────────────────────────────────
# Setup handlers list
handlers = []

# Console handler
console_handler = StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(color_formatter)
handlers.append(console_handler)

"""File size-based or time-based rotation strategy
Warn if both size and time rotation configs exist.
Python’s logging.handlers does not natively 
support combining time- and size-based rotation in a single handler. 
This is why it is required that the user specifies their desired strategy."""
if "LOG_ROTATION_SIZE_MB" in os.environ and "LOG_ROTATION_TIME" in os.environ:
    print(
        "⚠️ Both LOG_ROTATION_SIZE_MB and LOG_ROTATION_TIME are "
        "set in the environment. "
        "Only one will be used based on LOG_ROTATION_STRATEGY."
    )

rotation_strategy = os.getenv("LOG_ROTATION_STRATEGY", "SIZE").upper()
backup_count = int(os.getenv("LOG_BACKUP_COUNT", "5"))

if rotation_strategy == "SIZE":
    max_bytes = int(os.getenv("LOG_ROTATION_SIZE_MB", "5")) * 1024 * 1024
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
elif rotation_strategy == "TIME":
    when = os.getenv("LOG_ROTATION_TIME", "midnight")
    file_handler = TimedRotatingFileHandler(
        LOG_FILE, when=when, backupCount=backup_count, encoding = "utf-8"
    )
else:
    raise ValueError("LOG_ROTATION_STRATEGY must be either 'SIZE' or 'TIME' ")


# File handler

file_handler.setFormatter(file_formatter)
handlers.append(file_handler)


# Use the helper to get the Discord handler if possible
discord_handler = get_discord_handler()
if discord_handler:
    handlers.append(discord_handler)
else:
    print("Discord logging disabled or handler unavailable.")


# ─────────────────────────────────────────────────────────────
# Final logger setup
# ─────────────────────────────────────────────────────────────

# Configure root logger
# force=True clears any existing handlers before adding these (Python 3.8+)
logging.basicConfig(
    level=LOG_LEVEL,
    handlers=handlers,
    force=True,
)
