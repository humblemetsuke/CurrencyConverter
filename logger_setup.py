"""python logging module for creation and management of logs."""
import logging

# OS module necessary due to the usage of environment variables.
import os

# Imports a custom logging handler that sends logs to a Discord webhook.
from notifications import DiscordWebhookHandler

from dotenv import load_dotenv
load_dotenv()  # Loads variables from .env into os.environment


# === Logger Setup ===

def setup_logger() -> logging.Logger:
    """ Imports the DISCORD_WEBHOOK_URL environment variable. If not set,
    then defaults to an empty string. The .strip() method is used for hygiene,
    removing any leading AND trailing whitespaces.
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if len(webhook_url) < 60:  # Further hygiene check, sets an arbitrary threshold
        # for the minimum length of webhook url.
        raise ValueError(
            "❌ Invalid or missing DISCORD_WEBHOOK_URL environment variable. "
            "Please properly configure it in your environment."
        )

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)  # Ensures only logs of ERROR and above are handled.

    """Avoid adding multiple handlers of the same type.
        Prevents adding multiple identical DiscordWebhookHandlers to the same logger,
        which would cause duplicate log messages being sent to Discord. """
    if not any(isinstance(h, DiscordWebhookHandler) for h in logger.handlers):
        handler = DiscordWebhookHandler(webhook_url)  # Creates an instance of the
        # DiscordWebhookHandler logging handler using the valid webhook URL.
        # This handler will send logs to the specified Discord channel.

        # Responsible for the physical layout and format of the handler.
        # %(asctime)s is the timestamp of the log message.
        # %(levelname)s is the level associated with the log.
        # %(message)s: The actual log message.
        handler.setFormatter(logging.Formatter('%(asctime)s -'
                                               ' %(levelname)s -'
                                               ' %(message)s'))

        logger.addHandler(handler)

    return logger
