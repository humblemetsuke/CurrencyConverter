import sys
import os
import pandas as pd
import pprint


def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource, works for development and for PyInstaller.

    PyInstaller bundles files into a temporary folder accessible via sys._MEIPASS.
    If not running in a PyInstaller bundle, return the path relative to the current directory.
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def generate_currency_dictionary() -> dict:
    """
    Reads the currency CSV file and returns a dictionary mapping
    currency name (column 1) to 3-letter currency code (column 0).

    The dictionary is also pretty-printed for easier visual inspection.
    """
    csv_path = resource_path('data/physical_currency_list.csv')
    df = pd.read_csv(csv_path)
    currency_dict = dict(zip(df.iloc[:, 1], df.iloc[:, 0]))

    pprint.pprint(currency_dict)
    return currency_dict


if __name__ == "__main__":
    generate_currency_dictionary()
