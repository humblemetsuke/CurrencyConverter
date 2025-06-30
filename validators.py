from constants import VALID_CURRENCIES
from logger_setup import setup_logger

logger = setup_logger()


def is_valid_currency(code: str) -> bool:
    """Check if currency code is exactly 3 alphabetic letters."""
    return code.isalpha() and len(code) == 3 and code.upper() in VALID_CURRENCIES


def get_valid_amount() -> float:
    """Continuously prompt for a valid positive float until correct input is given."""
    while True:
        try:
            raw_input_value = input("Enter amount: ").strip()
            value = float(raw_input_value)
            if value <= 0:
                raise ValueError("Amount must be greater than 0.")
            return value
        except ValueError as e:
            logger.error(f"Invalid amount entered: '{raw_input_value}'. Reason: {e}")
            print(f"❌ {e}")
        except KeyboardInterrupt:
            print("\n❗ Input cancelled by user. Exiting.")
            exit(0)
        except EOFError:
            print("\n❗ No input detected (EOF). Exiting.")
            exit(0)


def get_currency_input(label: str) -> str | None:
    """
        Continuously prompt for a valid currency code (e.g. USD).
        Only allows uppercase 3-letter codes defined in VALID_CURRENCIES.
        """
    while True:
        try:
            code = input(f"{label} currency (e.g. USD): ").strip().upper()
            if is_valid_currency(code):
                return code
            print(f"❌ Invalid {label.lower()} currency. Choose one of: {', '.join(VALID_CURRENCIES)}")
        except KeyboardInterrupt:
            print("\n❗ Input cancelled by user. Exiting.")
            exit(0)
        except EOFError:
            print("\n❗ No input detected (EOF). Exiting.")
            exit(0)
