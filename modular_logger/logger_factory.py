"""Logger factory for named loggers."""

import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from config import LOG_LEVEL, LOG_FILE, get_env_int
from formatters import JsonFormatter, color_formatter, file_formatter
from handlers import get_discord_handler
import os


def setup_logger(name=__name__, use_discord=False, json_format=False) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.propagate = False

    logger.setLevel(LOG_LEVEL)

    # Console
    local_console = StreamHandler()
    local_console.setLevel(LOG_LEVEL)
    local_console.setFormatter(JsonFormatter() if json_format else color_formatter)
    logger.addHandler(local_console)

    # File
    rotation_strategy = (os.getenv("LOG_ROTATION_STRATEGY") or "SIZE").upper()
    backup_count = get_env_int("LOG_BACKUP_COUNT", 5)

    if rotation_strategy == "SIZE":
        rotation_max_bytes = get_env_int("LOG_ROTATION_SIZE_MB", 5) * 1024 * 1024
        file_log_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=rotation_max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
    else:
        when = os.getenv("LOG_ROTATION_TIME", "midnight")
        file_log_handler = TimedRotatingFileHandler(
            LOG_FILE,
            when=when,
            backupCount=backup_count,
            encoding="utf-8"
        )

    file_log_handler.setFormatter(JsonFormatter() if json_format else file_formatter)
    logger.addHandler(file_log_handler)

    # Optional Discord
    if use_discord:
        discord = get_discord_handler()
        if discord:
            logger.addHandler(discord)

    return logger
