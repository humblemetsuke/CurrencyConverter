"""
Live integration test for the `get_exchange_rate` function using the Alpha Vantage API.

- Avoids hitting the API unless explicitly enabled via environment variable.
- Verifies return type and positive value of the exchange rate.
"""

import os
import unittest

from currency_utils import get_exchange_rate


class TestCurrencyUtilsIntegration(unittest.TestCase):
    def test_live_get_exchange_rate(self):
        if os.getenv("RUN_INTEGRATION_TESTS") != "1":
            self.skipTest("Set RUN_INTEGRATION_TESTS=1 to enable integration tests.")

        api_key = os.getenv("EXCHANGE_API_KEY")
        if not api_key:
            self.skipTest("Missing API key: Set EXCHANGE_API_KEY in environment.")

        rate = get_exchange_rate(api_key, "USD", "EUR")

        # Validate the API returned a usable value
        self.assertIsInstance(rate, float, "Exchange rate should be a float.")
        self.assertGreater(rate, 0, "Exchange rate should be greater than 0.")


if __name__ == "__main__":
    unittest.main()
