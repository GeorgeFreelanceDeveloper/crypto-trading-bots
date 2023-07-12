import csv
import datetime
import http.client
import logging
import sys
from datetime import datetime, time, timedelta

import requests

from trading_bots.helpers.equity_level_trade_bot_capital_auth_helper import EquityLevelTraderBotCapitalAuthHelper


class EquityLevelTraderBotCapitalHelper:

    def __init__(self, config: dict):
        self.alpha_vantage_api_key = config["alphavantageApiKey"]["apiKey"]
        self.capital_api_config = config["capitalApi"]
        self.auth_helper = EquityLevelTraderBotCapitalAuthHelper(config)

    @staticmethod
    def load_orders(file_path):
        result = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                result.append(row)
        return result

    def is_open_exchange(self) -> bool:
        now = datetime.now()
        return self._is_work_day(now) and self._is_time_between_range(now.time(), time(15, 30), time(22, 00))

    def is_open_positions(self) -> bool:
        # TODO: @Lucka
        return False

    @staticmethod
    def place_trade(order: dict):
        # TODO: @Lucka
        pass

    def has_price_reached_entry(self, order: dict):
        last_bar = self._get_last_closed_bar(order["ticker"], "MINUTE")
        entry_price = order["entry_price"]

        if order["direction"] == "LONG" and last_bar["lowPrice"] <= entry_price:
            return True

        if order["direction"] == "SHORT" and last_bar["highPrice"] >= entry_price:
            return True

        return False

    def was_yesterday_earnings(self, ticker) -> bool:
        now = datetime.now().date()
        yesterday = now - timedelta(days=1)

        url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={self.alpha_vantage_api_key}"
        response = requests.get(url)
        data = response.json()

        earnings_types = ["quarterlyEarnings", "annualEarnings"]
        for earnings_type in earnings_types:
            earnings = data.get(earnings_type, [])
            if earnings and datetime.strptime(earnings[0]["reportedDate"], "%Y-%m-%d").date() == yesterday:
                logging.debug(f"The last earnings result ({earnings_type}) was yesterday: {yesterday}")
                return True
            else:
                return False

    @staticmethod
    def is_earnings_next_days(ticker: str, count_days: int = 10) -> bool:
        now = datetime.now().date()
        # TODO: Lucka
        return False

    @staticmethod
    def _is_work_day(date):
        return date.weekday() < 5

    @staticmethod
    def _is_time_between_range(actual_time: datetime.time, start_time: datetime.time, end_time: datetime.time) -> bool:
        return start_time <= actual_time <= end_time

    def _get_last_closed_bar(self, ticker: str, time_frame: str = "MINUTE") -> dict:
        try:
            logging.debug("Get last closed bar")

            authorization_token = self.auth_helper.get_authorization_token()
            conn = http.client.HTTPSConnection(self.capital_api_config["url"])
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

            data = res.read()
            return data["prices"][-1]
        except Exception as e:
            logging.error(f"Failed call GET method /api/v1/prices on capital.com REST api: {str(e)}")
            sys.exit(-1)
