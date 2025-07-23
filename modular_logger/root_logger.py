"""Global root logger setup with console, file, and optional Discord handlers."""

import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from config import LOG_LEVEL, LOG_FILE, get_env_int
from formatters import color_formatter, file_formatter
from handlers import get_discord_handler
import os

# Here, the user will choose between time and size rotations strategies.
# The default is SIZE, in the event that this is unchosen or invalid.
# The user can choose between the two strategies via the .env file.
rotation_strategy = (os.getenv("LOG_ROTATION_STRATEGY") or "SIZE").upper()
if rotation_strategy not in {"SIZE", "TIME"}:
    print(f"⚠️ Invalid LOG_ROTATION_STRATEGY '{rotation_strategy}', defaulting to 'SIZE'.")
    rotation_strategy = "SIZE"

backup_count = get_env_int("LOG_BACKUP_COUNT", 5)

global_handlers = []

# Console
root_console_handler = StreamHandler()
root_console_handler.setLevel(LOG_LEVEL)
root_console_handler.setFormatter(color_formatter)
global_handlers.append(root_console_handler)

# File (Rotating or Timed)
#
if rotation_strategy == "SIZE":
    max_bytes = get_env_int("LOG_ROTATION_SIZE_MB", 5) * 1024 * 1024
    root_file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
else:
    rotation_when = os.getenv("LOG_ROTATION_TIME", "midnight")
    root_file_handler = TimedRotatingFileHandler(
        LOG_FILE, when=rotation_when, backupCount=backup_count, encoding="utf-8"
    )

root_file_handler.setFormatter(file_formatter)
global_handlers.append(root_file_handler)

# Optional Discord
# Adds Discord handler only if valid and available.
discord_handler = get_discord_handler()
if discord_handler:
    global_handlers.append(discord_handler)

logging.basicConfig(
    level=LOG_LEVEL,
    handlers=global_handlers,
    force=True  # Python 3.8+: clears existing handlers
)

logging.info(f"Logger initialized at level {LOG_LEVEL} with rotation strategy "
             f"{rotation_strategy}")

logger = logging.getLogger(__name__)