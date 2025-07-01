from config import API_KEY
from currency_utils import convert_currency
from logger_setup import setup_logger
from validators import get_currency_input, get_valid_amount
import requests
logger = setup_logger()

def main():
    print("=== Currency Converter ===")

    amount = get_valid_amount()
    if amount is None:
        print("❌ You have not entered any value.")
        return

    from_currency = get_currency_input("From")
    if not from_currency:
        print("❌ Invalid 'From' currency entered.")
        return

    to_currency = get_currency_input("To")
    if not to_currency:
        print("❌ Invalid 'To' currency entered.")
        return

    try:
        converted = convert_currency(API_KEY, amount, from_currency, to_currency)
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Please check your internet connection and try again.")
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection error. Please check your network and try again.")
    except requests.exceptions.HTTPError as http_err:
        status = http_err.response.status_code
        if status == 401:
            print("❌ Unauthorized: Invalid API key. Please check your API key.")
        elif status == 429:
            print("⚠️ Rate limit exceeded. Please wait before making more requests.")
        else:
            print(f"❌ HTTP error {status}: {http_err.response.reason}")
        logger.error(f"HTTP {status} error during conversion.")
    except ValueError as val_err:
        print(f"❌ Value error: {val_err}")
        logger.error(f"Value error: {val_err}")
    except Exception as e:
        print("❌ An unexpected error occurred. Please check the logs.")
        logger.exception("Unexpected error during conversion.")

    else:
        if converted is not None:
            print(f"\n💱 {amount:.2f} {from_currency} = {converted:.2f} {to_currency}")
            logger.info(
                f"Conversion: {amount:.2f} {from_currency} "
                f"→ {converted:.2f} {to_currency}"
            )
        else:
            print("⚠️ Conversion failed. Please check your API key or currency codes.")


    # Optional: Retry
    retry = input("\nTry another conversion? (y/n): ").strip().lower()
    if retry == "y":
        print()
        main()


if __name__ == "__main__":
    main()


