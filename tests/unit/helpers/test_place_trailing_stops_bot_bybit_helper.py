import unittest
from unittest.mock import MagicMock

import pandas as pd

from trading_bots.helpers.place_trailing_stops_bot_bybit_helper import PlaceTrailingStopsBotBybitHelper


class TestPlaceTrailingStopsBotBybitHelper(unittest.TestCase):

    def setUp(self):
        # Initialize the PlaceTrailingStopsBotBybitHelper object for testing
        self.pybit_client = MagicMock()
        self.helper = PlaceTrailingStopsBotBybitHelper(self.pybit_client)

    def test_calculate_trailing_stops(self):
        # Create a sample positions DataFrame
        positions_data = {
            "symbol": ["BTCUSDT", "ETHUSDT"],
            "avgPrice": [40000, 3000],
            "stopLoss": [39000, 2900]
        }
        positions = pd.DataFrame(positions_data)

        # Test the method
        self.helper.calculate_trailing_stops(positions)

        # Verify the computed trailing stop values
        expected_result = pd.DataFrame({
            "symbol": ["BTCUSDT", "ETHUSDT"],
            "avgPrice": [40000, 3000],
            "stopLoss": [39000, 2900],
            "priceScale": [2, 2],
            "isSetStopLoss": [True, True],
            "computeTrailingStop": [1000, 100]
        })
        pd.testing.assert_frame_equal(positions, expected_result)

    def test_place_trailing_stops(self):
        # Create a sample positions DataFrame
        positions_data = {
            "symbol": ["BTCUSDT", "ETHUSDT"],
            "side": ["Buy", "Sell"],
            "isSetStopLoss": [True, True],
            "trailingStop": [0, 0],
            "computeTrailingStop": [1000, 100],
            "positionIdx": [0, 0]
        }
        positions = pd.DataFrame(positions_data)

        # Test the method
        self.helper.place_trailing_stops(positions)

        # Verify the mock calls
        self.pybit_client.set_trading_stop.assert_called()

    def test_get_price_scale(self):
        # Mock the instruments_info data
        self.helper.instruments_info = [
            {"symbol": "BTCUSDT", "priceScale": 2},
            {"symbol": "ETHUSDT", "priceScale": 3}
        ]

        # Test the method
        result1 = self.helper._get_price_scale("BTCUSDT")
        result2 = self.helper._get_price_scale("ETHUSDT")
        result3 = self.helper._get_price_scale("DOGEUSDT")  # Non-existent ticker

        # Verify the results
        self.assertEqual(result1, 2)
        self.assertEqual(result2, 3)
        self.assertEqual(result3, 2)  # Default price scale

    def test_is_active_trailing_stop(self):
        # Create a sample position Series
        position_data = {
            "trailingStop": "100"
        }
        position = pd.Series(position_data)

        # Test the method
        result1 = self.helper._is_active_trailing_stop(position)

        # Verify the result
        self.assertTrue(result1)


if __name__ == '__main__':
    unittest.main()
