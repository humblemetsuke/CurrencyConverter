import unittest
from unittest.mock import patch
import requests.exceptions
from currency_utils import convert_currency, get_exchange_rate


class TestCurrencyUtils(unittest.TestCase):

    @patch("currency_utils.requests.get")
    def test_get_exchange_rate_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rate": 1.25,
        }
        mock_get.return_value.raise_for_status.return_value = None
        rate = get_exchange_rate("fake_api_key", "USD", "EUR")
        self.assertEqual(rate, 1.25)

    @patch("currency_utils.requests.get")
    def test_get_exchange_rate_api_error(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "error",
            "error-type": "invalid-key",
        }
        mock_get.return_value.raise_for_status.return_value = None
        rate = get_exchange_rate("fake_api_key", "USD", "EUR")
        self.assertIsNone(rate)

    @patch("currency_utils.requests.get")
    def test_get_exchange_rate_malformed_response(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "success"
            # conversion_rate key is missing
        }
        mock_get.return_value.raise_for_status.return_value = None
        rate = get_exchange_rate("fake_api_key", "USD", "EUR")
        self.assertIsNone(rate)

    @patch("currency_utils.requests.get")
    def test_get_exchange_rate_invalid_currency(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "error",
            "error-type": "invalid-from-currency",
        }
        mock_get.return_value.raise_for_status.return_value = None
        rate = get_exchange_rate("fake_api_key", "INVALID", "EUR")
        self.assertIsNone(rate)

    @patch("currency_utils.requests.get")
    def test_get_exchange_rate_network_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network failure")
        rate = get_exchange_rate("fake_api_key", "USD", "EUR")
        self.assertIsNone(rate)

    @patch("currency_utils.get_exchange_rate")
    def test_convert_currency_success(self, mock_get_rate):
        mock_get_rate.return_value = 2.0
        result = convert_currency("fake_api_key", 10, "USD", "EUR")
        self.assertEqual(result, 20.0)

    @patch("currency_utils.get_exchange_rate")
    def test_convert_currency_zero_amount(self, mock_get_rate):
        mock_get_rate.return_value = 1.5
        result = convert_currency("fake_api_key", 0, "USD", "EUR")
        self.assertEqual(result, 0)

    @patch("currency_utils.get_exchange_rate")
    def test_convert_currency_negative_amount(self, mock_get_rate):
        mock_get_rate.return_value = 1.5
        result = convert_currency("fake_api_key", -100, "USD", "EUR")
        self.assertEqual(result, -150)

    @patch("currency_utils.get_exchange_rate")
    def test_convert_currency_large_amount(self, mock_get_rate):
        mock_get_rate.return_value = 1.2
        large_amount = 10**9
        result = convert_currency("fake_api_key", large_amount, "USD", "EUR")
        self.assertEqual(result, large_amount * 1.2)

    @patch("currency_utils.get_exchange_rate")
    def test_convert_currency_when_rate_none(self, mock_get_rate):
        mock_get_rate.return_value = None
        result = convert_currency("fake_api_key", 100, "USD", "EUR")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
