"""Optional logging handlers, including Discord webhook handler."""

import logging
from config import DISCORD_WEBHOOK_URL
from formatters import file_formatter


def get_discord_handler(
    webhook_url: str = DISCORD_WEBHOOK_URL,
    log_level: int = logging.ERROR,
) -> logging.Handler | None:

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
