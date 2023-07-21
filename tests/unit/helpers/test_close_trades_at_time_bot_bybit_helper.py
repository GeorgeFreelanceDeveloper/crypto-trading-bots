import unittest
from unittest.mock import MagicMock

from trading_bots import constants
from trading_bots.helpers.close_trades_at_time_bot_bybit_helper import CloseTradesAtTimeBotBybitHelper


class TestCloseTradesAtTimeBotBybitHelper(unittest.TestCase):

    def setUp(self):
        # Initialize the CloseTradesAtTimeBotBybitHelper object for testing
        self.pybit_client = MagicMock()
        self.helper = CloseTradesAtTimeBotBybitHelper(self.pybit_client)

    def test_close_all_open_positions_and_pending_orders(self):
        # Create a mock response from the pybit_client for the get_positions call
        response = {
            "result": {
                "list": [
                    {
                        "symbol": "BTCUSD",
                        "side": "Buy",
                        "size": 1.0,
                        "positionIdx": "123"
                    }
                ]
            }
        }
        self.pybit_client.get_positions.return_value = response

        # Test the method
        self.helper.close_all_open_positions_and_pending_orders()

        # Verify that the pybit_client methods were called with the expected arguments
        self.pybit_client.place_order.assert_called_with(
            category=constants.BYBIT_LINEAR_CATEGORY,
            symbol="BTCUSD",
            orderType="Market",
            side="Sell",
            qty=1.0,
            positionIdx="123",
            reduceOnly=True
        )

        self.pybit_client.cancel_all_orders.assert_called_once_with(
            category="linear",
            settleCoin="USDT"
        )

    def tearDown(self):
        # Clean up after the tests
        pass


if __name__ == "__main__":
    unittest.main()
