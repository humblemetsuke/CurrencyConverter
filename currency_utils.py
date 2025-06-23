import requests
import logging
from config import API_KEY


#This is used to create a logger specific to this module (currency_utils.py).
logger = logging.getLogger(__name__)

def get_exchange_rate(from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}"
    logger.info(f"Fetching exchange rate: {from_currency} -> {to_currency}")

    try:
        response = requests.get(url)
        data = response.json()
    #If the request fails (invalid URL/internet disconnection) returns traceback and None.
    except Exception as e:
        logger.exception("Failed to fetch or parse exchange rate data.")
        return None

    if data.get('result') == 'success':
        rate = data['conversion_rate']
        logger.info(f"Rate found: 1 {from_currency} = {rate} {to_currency}")
        return rate
    else:
        #Returns the error message(s) in the event that the API call was NOT successful.
        logger.error(f"API error: {data.get('error-type', 'Unknown error')}")
        return None

def convert_currency(amount, from_currency, to_currency):
    logger.debug(f"Converting {amount} {from_currency} to {to_currency}")
    rate = get_exchange_rate(from_currency, to_currency)

    #If the conversion is successful, conversion is performed, and logged.
    if rate:
        converted = amount * rate
        logger.info(f"Converted amount: {converted:.2f} {to_currency}")
        return converted
    else:
        #if conversion is not successful, log a warning and returns None.
        logger.warning("Conversion failed due to missing exchange rate.")
        return None
