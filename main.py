import logging
from currency_utils import convert_currency

logger = logging.getLogger(__name__)


def main():
    print("=== Currency Converter ===")
    try:
        amount = float(input("Enter amount: "))
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
