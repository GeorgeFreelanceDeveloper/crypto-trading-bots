import csv
import datetime
import http.client
import json
import logging
import sys
from datetime import datetime, time, timedelta
from io import StringIO

import requests

from trading_bots.helpers.equity_level_trade_bot_capital_auth_helper import EquityLevelTraderBotCapitalAuthHelper


class EquityLevelTraderBotCapitalHelper:

    def __init__(self, config: dict):
        self.alpha_vantage_api_key = config["alphavantageApiKey"]["apiKey"]
        self.capital_api_config = config["capitalApi"]
        self.percentage_before_entry = config["base"]["percentageBeforeEntry"]
        self.risk_per_trade_usd = config["base"]["riskPerTradeUsd"]
        self.auth_helper = EquityLevelTraderBotCapitalAuthHelper(config)

    def is_open_exchange(self) -> bool:
        now = datetime.now()
        return self._is_work_day(now) and self._is_time_between_range(now.time(), time(15, 30), time(22, 00))

    def is_open_positions(self) -> bool:
        try:
            logging.debug("Place trade")
            authorization_token = self.auth_helper.get_authorization_token()
            conn = http.client.HTTPSConnection(self.capital_api_config["url"])
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

            return len(data["positions"]) > 0
        except Exception as e:
            logging.error(
                f"Failed call GET method /api/v1/positions on api-capital.backend-capital.com REST api: {str(e)}")
            sys.exit(-1)

    def place_trade(self, order: dict):
        try:
            logging.debug("Place trade")
            authorization_token = self.auth_helper.get_authorization_token()
            conn = http.client.HTTPSConnection(self.capital_api_config["url"])
            logging.debug(order)

            move = float(order["entry_price"]) - float(order["stop_loss_price"])
            profit_target = float(order["entry_price"]) + move
            amount = round(abs(self.risk_per_trade_usd / move), self._get_round_rule(order["ticker"]))

            payload = json.dumps({
                "epic": order["ticker"],
                "direction": "BUY" if order["direction"] == "LONG" else "SELL",
                "size": amount,
                "guaranteedStop": False,
                "stopDistance": abs(move),
                "trailingStop": True,
                "profitLevel": profit_target
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

    def was_yesterday_earnings(self, ticker) -> bool:
        try:
            now = datetime.now().date()
            yesterday = now - timedelta(days=1)

            url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={self.alpha_vantage_api_key}"
            response = requests.get(url)

            if response.status_code != 200:
                raise Exception(f"HTTP Error {response.status_code}: {response.reason}")

            data = response.json()

            earnings_types = ["quarterlyEarnings", "annualEarnings"]
            earnings_date_names = ["reportedDate", "fiscalDateEnding"]

            for earnings_type, earnings_date_name in zip(earnings_types, earnings_date_names):
                earnings = data.get(earnings_type, [])
                last_earnings_date = datetime.strptime(earnings[0][earnings_date_name], "%Y-%m-%d").date()
                logging.debug(f"Last earnings date: {last_earnings_date}")
                if earnings and last_earnings_date == yesterday:
                    logging.debug(f"The last earnings result ({earnings_type}) was yesterday: {yesterday}")
                    return True

            return False

        except Exception as e:
            logging.error(f"Failed call GET method /query?function=EARNINGS on www.alphavantage.co REST api: {str(e)}")
            sys.exit(-1)

    def is_earnings_next_days(self, ticker: str, count_days: int = 10) -> bool:
        try:
            now = datetime.now().date()
            next_10_days = now + timedelta(days=count_days)
            horizon = "12month"

            url = f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol={ticker}&horizon={horizon}&apikey={self.alpha_vantage_api_key}"
            response = requests.get(url)

            if response.status_code != 200:
                raise Exception(f"HTTP Error {response.status_code}: {response.reason}")

            csv_data = response.text

            csv_reader = csv.DictReader(StringIO(csv_data))
            data = list(csv_reader)

            for row in data:
                report_date = row["reportDate"]
                report_date = datetime.strptime(report_date, "%Y-%m-%d").date()
                logging.debug(f"Next earnings date: {report_date}")
                if report_date <= next_10_days:
                    logging.debug(f"The future earnings {report_date} is in less then 10 days.")
                    return True

            return False
        except Exception as e:
            logging.error(
                f"Failed call GET method /query?function=EARNINGS_CALENDAR on www.alphavantage.co REST api: {str(e)}")
            sys.exit(-1)

    def check_price_reach_before_entry_price(self, order: dict) -> bool:
        entry_price = float(order["entry_price"])
        stop_loss = float(order["stop_loss_price"])
        order_side = order["direction"]

        before_entry_price = entry_price + ((entry_price - stop_loss) * self.percentage_before_entry)
        logging.debug(f"Before entry price: {before_entry_price}")

        last_closed_bar = self._get_last_closed_bar(order["ticker"])
        logging.debug(f"Last closed bar: {last_closed_bar}")

        return (order_side == "LONG" and before_entry_price >= last_closed_bar["lowPrice"]) or (
                order_side == "SHORT" and before_entry_price <= last_closed_bar["highPrice"])

    def is_price_at_entry_price(self, order: dict):
        entry_price = float(order["entry_price"])
        order_side = order["direction"]

        market_info = self._get_market_info(order["ticker"])

        bid = market_info["snapshot"]["bid"]
        ask = market_info["snapshot"]["offer"]

        return (order_side == "LONG" and ask < entry_price) or (
                order_side == "SHORT" and bid > entry_price
        )

    def check_price_reach_profit_target(self, order: dict) -> bool:
        entry_price = float(order["entry_price"])
        stop_loss = float(order["stop_loss_price"])
        order_side = order["direction"]

        move = entry_price - stop_loss
        take_profit = entry_price + move
        logging.debug(f"Take profit price: {take_profit}")

        last_closed_bar = self._get_last_closed_bar(order["ticker"])
        logging.debug(f"Last closed bar: {last_closed_bar}")

        return (order_side == "LONG" and take_profit <= last_closed_bar["highPrice"]) or (
                order_side == "SHORT" and take_profit >= last_closed_bar["lowPrice"])

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

    def _get_market_info(self, ticker: str):
        try:
            authorization_token = self.auth_helper.get_authorization_token()

            conn = http.client.HTTPSConnection(self.capital_api_config["url"])
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

            logging.debug(f"Response _get_market_info: {response}")

            market_details = json.loads(response)["marketDetails"]

            return market_details[0]
        except Exception as e:
            raise Exception(f"Failed call GET method /api/v1/markets on capital.com REST api: {str(e)}")

    def _get_round_rule(self, ticker):
        market_info = self._get_market_info(ticker)
        return 1 if market_info["dealingRules"]["minDealSize"]["value"] == 0.1 else 0
