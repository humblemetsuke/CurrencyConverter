"""Optional logging handlers, including Discord webhook handler."""

import logging
from modular_logger.config import DISCORD_WEBHOOK_URL
from modular_logger.formatters import file_formatter


def get_discord_handler(
    webhook_url: str = DISCORD_WEBHOOK_URL,
    log_level: int = logging.ERROR,
) -> logging.Handler | None:
    """Returns a configured DiscordWebhookHandler if available and valid.
    Falls back to None if the webhook URL is invalid, missing, or if
    the handler cannot be imported or initialized.
    Parameters:
    - webhook_url (str): The Discord webhook URL.
    - log_level (int): Logging level for the handler.
    Returns:
    - logging.Handler | None: Configured handler or None.
"""

    # if the webhook is invalid or missing, skip.
    if not webhook_url or not webhook_url.startswith("https://"):
        print("⚠️ Invalid or missing DISCORD_WEBHOOK_URL. Skipping Discord logging.")
        return None

    try:
        from notifications import DiscordWebhookHandler
    except ImportError:
        print("🔕 DiscordWebhookHandler not available.")
        return None

    try:
        handler = DiscordWebhookHandler(webhook_url)
        handler.setLevel(log_level)
        handler.setFormatter(file_formatter)
        return handler
    except Exception as e:
        print(f"❌ Failed to initialize DiscordWebhookHandler: {e}")
        return None
