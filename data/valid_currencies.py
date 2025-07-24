from parse_currencies_from_csv import generate_currency_dictionary

# The generate_currency_dictionary function internally uses pprint.pprint()
# to display the dictionary for better readability (separation of concerns).
# This file assigns the returned dictionary to `valid_currencies` for easy use.
# The dictionary keys are currency names, values are 3-letter currency codes.

valid_currencies_dict = generate_currency_dictionary()
