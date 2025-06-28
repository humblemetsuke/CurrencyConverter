from config import API_KEY
from currency_utils import convert_currency
from logger_setup import setup_logger
from validators import get_currency_input, get_valid_amount

logger = setup_logger()


def main():
    print("=== Currency Converter ===")

    amount = get_valid_amount()
    if amount is None:
        return

    from_currency = get_currency_input("From")
    if not from_currency:
        return

    to_currency = get_currency_input("To")
    if not to_currency:
        return

    try:
        converted = convert_currency(API_KEY, amount, from_currency, to_currency)
        if converted is not None:
            print(f"\n💱 {amount:.2f} {from_currency} = {converted:.2f} {to_currency}")
            logger.info(
                f"Conversion: {amount:.2f} {from_currency} "
                f"→ {converted:.2f} {to_currency}"
            )
        else:
            print("⚠️ Conversion failed. Please check your API key or currency codes.")
    except Exception:
        logger.exception("An error occurred during the conversion.")
        print("❌ An unexpected error occurred. Please check logs.")

    # Optional: Retry
    retry = input("\nTry another conversion? (y/n): ").strip().lower()
    if retry == "y":
        print()
        main()


if __name__ == "__main__":
    main()
