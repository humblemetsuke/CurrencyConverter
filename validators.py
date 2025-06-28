from logger_setup import setup_logger

logger = setup_logger()


def is_valid_currency(code: str) -> bool:
    """Check if currency code is exactly 3 alphabetic letters."""
    return code.isalpha() and len(code) == 3


def get_valid_amount() -> float | None:
    """Prompt for amount input; returns positive float or None if invalid."""
    raw_input = input("Enter amount: ").strip()
    try:
        value = float(raw_input)
        if value < 0:
            raise ValueError("Amount must be positive.")
        return value
    except ValueError as e:
        logger.error(f"Invalid amount entered: '{raw_input}'. Reason: {e}")
        print(f"❌ {e}")
        return None
    except KeyboardInterrupt:
        print("\n❗ Input cancelled by user. Exiting.")
        exit(0)
    except EOFError:
        print("\n❗ No input detected (EOF). Exiting.")
        exit(0)


def get_currency_input(label: str) -> str | None:
    """Prompt for currency code input;
    returns 3-letter uppercase code or None if invalid."""
    code = input(f"{label} currency (e.g. USD): ").upper().strip()
    if not is_valid_currency(code):
        print(
            f"❌ Invalid '{label.lower()}' currency code. Must be a 3-letter code like USD."
        )
        return None
    return code
