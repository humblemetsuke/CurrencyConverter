
from data.valid_currencies import valid_currencies_dict
from logger_setup import setup_logger

logger = setup_logger()

def is_valid_currency(code: str) -> bool:
    """Return True if code is a valid 3-letter currency code."""
    code =code.upper()
    return (code.isalpha() and len(code) == 3
            and code in valid_currencies_dict.values())

def exit_on_interrupt(message: str = "Input cancelled by user. "
                                     "Exiting.", code: int = 1):
    print(f"\n❗ {message}")
    exit(code)

def get_valid_amount() -> float:
    """Continuously prompt for a valid positive
    float until correct input is given."""
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
            exit_on_interrupt()
        except EOFError:
            exit_on_interrupt("No input detected (EOF). Exiting...", code=1)

def get_currency_input(label: str) -> str:
    """Continuously prompt for a valid 3-letter currency code
    defined in valid_currencies_dict."""
    while True:
        try:
            code = input(f"{label} currency (e.g. USD): ").strip().upper()
            if is_valid_currency(code):
                return code
            print(f"❌ Invalid {label.lower()} currency. "
                  f"Choose one of: {', '.join(sorted(valid_currencies_dict))}")
        except KeyboardInterrupt:
            exit_on_interrupt()
        except EOFError:
            exit_on_interrupt("No input detected (EOF). Exiting...", code=1)
