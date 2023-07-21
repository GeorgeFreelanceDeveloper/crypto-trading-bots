import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock

from trading_bots.helpers.check_futures_margin_level_bot_bybit_helper import CheckFuturesMarginLevelBotBybitHelper


class TestCheckFuturesMarginLevelBotBybitHelper(unittest.TestCase):

    fixture_folder_path = "tests/unit/helpers/fixtures"
    # fixture_folder_path = "fixtures" # for run tests in ide

    def setUp(self):
        # Initialize the CheckFuturesMarginLevelBotBybitHelper object for testing
        self.pybit_client = MagicMock()
        self.funding_dates_json_path = f"{self.fixture_folder_path}/test_funding_dates.json"

        with open(self.funding_dates_json_path, "w") as file:
            file.write("[]")

        self.helper = CheckFuturesMarginLevelBotBybitHelper(self.pybit_client, self.funding_dates_json_path)

    def test_get_available_balance_on_futures_account(self):
        # Create a mock response from the pybit_client
        response = {
            "result": {
                "list": [
                    {
                        "coin": [
                            {
                                "walletBalance": "1000",
                                "availableToWithdraw": "800"
                            }
                        ]
                    }
                ]
            }
        }
        self.pybit_client.get_wallet_balance.return_value = response

        # Test the method
        result = self.helper.get_available_balance_on_futures_account()

        # Verify the result
        self.assertEqual(result, 1000.0)

    def test_is_open_positions(self):
        # Create a mock response from the pybit_client
        response = {
            "result": {
                "list": [
                    {
                        "positionId": "123"
                    }
                ]
            }
        }
        self.pybit_client.get_positions.return_value = response

        # Test the method
        result = self.helper.is_open_positions()

        # Verify the result
        self.assertTrue(result)

    def test_was_funding_account_today(self):
        # Set the last funding date to today
        self.helper.funding_dates = [datetime.now()]

        # Test the method
        result = self.helper.was_funding_account_today()

        # Verify the result
        self.assertTrue(result)

    def test_get_last_position_close_date(self):
        # Create a mock response from the pybit_client
        response = {
            "result": {
                "list": [
                    {
                        "updatedTime": 1624705200000  # Unix timestamp for June 26, 2021
                    }
                ]
            }
        }
        self.pybit_client.get_closed_pnl.return_value = response

        # Test the method
        result = self.helper.get_last_position_close_date()

        # Verify the result
        self.assertEqual(result.date(), datetime(2021, 6, 26).date())

    def test_funding_futures_account(self):
        # Create a mock response from the pybit_client
        response = {
            "retMsg": "success"
        }
        self.pybit_client.create_internal_transfer.return_value = response

        # Test the method
        self.helper.funding_futures_account(2000.0, 1500.0)

        # Verify that the pybit_client method was called with the expected arguments
        self.pybit_client.create_internal_transfer.assert_called_once_with(
            transferId=unittest.mock.ANY,
            coin="USDT",
            amount="500.1",
            fromAccountType="SPOT",
            toAccountType="CONTRACT"
        )

    def tearDown(self):
        # Clean up after the tests, e.g., deleting the test funding dates file
        if os.path.exists(self.funding_dates_json_path):
            os.remove(self.funding_dates_json_path)
