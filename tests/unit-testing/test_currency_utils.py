"""unittest is Python's in-built unit testing library.
patch is used mock/replace portions of the code during tests,
such as API calls.
This simulates actual API calls with dummy data,
preventing API call usage.
requests.exceptions is used to simulate
network errors that may arise.
from the file currency_utils.py,
we import convert_currency and get_exchange_rate.
Two test classes are formed, one for each of our
functions imported from currency_utils. """

import unittest
from unittest.mock import patch
import requests.exceptions
from currency_utils import convert_currency, get_exchange_rate

"""Creates test class, inheriting from unittest, that will test the
get_exchange_rate function from our currency_utils file.
It inherits from unittest.TestCase, which provides test runner features
and assertion methods."""

"""A decorator replacing the requests.get inside the currency_utils
   with a mock object."""


@patch("currency_utils.requests.get")
class TestGetExchangeRate(unittest.TestCase):

    # A test method, testing the successful API call outcome.
    # mock.get is the mock object, replacing the request.get of the original
    # function.
    # If successful, dictionary is returned.
    def test_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rate": 1.25,
        }
        mock_get.return_value.raise_for_status.return_value = None
        rate = get_exchange_rate("fake_api_key", "USD", "EUR")
        # Calls the real get_exchange_rate function with a
        # dummy API key and currencies,
        # but since requests.get is mocked, no real API call happens.
        self.assertEqual(rate, 1.25)

    # This tests a failure scenario, if failure condition is satisfied,
    # None is returned by the get_exchange_rate function.

    def test_api_error(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "error",
            "error-type": "invalid-key",
        }
        mock_get.return_value.raise_for_status.return_value = None
        rate = get_exchange_rate("fake_api_key", "USD", "EUR")
        self.assertIsNone(rate)

    def test_malformed_response(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "success"
            # Missing 'conversion_rate'
        }
        mock_get.return_value.raise_for_status.return_value = None
        rate = get_exchange_rate("fake_api_key", "USD", "EUR")
        self.assertIsNone(rate)

    def test_invalid_currency(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "error",
            "error-type": "invalid-from-currency",
        }
        mock_get.return_value.raise_for_status.return_value = None
        rate = get_exchange_rate("fake_api_key", "INVALID", "EUR")
        self.assertIsNone(rate)

    def test_network_error(self, mock_get):
        mock_get.side_effect = (
            requests.exceptions.RequestException("Network failure"))
        rate = get_exchange_rate("fake_api_key", "USD", "EUR")
        self.assertIsNone(rate)


@patch("currency_utils.get_exchange_rate")
class TestConvertCurrency(unittest.TestCase):

    def test_success(self, mock_get_rate):
        mock_get_rate.return_value = 2.0
        result = convert_currency("fake_api_key", 10, "USD", "EUR")
        self.assertEqual(result, 20.0)

    def test_zero_amount(self, mock_get_rate):
        mock_get_rate.return_value = 1.5
        result = convert_currency("fake_api_key", 0, "USD", "EUR")
        self.assertEqual(result, 0)

    def test_negative_amount(self, mock_get_rate):
        mock_get_rate.return_value = 1.5
        result = convert_currency("fake_api_key", -100, "USD", "EUR")
        self.assertEqual(result, -150)

    # Used to test excessively large numbers entered,
    # as part of boundary testing.
    def test_large_amount(self, mock_get_rate):
        mock_get_rate.return_value = 1.2
        large_amount = 10 ** 9
        result = convert_currency("fake_api_key", large_amount, "USD", "EUR")
        self.assertEqual(result, large_amount * 1.2)

    def test_none_exchange_rate(self, mock_get_rate):
        # Mocks the .raise_for_status() method
        # so it does nothing (simulating HTTP 200 OK with no error).
        mock_get_rate.return_value = None
        result = convert_currency("fake_api_key", 100, "USD", "EUR")
        self.assertIsNone(result)

    def test_nan_exchange_rate(self, mock_get_rate):
        mock_get_rate.return_value = float("nan")
        result = convert_currency("fake_api_key", 50, "USD", "EUR")
        self.assertTrue(result != result)  # NaN != NaN

    def test_infinite_exchange_rate(self, mock_get_rate):
        mock_get_rate.return_value = float("inf")
        result = convert_currency("fake_api_key", 50, "USD", "EUR")
        self.assertEqual(result, float("inf"))

    def test_amount_as_string(self, mock_get_rate):
        mock_get_rate.return_value = 1.0
        with self.assertRaises(TypeError):
            convert_currency("fake_api_key", "100", "USD", "EUR")

    def test_none_amount(self, mock_get_rate):
        mock_get_rate.return_value = 1.0
        with self.assertRaises(TypeError):
            convert_currency("fake_api_key", None, "USD", "EUR")


if __name__ == "__main__":
    unittest.main(verbosity=2)
