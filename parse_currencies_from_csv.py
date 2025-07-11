import pandas as pd
import pprint

def generate_currency_dictionary():
    df = pd.read_csv('data/physical_currency_list.csv')
    currency_dict = dict(zip(df.iloc[:, 1], df.iloc[:, 0]))
    pprint.pprint(currency_dict)
    return currency_dict


generate_currency_dictionary()
