import logging
import requests

logger = logging.getLogger(__name__)


def get_exchange_rate(api_key, from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"
    logger.info(f"Fetching exchange rate: {from_currency} -> {to_currency}")

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
    except Exception:
        logger.exception("Failed to fetch or parse exchange rate data.")
        return None

    if data.get("result") == "success":
        rate = data["conversion_rate"]
        logger.info(f"Rate found: 1 {from_currency} = {rate} {to_currency}")
        return rate
    else:
        logger.error(f"API error: {data.get('error-type', 'Unknown error')}")
        return None


def convert_currency(api_key, amount, from_currency, to_currency):
    logger.debug(f"Converting {amount} {from_currency} to {to_currency}")
    rate = get_exchange_rate(api_key, from_currency, to_currency)

    if rate is not None:
        converted = amount * rate
        logger.info(f"Converted amount: {converted:.2f} {to_currency}")
        return converted
    else:
        logger.warning("Conversion failed due to missing exchange rate.")
        return None
