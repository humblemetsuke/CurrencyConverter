"""
Setup for environment-based API key loading and
logging configuration with colored console output and file logging.
"""


import os
import logging
from logging import StreamHandler
from colorlog import ColoredFormatter
from dotenv import load_dotenv
from notifications import DiscordWebhookHandler


# API keys should never be hard-coded. They are saved in environment variables.
# load_dotenv() loads environment variables from a .env file into the environment.
load_dotenv()

# Loads API Key. ValueError is raised because the API key being present is critical.
API_KEY = os.getenv("EXCHANGE_API_KEY")
if not API_KEY:
    raise ValueError("Missing EXCHANGE_API_KEY in environment.")

# Setup logging. os.makedirs is used to create a directory called "logs" if not exists.
# To avoid any errors if the directory already exists, we set exist_ok = True .
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = "logs/converter.log"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

os.makedirs("logs", exist_ok=True)


# Colour coded output sent to console to aid in visual inspection.
# Colour-coding ensures at a glance, specific issues can be narrowed down.
color_formatter = ColoredFormatter(

"%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
)

# Console Handler prints colourised output.
# For reference, the colour codes are specified in the 'log_colors' dictionary inside ColoredFormatter.
# Events are keys, colours are values. Each log level has unique colour to avoid confusion.


console_handler = StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(color_formatter)

# File Handler (plaintext output stored to logs/converter.log).
# This is intended for persistent storage purposes.

file_handler = logging.FileHandler(LOG_FILE)
file_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)
file_handler.setFormatter(file_formatter)

handlers = [console_handler, file_handler]

# discord_handler.setLevel(logging.ERROR) ensures that events of error and higher are sent to the discord.
if DISCORD_WEBHOOK_URL:
    discord_handler = DiscordWebhookHandler(DISCORD_WEBHOOK_URL)
    discord_handler.setLevel(logging.ERROR)
    discord_handler.setFormatter(file_formatter)  # plaintext format
    handlers.append(discord_handler)

# The root logger is configured using both of the handlers specified above:
# console_handler, file_handler
logging.basicConfig(
    level = LOG_LEVEL,
    handlers =  handlers,
    force = True # This is used to clear any/all existing handlers first.
                # This prevents unnecessary duplication.
                # force = True ONLY works with Python 3.8+
)

