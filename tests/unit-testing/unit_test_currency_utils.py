import unittest
from unittest.mock import patch

from currency_utils import convert_currency, get_exchange_rate

"""Different values are used across the different unit tests.
This was purposefully implemented, to avoid false positives
"""


class TestCurrencyUtils(unittest.TestCase):
    # SUCCESS case
    @patch("currency_utils.requests.get")
    def test_get_exchange_rate_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rate": 1.25,
        }
        rate = get_exchange_rate("fake_api_key", "USD", "EUR")
        self.assertEqual(rate, 1.25)

    # FAILURE case with known API error
    @patch("currency_utils.requests.get")
    def test_get_exchange_rate_failure(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "error",
            "error-type": "invalid-key",
        }
        with self.assertRaises(ValueError) as context:
            get_exchange_rate("fake_api_key", "USD", "EUR")
        self.assertIn("invalid-key", str(context.exception))

    # FAILURE case: malformed JSON response
    @patch("currency_utils.requests.get")
    def test_get_exchange_rate_malformed_response(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "success"
            # missing conversion_rate key
        }
        with self.assertRaises(KeyError):
            get_exchange_rate("fake_api_key", "USD", "EUR")

    # FAILURE case: invalid from-currency
    @patch("currency_utils.requests.get")
    def test_get_exchange_rate_invalid_currency(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "error",
            "error-type": "invalid-from-currency",
        }
        with self.assertRaises(ValueError) as context:
            get_exchange_rate("fake_api_key", "INVALID", "EUR")
        self.assertIn("invalid-from-currency", str(context.exception))

    # FAILURE case: network error (e.g., timeout)
    @patch("currency_utils.requests.get")
    def test_get_exchange_rate_network_error(self, mock_get):
        mock_get.side_effect = Exception("Network failure")
        with self.assertRaises(Exception) as context:
            get_exchange_rate("fake_api_key", "USD", "EUR")
        self.assertIn("Network failure", str(context.exception))

    # Basic convert_currency test with mocked exchange rate
    @patch("currency_utils.get_exchange_rate")
    def test_convert_currency(self, mock_get_rate):
        mock_get_rate.return_value = 2.0
        converted = convert_currency("fake_api_key", 10, "USD", "EUR")
        self.assertEqual(converted, 20)

    # Edge case: amount is zero
    @patch("currency_utils.get_exchange_rate")
    def test_convert_currency_zero_amount(self, mock_get_rate):
        mock_get_rate.return_value = 1.5
        converted = convert_currency("fake_api_key", 0, "USD", "EUR")
        self.assertEqual(converted, 0)

    # Edge case: amount is negative
    @patch("currency_utils.get_exchange_rate")
    def test_convert_currency_negative_amount(self, mock_get_rate):
        mock_get_rate.return_value = 1.5
        converted = convert_currency("fake_api_key", -100, "USD", "EUR")
        self.assertEqual(converted, -150)

    # Edge case: very large amount
    @patch("currency_utils.get_exchange_rate")
    def test_convert_currency_large_amount(self, mock_get_rate):
        mock_get_rate.return_value = 1.2
        large_amount = 10**9
        converted = convert_currency("fake_api_key", large_amount, "USD", "EUR")
        self.assertEqual(converted, large_amount * 1.2)


if __name__ == "__main__":
    # Here, all unit tests will be executed as soon as the program is.
    unittest.main()
