"""
This script performs a live integration test for the `get_exchange_rate` function
using the Alpha Vantage API.

- `os` is used to access environment variables such as the API key.
- `unittest` is the standard Python framework for writing and executing tests.
- Because Alpha Vantage limits requests (5 per minute on the free tier),
  this test is conditionally executed to avoid accidental API overuse.
"""

import os
import unittest
from currency_utils import get_exchange_rate

"""
This test class inherits from `unittest.TestCase`, the base class for all test cases.
By naming the class with a `Test` prefix, it can be automatically discovered and run by the unittest framework.
"""
class TestCurrencyUtilsIntegration(unittest.TestCase):

    def test_live_get_exchange_rate(self):
        # Check if integration tests are enabled via an environment variable
        if os.getenv("RUN_INTEGRATION_TESTS") != "1":
            print("⚠️  Skipping integration test: Set RUN_INTEGRATION_TESTS=1 to enable.")
            self.skipTest("Integration test skipped. Set RUN_INTEGRATION_TESTS=1 to run.")

        # Check if the API key is set in the environment
        api_key = os.getenv("EXCHANGE_API_KEY")
        if not api_key:
            print("⚠️  Skipping test: Set EXCHANGE_API_KEY in environment to run this test.")
            self.skipTest("Missing API key.")

        # Perform the actual API call
        rate = get_exchange_rate(api_key, "USD", "EUR")

        # Assert that the returned rate is a float
        self.assertIsInstance(rate, float)

        # Assert that the exchange rate is a positive number (> 0)
        self.assertGreater(rate, 0)  # Exchange rates should logically be greater than zero

"""
As with unit tests, this integration test will automatically run 
when the script is executed directly — *if* conditions allow it.
"""
if __name__ == "__main__":
    unittest.main()
