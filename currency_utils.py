import requests
from config import API_KEY


def get_exchange_rate(from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}"
    response = requests.get(url)
    data = response.json()
    if data['result'] == 'success':
        return data['conversion_rate']
    else:
        print("Error fetching exchange rate:", data['error-type'])
        return None

def convert_currency(amount, from_currency, to_currency):
    rate = get_exchange_rate(from_currency, to_currency)
    if rate:
        return amount * rate
    else:
        return None
