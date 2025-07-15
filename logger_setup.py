import logging
import os
import json
from logging import StreamHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────────────
# Config loading and validation helpers
# ─────────────────────────────────────────────────────────────

def get_env_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        print(f"⚠️ Invalid integer for {key}, defaulting to {default}")
        return default


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

# ─────────────────────────────────────────────────────────────
# JSON Formatter for structured logging (optional usage)
# ─────────────────────────────────────────────────────────────

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# ─────────────────────────────────────────────────────────────
# Formatters Setup (with optional colorlog)
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
# Optional Discord Webhook Handler factory
# ─────────────────────────────────────────────────────────────

def get_discord_handler(
    webhook_url: str = DISCORD_WEBHOOK_URL,
    log_level: int = logging.ERROR,
) -> logging.Handler | None:
    """
    Attempts to create and return a DiscordWebhookHandler for error logging.
    Returns None if the handler is unavailable or misconfigured.
    """
    if (not webhook_url or len(webhook_url) < 60 or not
    webhook_url.startswith("https://")):
        print("⚠️ Invalid or missing DISCORD_WEBHOOK_URL. "
              "Skipping Discord logging.")
        return None

    try:
        from notifications import DiscordWebhookHandler
    except ImportError:
        print("🔕 DiscordWebhookHandler not available. "
              "Skipping Discord logging.")
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
# Log rotation strategy and handler setup
# ─────────────────────────────────────────────────────────────

# Warn if both size and time rotation env vars are set
if "LOG_ROTATION_SIZE_MB" in os.environ and "LOG_ROTATION_TIME" in os.environ:
    print(
        "⚠️ Both LOG_ROTATION_SIZE_MB and LOG_ROTATION_TIME are "
        "set in the environment. Only one will be used "
        "based on LOG_ROTATION_STRATEGY."
    )

VALID_ROTATION_STRATEGIES = {"SIZE", "TIME"}
rotation_strategy = (os.getenv("LOG_ROTATION_STRATEGY") or "SIZE").upper()

if rotation_strategy not in VALID_ROTATION_STRATEGIES:
    print(f"⚠️ Invalid LOG_ROTATION_STRATEGY '{rotation_strategy}', "
          f"defaulting to 'SIZE'.")
    rotation_strategy = "SIZE"

backup_count = get_env_int("LOG_BACKUP_COUNT", 5)

handlers = []

# Console handler (always enabled)
console_handler = StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(color_formatter)
handlers.append(console_handler)

# File handler with rotation
if rotation_strategy == "SIZE":
    max_bytes_mb = get_env_int("LOG_ROTATION_SIZE_MB", 5)
    max_bytes = max_bytes_mb * 1024 * 1024
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
elif rotation_strategy == "TIME":
    when = os.getenv("LOG_ROTATION_TIME", "midnight")
    file_handler = TimedRotatingFileHandler(
        LOG_FILE, when=when, backupCount=backup_count, encoding="utf-8"
    )
else:
    raise ValueError("LOG_ROTATION_STRATEGY must be either 'SIZE' or 'TIME'")

file_handler.setFormatter(file_formatter)
handlers.append(file_handler)

# Optional Discord webhook logging
discord_handler = get_discord_handler()
if discord_handler:
    handlers.append(discord_handler)
else:
    print("Discord logging disabled or handler unavailable.")

# ─────────────────────────────────────────────────────────────
# Final root logger configuration
# ─────────────────────────────────────────────────────────────

logging.basicConfig(
    level=LOG_LEVEL,
    handlers=handlers,
    force=True,  # Clear existing handlers (Python 3.8+)
)

logging.info(f"Logger initialized at level {LOG_LEVEL} with rotation strategy {rotation_strategy}")
