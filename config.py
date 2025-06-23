import os
import logging
from logging import StreamHandler
from colorlog import ColoredFormatter
from dotenv import load_dotenv


load_dotenv()
API_KEY =os.getenv("EXCHANGE_API_KEY")

if not API_KEY:
    raise ValueError("Missing EXCHANGE_API_KEY in the environment.")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

#LOG_FILE simply specifies the output location for the log file(s).
LOG_FILE = "logs/converter.log"

# checks if logs folder exists, if it does not, it is created. 2nd argument is used to avoid any errors if folder already exists.
os.makedirs("logs", exist_ok = True)


#DATE_FMT utilises ISO format for consistency and 24 hour time formatting.
DATE_FMT = "%Y-%m-%d %H:%M:%S"

color_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",

    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
)

file_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt = DATE_FMT
)

#Below will print coloured logs to the console.
console_handler = StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(color_formatter)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(file_formatter)



logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

# Clear previous handlers to avoid duplicate logs in some environments
if logger.hasHandlers():
    logger.handlers.clear()

logger.addHandler(console_handler)
logger.addHandler(file_handler)
