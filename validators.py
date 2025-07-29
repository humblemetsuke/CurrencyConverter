from data.valid_currencies import valid_currencies_dict
from modular_logger.root_logger import logger
from typing import Optional


def is_valid_currency(code: str) -> bool:
    """Return True if code is a valid 3-letter currency code."""
    code = code.upper()
    return (code.isalpha() and len(code) == 3
            and code in valid_currencies_dict.values())


def exit_on_interrupt(message: str = "Input cancelled by user. Exiting.",
                      code: int = 1):
    print(f"\n❗ {message}")
    exit(code)


def get_valid_amount(user_input: str) -> Optional[float]:
    """Validate a single user input string as a positive float."""
    try:
        value = float(user_input)
        if value <= 0:
            raise ValueError("Amount must be greater than 0.")
        return value
    except ValueError as e:
        logger.error(f"Invalid amount entered: '{user_input}'. Reason: {e}")
        return None


def get_currency_input(label: str) -> str:
    """Continuously prompt for a valid 3-letter currency code."""
    while True:
        try:
            code = input(f"{label} ").strip().upper()
            if is_valid_currency(code):
                return code
            print(f"❌ Invalid currency. "
                  f"Choose one of: {', '.join(sorted(valid_currencies_dict))}")
        except KeyboardInterrupt:
            exit_on_interrupt()
        except EOFError:
            exit_on_interrupt("No input detected (EOF). "
                              "Exiting...", code=1)
