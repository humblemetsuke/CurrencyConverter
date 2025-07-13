import logging

"""requests sends HTTP requests to external services.
In our project, Discord."""
import requests


class DiscordWebhookHandler(logging.Handler):

    """This is a custom logging handler, that will send log records to
    Discord server using the specified webhook."""

    def __init__(self, webhook_url, level=logging.ERROR, timeout=5):
        super().__init__()
        # This url is where the discord messages will be sent to.
        self.webhook_url = webhook_url

    def emit(self, record):
        log_entry = self.format(record)
        data = {"content": f"🚨 Error Alert:\n{log_entry}"}
        try:
            response = requests.post(self.webhook_url, json=data)
            if response.status_code != 204:
                print(
                    f"[DiscordWebhookHandler] Failed to send: "
                    f"{response.status_code} {response.text}"
                )
        except Exception as e:
            print(f"[DiscordWebhookHandler] Exception: {e}")


logger = logging.getLogger(__name__)
