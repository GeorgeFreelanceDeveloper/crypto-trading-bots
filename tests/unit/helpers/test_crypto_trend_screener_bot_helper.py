import unittest
import os
from unittest.mock import MagicMock

import pandas as pd
from trading_bots import constants
from trading_bots.helpers.crypto_trend_screener_bot_helper import CryptoTrendScreenerBotHelper


class TestCryptoTrendScreenerBotHelper(unittest.TestCase):

    def setUp(self):
        # Initialize the CryptoTrendScreenerBotHelper object for testing
        self.pybit_client = MagicMock()
        self.helper = CryptoTrendScreenerBotHelper(self.pybit_client)

    def test_get_pybit_futures_tickers(self):
        # Create a mock response from the pybit_client for the get_instruments_info call
        response = {
            "result": {
                "list": [
                    {"symbol": "BTCUSDT"},
                    {"symbol": "ETHUSDT"},
                    {"symbol": "XRPUSDT"}
                ]
            }
        }
        self.pybit_client.get_instruments_info.return_value = response

        # Test the method
        result = self.helper.get_pybit_futures_tickers()

        # Verify that the pybit_client method was called
        self.pybit_client.get_instruments_info.assert_called_once_with(category=constants.BYBIT_LINEAR_CATEGORY)

        # Verify the result
        expected_result = ["BTCUSDT", "ETHUSDT", "XRPUSDT"]
        self.assertEqual(result, expected_result)

    def test_get_ohlc(self):
        # Create a mock response from the pybit_client for the get_kline call
        response = {
            "result": {
                "list": [
                    {"startTime": 1625827200000, "open": "32000", "high": "33000", "low": "31000", "close": "31500",
                     "volume": "1000", "turnover": "30000000"},
                    {"startTime": 1625913600000, "open": "31500", "high": "32500", "low": "31000", "close": "32000",
                     "volume": "2000", "turnover": "60000000"}
                ]
            }
        }
        self.pybit_client.get_kline.return_value = response

        # Test the method
        result = self.helper.get_ohlc("BTCUSDT", "1d")

        # Verify that the pybit_client method was called
        self.pybit_client.get_kline.assert_called_once_with(
            category=constants.BYBIT_LINEAR_CATEGORY,
            symbol="BTCUSDT",
            interval="1d"
        )

        # Verify the result
        expected_result = pd.DataFrame({
            "startTime": [pd.Timestamp(1625827200000, unit="ms"), pd.Timestamp(1625913600000, unit="ms")],
            "open": [32000, 31500],
            "high": [33000, 32500],
            "low": [31000, 31000],
            "close": [31500, 32000],
            "volume": [1000, 2000],
            "turnover": [30000000, 60000000]
        })
        pd.testing.assert_frame_equal(result, expected_result)

    def test_create_tw_report(self):
        trends = pd.DataFrame({
            "ticker": ["BTCUSDT", "ETHUSDT", "XRPUSDT"],
            "context": ["Up-trend", "Start rotation after up-trend", "Down-trend"]
        })

        # Test the method
        result = self.helper.create_tw_report(trends)

        # Verify the result

        expected_result = "###UP-TREND,BTCUSDT,###START ROTATION AFTER UP-TREND,ETHUSDT,###DOWN-TREND,XRPUSDT,###START ROTATION AFTER DOWN-TREND,###ROTATION"
        self.assertEqual(result, expected_result)

    def test_save_tw_report(self):
        report = "###UP-TREND,BTCUSDT,###START ROTATION AFTER UP-TREND,ETHUSDT,###DOWN-TREND,XRPUSDT,###ROTATION"
        file_path = "reports/report.txt"

        # Test the method
        self.helper.save_tw_report(report, file_path)

        # Verify that the file was written
        with open(file_path, "r") as file:
            saved_report = file.read()
        self.assertEqual(saved_report, report)

        # Clean up the created file
        os.remove(file_path)


if __name__ == '__main__':
    unittest.main()
