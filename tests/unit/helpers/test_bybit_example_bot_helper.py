import unittest
from unittest.mock import Mock

from trading_bots.helpers.bybit_example_bot_helper import BybitExampleBotHelper


class BybitExampleBotHelperTest(unittest.TestCase):

    def setUp(self) -> None:
        exchange_mock = self.create_exchange_mock()
        self.helper = BybitExampleBotHelper(exchange_mock)

    def test_get_btc_current_price(self):
        expected_result = 30050
        actual_result = self.helper.get_btc_current_price()

        self.assertEqual(expected_result, actual_result)

    @staticmethod
    def create_exchange_mock():
        exchange = Mock()
        exchange.get_orderbook.return_value = {"result": {"a": [[30000]], "b": [[30100]]}}
        return exchange
