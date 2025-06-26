import logging
from currency_utils import convert_currency
from notifications import DiscordWebhookHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


discord_handler = DiscordWebhookHandler("YOUR_DISCORD_WEBHOOK_URL")
discord_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(discord_handler)

# Sample error to verify that the discord notification works as intended.
# try:
#   1 / 0
# except ZeroDivisionError:
#    logger.exception("Division by zero occurred!")



def main():
    print("=== Currency Converter ===")
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        logger.error("Invalid amount entered.")
        print("Please enter a valid number.")
        return
    try:
        from_currency = input("From currency (e.g. USD): ").upper()
        to_currency = input("To currency (e.g. EUR): ").upper()

        converted = convert_currency(amount, from_currency, to_currency)
        if converted is not None:
            print(f"{amount} {from_currency} = {converted:.2f} {to_currency}")
        else:
            print("Conversion failed.")
    except Exception as e:
        logger.exception("An error occurred during the conversion.")


if __name__ == "__main__":
    main()
