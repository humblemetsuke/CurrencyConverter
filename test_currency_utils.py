import unittest
from unittest.mock import patch
from currency_utils import get_exchange_rate, convert_currency
"""@patch('currency_utils.requests.get') is a decorator.
Decorators are commonly used to temporarily replace the contents of the 
requests.get function inside the currency_utils module with a mock object.
Why? requests.get is external, slow and can be costly, esp. given if API calls are limited.
By substituting fake calls in lieu of the original we avoid these issues.
 mock_get is a mock object of the requests.get.
configure the mock so that when .json() is called on the response, it returns this fake JSON 
representing a successful API call with a conversion rate of 1.25.        
The assertions are used to test for both success and failure scenarios.

"""

class TestCurrencyUtils(unittest.TestCase):

    @patch('currency_utils.requests.get')



    def test_get_exchange_rate_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rate": 1.25
        }



        rate = get_exchange_rate("fake_api_key", "USD", "EUR")
        #Here we are invoking a real function (the get_exchange_rate) with the mock data contained in the JSON.
        #This avoids the incurring of a real API call.
        self.assertEqual(rate, 1.25)
        #if the rate is not equal to 1.25 the test will fail.


    #Here, we are now mocking the scenario where we have a failed API call.
    # As with the above function, we are using mock data to achieve this outcome.
    @patch('currency_utils.requests.get')
    def test_get_exchange_rate_failure(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": "error",
            "error-type": "invalid-key"
        }
        #If the API call does result in a fail, we expect that None will be returned.
        #The assertion is then included in order to validate if this is True.
        with self.assertRaises(ValueError) as context:
            get_exchange_rate("fake_api_key", "USD", "EUR")
        self.assertIn("invalid-key", str(context.exception))

    @patch('currency_utils.get_exchange_rate')
    def test_convert_currency(self, mock_get_rate):
        mock_get_rate.return_value = 2.0
        converted = convert_currency("fake_api_key", 10, "USD", "EUR")
        self.assertEqual(converted, 20)

if __name__ == '__main__':
    unittest.main()
