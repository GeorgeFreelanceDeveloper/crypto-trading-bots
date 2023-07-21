import unittest
from unittest.mock import patch, MagicMock

from trading_bots.helpers.equity_level_trader_bot_capital_helper import EquityLevelTraderBotCapitalHelper


class TestEquityLevelTraderBotCapitalHelper(unittest.TestCase):

    def setUp(self):
        self.config = {
            "capitalApi": {
                "url": "example.com",
                "username": "testuser",
                "password": "testpassword",
                "apiKey": "testapikey",
                "subAccountName": "TestAccount",
                "tokenExpireMinutes": 30
            },
            "base": {
                "riskPerTradeUsd": 100,
                "percentageBeforeEntry": 0.5
            }
        }

        self.earning_calendar = [
            {"symbol": "AAPL", "reportDate": "2023-07-01"},
            {"symbol": "GOOG", "reportDate": "2023-07-02"}
        ]

        self.earning_calendar_old = [
            {"symbol": "AAPL", "reportDate": "2023-06-01"},
            {"symbol": "GOOG", "reportDate": "2023-06-02"}
        ]

    @patch('trading_bots.api.capital_broker_client.CapitalBrokerClient')
    def test_is_open_exchange_returns_true(self, mock_capital_broker_client):
        helper = EquityLevelTraderBotCapitalHelper(config=self.config, earning_calendar=self.earning_calendar,
                                                   earning_calendar_old=self.earning_calendar_old)
        helper._is_work_day = MagicMock(return_value=True)
        helper._is_time_between_range = MagicMock(return_value=True)

        self.assertTrue(helper.is_open_exchange())

    @patch('trading_bots.api.capital_broker_client.CapitalBrokerClient')
    def test_is_open_exchange_returns_false_on_weekend(self, mock_capital_broker_client):
        helper = EquityLevelTraderBotCapitalHelper(config=self.config, earning_calendar=self.earning_calendar,
                                                   earning_calendar_old=self.earning_calendar_old)
        helper._is_work_day = MagicMock(return_value=False)
        helper._is_time_between_range = MagicMock(return_value=True)

        self.assertFalse(helper.is_open_exchange())

    @patch('trading_bots.api.capital_broker_client.CapitalBrokerClient')
    def test_is_open_exchange_returns_false_outside_time_range(self, mock_capital_broker_client):
        helper = EquityLevelTraderBotCapitalHelper(config=self.config, earning_calendar=self.earning_calendar,
                                                   earning_calendar_old=self.earning_calendar_old)
        helper._is_work_day = MagicMock(return_value=True)
        helper._is_time_between_range = MagicMock(return_value=False)

        self.assertFalse(helper.is_open_exchange())

    @patch('trading_bots.api.capital_broker_client.CapitalBrokerClient')
    def test_is_open_positions_returns_true(self, mock_capital_broker_client):
        mock_capital_broker_client.get_positions.return_value = [{"id": 1, "ticker": "AAPL"}]

        helper = EquityLevelTraderBotCapitalHelper(config=self.config, earning_calendar=self.earning_calendar,
                                                   earning_calendar_old=self.earning_calendar_old)
        helper.capital_broker_client = mock_capital_broker_client

        self.assertTrue(helper.is_open_positions())

    @patch('trading_bots.api.capital_broker_client.CapitalBrokerClient')
    def test_is_open_positions_returns_false(self, mock_capital_broker_client):
        mock_capital_broker_client.get_positions.return_value = []

        helper = EquityLevelTraderBotCapitalHelper(config=self.config, earning_calendar=self.earning_calendar,
                                                   earning_calendar_old=self.earning_calendar_old)
        helper.capital_broker_client = mock_capital_broker_client

        self.assertFalse(helper.is_open_positions())

    @patch('trading_bots.api.capital_broker_client.CapitalBrokerClient')
    def test_place_trade_calls_capital_broker_client(self, mock_capital_broker_client):
        mock_capital_broker_client.place_trade.return_value = MagicMock()

        helper = EquityLevelTraderBotCapitalHelper(config=self.config, earning_calendar=self.earning_calendar,
                                                   earning_calendar_old=self.earning_calendar_old)

        helper.capital_broker_client = mock_capital_broker_client
        order = {
            "ticker": "AAPL",
            "direction": "LONG",
            "entry_price": "150",
            "stop_loss_price": "140"
        }
        helper.place_trade(order)

        self.assertTrue(mock_capital_broker_client.place_trade.called)


if __name__ == '__main__':
    unittest.main()
