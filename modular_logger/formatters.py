"""Logging formatters: JSON, colorlog, and plain text."""

import logging
import json

# Converts a log record into a JSON string.
# Adds timestamp, log level, logger name, message, and exception (if any).
# This is intended to be used for external services. JSON is more readable.
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


# Colorlog provides coloured logs allowing for increased readability.
# This is an optional feature and so if it is not installed, defaults back to
# plain text logs.
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
    print("⚠️ colorlog not installed, falling back to plain formatting.")
    color_formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")


# Standard, plaintext format for log files.
file_formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
