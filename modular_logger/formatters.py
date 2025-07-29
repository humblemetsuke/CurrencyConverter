"""
Logging is the standard logging library.
json is imported to allow for formatting the logs into JSON.
os is necessary for environment variable access.
Optional: typing hint to specify variables that may be None.
This does not assist in cross-compatibility,
as Python ignores type hints at runtime.
Optional is used primarily in static analysis and assisting the user.
Logging formatters: JSON, colorlog, and plain text.
warnings are used because the print statement is not machine-readable,
as it simply provides raw text/data with neither structure nor formatting.
Print cannot be filtered or disabled, leading to excess noise.
No severity level can be assigned or configured with print statements.
Warnings solves these issues. Furthermore,
they allow for alerting the user to non-fatal issues without breaking
or interrupting the flow of the overall program.
Warnings can be logged and tagged, aiding in debugging and navigating.

"""

import logging
import json
import warnings
import os
from typing import Optional
# Converts a log record into a JSON string.
# Adds timestamp, log level, logger name, message, and exception (if any).
# This is intended to be used for external services. JSON is more readable.


def get_api_key(raise_error: bool = True) -> Optional[str]:

    """This function attempts to read the EXCHANGE_RATE_API_KEY
    from the environment variable, env file. It accepts a flag raise_error
    (default True) that controls whether missing key raises an exception.
    It also returns Optional[str] meaning either str or None can be returned.
    None is returned in the event that the API key is missing.
    """
    api_key = os.getenv("EXCHANGE_API_KEY")
    if not api_key:
        message = "Missing EXCHANGE_API_KEY in environment."
        if raise_error:
            raise EnvironmentError(message)
        else:
            warnings.warn(message)
            return None  # signals the absence of the API key.
    return api_key


class JsonFormatter(logging.Formatter):
    def __init__(self, datefmt: str = "%Y-%m-%d %H:%M:%S"):
        super().__init__(datefmt=datefmt)

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        try:
            return json.dumps(log_record)
        except TypeError as e:
            fallback = super().format(record)
            return f"{fallback} [JsonFormatter serialization error: {e}]"


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
    warnings.warn("⚠️ colorlog not installed, falling back to plain formatting.")
    color_formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")


# Standard, plaintext format for log files.
file_formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
