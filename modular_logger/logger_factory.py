"""Logger factory for named loggers.
logging: Base logging module.
StreamHandler: Logs to console (stdout).
RotatingFileHandler: Rotates logs based on file size.
TimedRotatingFileHandler: Rotates logs based on time (e.g., daily).
os is used to read environment variables via os.getenv()


"""

import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from modular_logger.config import LOG_LEVEL, LOG_FILE, get_env_int
from modular_logger.formatters import JsonFormatter, color_formatter, file_formatter
from modular_logger.handlers import get_discord_handler
import os


def setup_logger(name=__name__, use_discord=False, json_format=False) -> logging.Logger:
    logger = logging.getLogger(name)

    # prevents duplicate handlers.
    # If logger already has handlers, return as is.
    if logger.handlers:

        return logger
    logger.propagate = False # Prevents log records passing up to parents.
    #

    logger.setLevel(LOG_LEVEL)

    # Console
    # Creates a console output handler.
    # Applies same level as logger (e.g., INFO or DEBUG).
    local_console = StreamHandler()
    local_console.setLevel(LOG_LEVEL)
    local_console.setFormatter(JsonFormatter() if json_format else color_formatter)
    logger.addHandler(local_console)

    # Read environment variable LOG_ROTATION_STRATEGY
    # to determine how to rotate logs (SIZE or TIME).
    rotation_strategy = (os.getenv("LOG_ROTATION_STRATEGY") or "SIZE").upper()
    # Specifies how many rotated log files to keep, here, 5 has been specified.
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
        # when is a string like "midnight", "H", "D".
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
    # If enabled, create and attach a custom handler that
    # logs to a Discord webhook.
    # The handler is defined in handlers.py.
    if use_discord:
        discord = get_discord_handler()
        if discord:
            logger.addHandler(discord)

    return logger
