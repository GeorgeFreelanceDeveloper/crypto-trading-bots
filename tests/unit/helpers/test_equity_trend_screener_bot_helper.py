import os
import unittest
from unittest.mock import patch, MagicMock

import pandas as pd

from trading_bots.helpers.equity_trend_screener_bot_helper import EquityTrendScreenerBotHelper


class TestEquityTrendScreenerBotHelper(unittest.TestCase):

    def setUp(self) -> None:
        self.helper = EquityTrendScreenerBotHelper()

    @patch("trading_bots.helpers.equity_trend_screener_bot_helper.yf")
    def test_get_daily_ohlc(self, mock_yf):
        # Create test data
        test_data = pd.DataFrame({
            "Date": ["2022-01-01", "2022-01-02"],
            "Open": [100, 110],
            "High": [120, 130],
            "Low": [90, 100],
            "Close": [110, 120]
        })
        test_data.set_index("Date", inplace=True)

        # Create mock
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = test_data
        mock_yf.Ticker.return_value = mock_ticker

        # Test method get_daily_ohlc
        ticker = "NASDAQ:AAPL"
        ohlc = self.helper.get_daily_ohlc(ticker)
        expected_ohlc = pd.DataFrame({
            "startTime": ["2022-01-02", "2022-01-01"],
            "open": [110, 100],
            "high": [130, 120],
            "low": [100, 90],
            "close": [120, 110]
        })

        pd.testing.assert_frame_equal(ohlc, expected_ohlc)

    def test_save_tw_report(self):
        # Create test file for report
        test_file = "reports/test_report.txt"

        # Test method save_tw_report
        report = "Test report"
        self.helper.save_tw_report(report, test_file)

        # Test create file and file contains right data
        self.assertTrue(os.path.exists(test_file))
        with open(test_file, "r") as file:
            saved_report = file.read()
            self.assertEqual(saved_report, report)

        # Remove test file
        os.remove(test_file)

    def test_count_items_without_rotation(self):
        # Create test data
        test_data = pd.DataFrame({
            "ticker": ["NASDAQ:AAPL", "NASDAQ:GOOGL", "NASDAQ:TSLA"],
            "context": ["Up-trend", "Rotation", "N/A"]
        })

        # Test method count_items_without_rotation
        count = self.helper.count_items_without_rotation(test_data)
        expected_count = 2
        self.assertEqual(count, expected_count)


if __name__ == "__main__":
    unittest.main()
