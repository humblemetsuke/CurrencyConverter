
from parse_currencies_from_csv import generate_currency_dictionary


"""No need for print statement, generate_currency_dictionary function
already uses pprint.pprint() improving readability. pprint.pprint functionality
performed in parse_currencies_from_csv file for separation of concerns.
Use valid_currencies as variable, for ease of use and point of reference.
valid_currencies is a dictionary where keys are the name of the currency,
the values are the 3 lettered currency codes. """

valid_currencies_dict = generate_currency_dictionary()

