"""The generate_currency_dictionary function internally uses pprint.pprint()
to display the dictionary for better readability (separation of concerns).
This file assigns the returned dictionary to valid_currencies_dict for easy use.
The dictionary keys are currency names, values are 3-letter currency codes.
"""


from parse_currencies_from_csv import generate_currency_dictionary
try:
    valid_currencies_dict: dict[str, str] = generate_currency_dictionary()
except Exception as e:
    raise RuntimeError("Failed to generate valid_currencies_dict") from e
