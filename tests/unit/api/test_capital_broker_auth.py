import unittest
from unittest.mock import patch, MagicMock

from trading_bots.api.capital_broker_auth import CapitalBrokerAuth


class TestCapitalBrokerAuth(unittest.TestCase):

    @patch('http.client.HTTPSConnection')
    def test_get_new_authorization_token_success(self, mock_https_connection):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"currentAccountId": 123, "accounts": [{"accountId": 123, "accountName": "SubAccount"}]}'
        mock_response.getheader.side_effect = lambda header: "MockHeader"
        mock_https_connection.return_value.getresponse.return_value = mock_response

        auth = CapitalBrokerAuth("example.com", "username", "password", "api_key", "SubAccount", 30)
        authorization_token = auth.get_authorization_token()

        self.assertEqual(authorization_token["X-SECURITY-TOKEN"], "MockHeader")
        self.assertEqual(authorization_token["CST"], "MockHeader")
        self.assertEqual(auth._cached_token, authorization_token)

    @patch('http.client.HTTPSConnection')
    def test_get_new_authorization_token_http_error(self, mock_https_connection):
        mock_response = MagicMock()
        mock_response.status = 400
        mock_response.reason = "Bad Request"
        mock_https_connection.return_value.getresponse.return_value = mock_response

        auth = CapitalBrokerAuth("example.com", "username", "password", "api_key", "SubAccount", 30)

        with self.assertRaises(SystemExit) as cm:
            auth.get_authorization_token()

        self.assertEqual(cm.exception.code, -1)

    @patch('http.client.HTTPSConnection')
    def test_switch_to_sub_account_success(self, mock_https_connection):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{}'
        mock_https_connection.return_value.getresponse.return_value = mock_response

        auth = CapitalBrokerAuth("example.com", "username", "password", "api_key", "SubAccount", 30)
        auth._cached_token = {
            "X-SECURITY-TOKEN": "MockHeader",
            "CST": "MockHeader"
        }
        auth._switch_to_sub_account(123, auth._cached_token)

        self.assertTrue(mock_https_connection.called)
        self.assertEqual(mock_https_connection.return_value.request.call_args[0][0], "PUT")
        self.assertEqual(mock_https_connection.return_value.request.call_args[0][1], "/api/v1/session")

    @patch('http.client.HTTPSConnection')
    def test_switch_to_sub_account_http_error(self, mock_https_connection):
        mock_response = MagicMock()
        mock_response.status = 400
        mock_response.reason = "Bad Request"
        mock_https_connection.return_value.getresponse.return_value = mock_response

        auth = CapitalBrokerAuth("example.com", "username", "password", "api_key", "SubAccount", 30)
        auth._cached_token = {
            "X-SECURITY-TOKEN": "MockHeader",
            "CST": "MockHeader"
        }

        with self.assertRaises(SystemExit) as cm:
            auth._switch_to_sub_account(123, auth._cached_token)

        self.assertEqual(cm.exception.code, -1)


if __name__ == '__main__':
    unittest.main()
