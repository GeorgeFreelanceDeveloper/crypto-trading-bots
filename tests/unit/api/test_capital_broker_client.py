import unittest
from unittest.mock import patch, MagicMock

from trading_bots.api.capital_broker_client import CapitalBrokerClient


class TestCapitalBrokerClient(unittest.TestCase):

    @patch('http.client.HTTPSConnection')
    def test_get_market_info_success(self, mock_https_connection):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"marketDetails": [{"name": "Market"}]}'
        mock_https_connection.return_value.getresponse.return_value = mock_response

        client = CapitalBrokerClient("example.com", "username", "password", "api_key", "SubAccount", 30)

        with patch.object(client.auth, 'get_authorization_token',
                          return_value={"X-SECURITY-TOKEN": "MockHeader", "CST": "MockHeader"}):
            market_info = client.get_market_info("TSLA")

        self.assertEqual(market_info["name"], "Market")

    @patch('http.client.HTTPSConnection')
    def test_get_last_closed_bar_success(self, mock_https_connection):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"prices": [{"snapshotTime": "2023-07-01", "openPrice": {"bid": 100}, "highPrice": {"bid": 200}, "lowPrice": {"bid": 50}, "closePrice": {"bid": 150}}]}'
        mock_https_connection.return_value.getresponse.return_value = mock_response

        client = CapitalBrokerClient("example.com", "username", "password", "api_key", "SubAccount", 30)

        with patch.object(client.auth, 'get_authorization_token',
                          return_value={"X-SECURITY-TOKEN": "MockHeader", "CST": "MockHeader"}):
            last_bar = client.get_last_closed_bar("TSLA")

        self.assertEqual(last_bar["snapshotTime"], "2023-07-01")
        self.assertEqual(last_bar["openPrice"], 100)
        self.assertEqual(last_bar["highPrice"], 200)
        self.assertEqual(last_bar["lowPrice"], 50)
        self.assertEqual(last_bar["closePrice"], 150)

    @patch('http.client.HTTPSConnection')
    def test_get_positions_success(self, mock_https_connection):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"positions": [{"id": 1, "ticker": "TSLA"}]}'
        mock_https_connection.return_value.getresponse.return_value = mock_response

        client = CapitalBrokerClient("example.com", "username", "password", "api_key", "SubAccount", 30)

        with patch.object(client.auth, 'get_authorization_token',
                          return_value={"X-SECURITY-TOKEN": "MockHeader", "CST": "MockHeader"}):
            positions = client.get_positions()

        self.assertEqual(positions[0]["id"], 1)
        self.assertEqual(positions[0]["ticker"], "TSLA")

    @patch('http.client.HTTPSConnection')
    def test_place_trade_success(self, mock_https_connection):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_https_connection.return_value.getresponse.return_value = mock_response

        client = CapitalBrokerClient("example.com", "username", "password", "api_key", "SubAccount", 30)

        with patch.object(client.auth, 'get_authorization_token',
                          return_value={"X-SECURITY-TOKEN": "MockHeader", "CST": "MockHeader"}):
            trade = {
                "ticker": "TSLA",
                "direction": "BUY",
                "size": 1,
                "guaranteedStop": False,
                "stopDistance": 10,
                "trailingStop": False,
                "profitLevel": 100
            }
            client.place_trade(trade)

        self.assertTrue(mock_https_connection.called)
        self.assertEqual(mock_https_connection.return_value.request.call_args[0][0], "POST")
        self.assertEqual(mock_https_connection.return_value.request.call_args[0][1], "/api/v1/positions")
        self.assertEqual(mock_https_connection.return_value.request.call_args[0][2],
                         '{"epic": "TSLA", "direction": "BUY", "size": 1, "guaranteedStop": false, "stopDistance": 10, "trailingStop": false, "profitLevel": 100}')
        self.assertEqual(mock_https_connection.return_value.request.call_args[0][3]['X-SECURITY-TOKEN'], 'MockHeader')
        self.assertEqual(mock_https_connection.return_value.request.call_args[0][3]['CST'], 'MockHeader')


if __name__ == '__main__':
    unittest.main()
