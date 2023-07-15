import http
import json
import logging

from trading_bots.api.capital_broker_auth import CapitalBrokerAuth


class CapitalBrokerClient:

    def __init__(self, url: str, username: str, password: str, api_key: str, sub_account_name: str,
                 token_expire_minutes: int):
        self.url = url
        self.username = username
        self.password = password
        self.api_key = api_key
        self.sub_account_name = sub_account_name
        self.token_expire_minutes = token_expire_minutes
        self.auth = CapitalBrokerAuth(url, username, password, api_key, sub_account_name, token_expire_minutes)

    def get_market_info(self, ticker: str):
        try:
            logging.debug("Get market info")

            authorization_token = self.auth.get_authorization_token()

            conn = http.client.HTTPSConnection(self.url)
            payload = ''
            headers = {
                'X-SECURITY-TOKEN': authorization_token["X-SECURITY-TOKEN"],
                'CST': authorization_token["CST"]
            }
            conn.request("GET", f"/api/v1/markets?&epics={ticker}", payload, headers)
            res = conn.getresponse()

            if res.status != 200:
                raise Exception(f"HTTP Error {res.status}: {res.reason}")

            response = res.read().decode("utf-8")

            logging.debug(f"Response get_market_info: {response}")

            market_details = json.loads(response)["marketDetails"]

            return market_details[0]
        except Exception as e:
            raise Exception(f"Failed call GET method /api/v1/markets on capital.com REST api: {str(e)}")

    def get_last_closed_bar(self, ticker: str, time_frame: str = "MINUTE") -> dict:
        try:
            logging.debug("Get last closed bar")

            authorization_token = self.auth.get_authorization_token()
            conn = http.client.HTTPSConnection(self.url)
            payload = ''
            headers = {
                'X-SECURITY-TOKEN': authorization_token["X-SECURITY-TOKEN"],
                'CST': authorization_token["CST"]
            }

            conn.request("GET",
                         f"/api/v1/prices/{ticker}?resolution={time_frame}",
                         payload, headers)

            res = conn.getresponse()
            if res.status != 200:
                raise Exception(f"HTTP Error {res.status}: {res.reason}")

            data = json.loads(res.read().decode("utf-8"))

            last_bar_raw = data["prices"][-1]

            last_bar = {
                "snapshotTime": last_bar_raw["snapshotTime"],
                "openPrice": last_bar_raw["openPrice"]["bid"],
                "highPrice": last_bar_raw["highPrice"]["bid"],
                "lowPrice": last_bar_raw["lowPrice"]["bid"],
                "closePrice": last_bar_raw["closePrice"]["bid"]
            }

            return last_bar

        except Exception as e:
            raise Exception(f"Failed call GET method /api/v1/prices on capital.com REST api: {str(e)}")

    def get_positions(self):
        try:
            logging.debug("Get positions")
            authorization_token = self.auth.get_authorization_token()
            conn = http.client.HTTPSConnection(self.url)
            payload = ''
            headers = {
                'X-SECURITY-TOKEN': authorization_token["X-SECURITY-TOKEN"],
                'CST': authorization_token["CST"]
            }
            conn.request("GET", "/api/v1/positions", payload, headers)
            res = conn.getresponse()

            data = json.loads(res.read().decode("utf-8"))

            logging.debug(f"Response is_open_positions: {data}")

            if res.status != 200:
                raise Exception(f"HTTP Error {res.status}: {res.reason}")

            return data
        except Exception as e:
            raise Exception(
                f"Failed call GET method /api/v1/positions on api-capital.backend-capital.com REST api: {str(e)}")

    def place_trade(self, trade: dict):
        try:
            logging.debug("Place trade")
            authorization_token = self.auth.get_authorization_token()
            conn = http.client.HTTPSConnection(self.url)
            logging.debug(f"Trade: {trade}")

            payload = json.dumps({
                "epic": trade["ticker"],
                "direction": trade["direction"],
                "size": trade["amount"],
                "guaranteedStop": trade["guaranteedStop"],
                "stopDistance": trade["stopDistance"],
                "trailingStop": trade["trailingStop"],
                "profitLevel": trade["profitLevel"]
            })

            logging.debug(f"Payload place_trade: {payload}")
            headers = {
                'X-SECURITY-TOKEN': authorization_token["X-SECURITY-TOKEN"],
                'CST': authorization_token["CST"],
                'Content-Type': 'application/json'
            }

            conn.request("POST", "/api/v1/positions", payload, headers)
            res = conn.getresponse()

            logging.debug(f"Response place_trade: {res.read().decode('utf-8')}")
            if res.status != 200:
                raise Exception(f"HTTP Error {res.status}: {res.reason}")

        except Exception as e:
            raise Exception(
                f"Failed call POST method /api/v1/positions on api-capital.backend-capital.com REST api: {str(e)}")
