import sys
import os
import pandas as pd
import pprint


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def generate_currency_dictionary():
    csv_path = str(resource_path('data/physical_currency_list.csv'))
    df = pd.read_csv(csv_path)
    currency_dict = dict(zip(df.iloc[:, 1], df.iloc[:, 0]))
    pprint.pprint(currency_dict)
    return currency_dict


generate_currency_dictionary()
