from modular_logger.config import API_KEY
from currency_utils import convert_currency
from modular_logger.root_logger import logger
from validators import get_currency_input, get_valid_amount
import requests
import time
import sys
from typing import Optional, Callable


def main(max_retries: int = 3) -> None:
    print("=== Currency Converter ===")
    retries: int = 0

    def handle_retry() -> None:
        nonlocal retries
        retries += 1
        time.sleep(1)

    def quit_program() -> None:
        print("Goodbye!")
        sys.exit(0)

    while retries < max_retries:
        amount_input = input("Enter amount(positive number) "
                             "or 'q' to quit: ").strip()
        if amount_input.casefold() == 'q':
            quit_program()

        amount: Optional[float] = get_valid_amount(amount_input)
        if amount is None:
            print("❌ Invalid amount. Please enter a positive number.")
            handle_retry()
            continue

        from_currency: Optional[str] = get_currency_input("From currency code (e.g. USD) "
                                           "or 'q' to quit: ")
        if from_currency.casefold() == 'q':
            quit_program()
        if not from_currency:
            print("❌ Invalid 'From' currency entered.")
            handle_retry()
            continue

        to_currency: Optional[str] = get_currency_input("To currency code "
                                                        "(e.g. GBP or "
                                         "'q' to quit: ")
        if to_currency.casefold() == 'q':
            quit_program()
        if not to_currency:
            print("❌ Invalid 'To' currency entered.")
            handle_retry()
            continue

        try:
            converted: Optional[float] = (
                convert_currency(API_KEY, amount,
                                 from_currency,
                                 to_currency))
        except requests.exceptions.Timeout:
            print("❌ Request timed out. "
                  "Please check your internet connection and try again.")
            handle_retry()
            continue
        except requests.exceptions.ConnectionError:
            print("❌ Connection error. "
                  "Please check your network and try again.")
            handle_retry()
            continue
        except requests.exceptions.HTTPError as http_err:
            status = http_err.response.status_code
            if status == 401:
                print("❌ Unauthorized: Invalid API key. "
                      "Please check your API key.")
            elif status == 429:
                print("⚠️ Rate limit exceeded. "
                      "Please wait before making more requests.")
            else:
                print(f"❌ HTTP error {status}: {http_err.response.reason}")
            logger.error(f"HTTP {status} error during conversion.")
            handle_retry()
            continue
        except ValueError as val_err:
            print(f"❌ Value error: {val_err}")
            logger.error(f"Value error: {val_err}")
            handle_retry()
            continue
        except Exception as e:
            print("❌ An unexpected error occurred. Please check the logs.")
            logger.exception(f"Unexpected error during conversion: {e}")
            handle_retry()
            continue
        else:
            if converted is not None:
                print(f"\n💱 {amount:.2f} {from_currency} "
                      f"= {converted:.2f} {to_currency}")
                logger.info(
                    f"Conversion: {amount:.2f} {from_currency} "
                    f"→ {converted:.2f} {to_currency}"
                )
            else:
                print("⚠️ Conversion failed. "
                      "Please check your API key or currency codes.")
            retries = 0  # reset retries on success

        retry: Optional[str] = (input("\nTry another conversion? (y/n): ")
                                .strip().lower())
        while retry not in ('y', 'n'):
            retry = (input("Please enter 'y' for yes or 'n' for no: ")
                     .strip().lower())

        if retry != 'y':
            quit_program()

    else:
        print("❌ Maximum retries reached. "
              "Exiting program.")

if __name__ == "__main__":
    main()
