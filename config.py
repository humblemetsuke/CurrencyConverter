import logging
import os
from logging import StreamHandler
from colorlog import ColoredFormatter
from dotenv import load_dotenv
from notifications import DiscordWebhookHandler

load_dotenv()

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

# Setup formatters
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

file_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

# Setup handlers list
handlers = []

# Console handler
console_handler = StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(color_formatter)
handlers.append(console_handler)

# File handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(file_formatter)
handlers.append(file_handler)

# Discord handler (only if URL is valid)
if DISCORD_WEBHOOK_URL:
    if len(DISCORD_WEBHOOK_URL) < 60 or not DISCORD_WEBHOOK_URL.startswith("https://"):
        print("⚠️ DISCORD_WEBHOOK_URL appears invalid. Skipping Discord logging.")
    else:
        try:
            discord_handler = DiscordWebhookHandler(DISCORD_WEBHOOK_URL)
            discord_handler.setLevel(logging.ERROR)
            discord_handler.setFormatter(file_formatter)  # plaintext for Discord
            handlers.append(discord_handler)
        except Exception as e:
            print(f"⚠️ Failed to initialize Discord webhook handler: {e}")
else:
    print("No DISCORD_WEBHOOK_URL provided. Discord notifications are disabled.")

# Configure root logger
logging.basicConfig(
    level=LOG_LEVEL,
    handlers=handlers,
    force=True,  # Clear existing handlers before adding new ones (Python 3.8+)
)
