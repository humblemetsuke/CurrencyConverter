import logging
import requests
import os
from config import API_KEY, EXCHANGE_RATE_BASE_URL
from requests.exceptions import RequestException
from modular_logger.root_logger import logger




def get_exchange_rate(from_currency: str,
                      to_currency: str) -> float |None:
    api_key = API_KEY
    if not api_key or not from_currency or not to_currency:
        logger.error("One or more of the required parameters is missing "
                     "for exchange rate lookup.")
        return None


    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if not (from_currency.isalpha() and len(from_currency) == 3 and
            to_currency.isalpha() and len(to_currency) == 3):
        logger.error(f"Invalid currency codes: {from_currency}, {to_currency}. "
                     "Expected 3-letter alphabetic ISO codes.")
        return None
    url = f"{EXCHANGE_RATE_BASE_URL}/{api_key}/pair/{from_currency}/{to_currency}"
    logger.info(f"Fetching exchange rate: {from_currency} -> {to_currency} from {url}")

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
    except RequestException as req_err:
        logger.exception(f"HTTP request has failed: {req_err}")
        return None

    if data.get("result") == "success":
        rate = data["conversion_rate"]
        logger.info(f"Rate found: 1 {from_currency} = {rate} {to_currency}")
        return rate
    else:
        logger.error(f"Exchange rate API error: "
                     f"{data.get('error-type', 'Unknown')} | Response: {data}")
        return None


def convert_currency(amount: float, from_currency: str,
                     to_currency: str) -> float | None:
    if not isinstance(amount, (int, float)) or amount <= 0:
        logger.error(f"Invalid amount for conversion: {amount}")
        return None
    logger.debug(f"Converting {amount} {from_currency} to {to_currency}")
    rate = get_exchange_rate(from_currency, to_currency)

    if rate is not None:
        converted = amount * rate
        logger.info(f"Converted amount: {converted:.2f} {to_currency}")
        return converted
    else:
        logger.warning("Conversion failed due to missing exchange rate.")
        return None
