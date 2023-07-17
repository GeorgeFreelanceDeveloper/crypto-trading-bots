import datetime
import logging
import sys
from datetime import datetime, time, timedelta

from trading_bots.api.capital_broker_client import CapitalBrokerClient


class EquityLevelTraderBotCapitalHelper:

    def __init__(self, config: dict, earning_calendar: list, earning_calendar_old: list):
        self.capital_broker_client = CapitalBrokerClient(
            url=config["capitalApi"]["url"],
            username=config["capitalApi"]["username"],
            password=config["capitalApi"]["password"],
            api_key=config["capitalApi"]["apiKey"],
            sub_account_name=config["capitalApi"]["subAccountName"],
            token_expire_minutes=config["capitalApi"]["tokenExpireMinutes"]
        )
        self.earnings_calendar = earning_calendar
        self.earnings_calendar_old = earning_calendar_old
        self.risk_per_trade_usd = config["base"]["riskPerTradeUsd"]
        self.percentage_before_entry = config["base"]["percentageBeforeEntry"]

    def is_open_exchange(self) -> bool:
        now = datetime.now()
        return self._is_work_day(now) and self._is_time_between_range(now.time(), time(15, 30), time(22, 00))

    def is_open_positions(self) -> bool:
        try:
            positions = self.capital_broker_client.get_positions()
            logging.debug(f"Response getPositions: {positions}")
            return len(positions) > 0
        except Exception as e:
            logging.error(f"Failed call get_positions on CapitalBrokerClient: {str(e)}")
            sys.exit(-1)

    def place_trade(self, order: dict):
        try:
            move = float(order["entry_price"]) - float(order["stop_loss_price"])
            trade = {
                "ticker": order["ticker"],
                "direction": "BUY" if order["direction"] == "LONG" else "SELL",
                "size": round(abs(self.risk_per_trade_usd / move), self._get_round_rule(order["ticker"])),
                "guaranteedStop": False,
                "stopDistance": abs(move),
                "trailingStop": True,
                "profitLevel": float(order["entry_price"]) + move
            }
            logging.debug(f"Place trade: {trade}")
            self.capital_broker_client.place_trade(trade)
        except Exception as e:
            raise Exception(f"Failed call place_trade on CapitalBrokerClient: {str(e)}")

    def was_yesterday_earnings(self, ticker: str) -> bool:
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        next_earning_date = self.get_next_earnings_date(ticker, old=True)
        return next_earning_date == yesterday

    def is_earnings_next_days(self, ticker: str, count_days: int = 10) -> bool:
        today = datetime.now().date()
        next_n_days = today + timedelta(days=count_days)
        next_earning_date = self.get_next_earnings_date(ticker)
        return next_earning_date <= next_n_days

    def get_next_earnings_date(self, ticker: str, old: bool = False):
        earnings_calendar = self.earnings_calendar if not old else self.earnings_calendar_old
        next_earnings_date = [x["reportDate"] for x in earnings_calendar if x["symbol"] == ticker]
        return next_earnings_date[0] if next_earnings_date else None

    def check_price_reach_before_entry_price(self, order: dict) -> bool:
        entry_price = float(order["entry_price"])
        stop_loss = float(order["stop_loss_price"])
        order_side = order["direction"]

        before_entry_price = entry_price + ((entry_price - stop_loss) * self.percentage_before_entry)
        logging.debug(f"Before entry price: {before_entry_price}")

        last_closed_bar = self.capital_broker_client.get_last_closed_bar(order["ticker"])
        logging.debug(f"Last closed bar: {last_closed_bar}")

        return (order_side == "LONG" and before_entry_price >= last_closed_bar["lowPrice"]) or (
                order_side == "SHORT" and before_entry_price <= last_closed_bar["highPrice"])

    def is_price_at_entry_price(self, order: dict):
        entry_price = float(order["entry_price"])
        stop_loss_price = float(order["stop_loss_price"])
        order_side = order["direction"]

        market_info = self.capital_broker_client.get_market_info(order["ticker"])

        bid = market_info["snapshot"]["bid"]
        ask = market_info["snapshot"]["offer"]

        return (order_side == "LONG" and entry_price > ask > stop_loss_price) or (
                    order_side == "SHORT" and entry_price < bid < stop_loss_price)

    def check_price_reach_profit_target(self, order: dict) -> bool:
        entry_price = float(order["entry_price"])
        stop_loss = float(order["stop_loss_price"])
        order_side = order["direction"]

        move = entry_price - stop_loss
        take_profit = entry_price + move
        logging.debug(f"Take profit price: {take_profit}")

        last_closed_bar = self.capital_broker_client.get_last_closed_bar(order["ticker"])
        logging.debug(f"Last closed bar: {last_closed_bar}")

        return (order_side == "LONG" and take_profit <= last_closed_bar["highPrice"]) or (
                order_side == "SHORT" and take_profit >= last_closed_bar["lowPrice"])

    @staticmethod
    def _is_work_day(date):
        return date.weekday() < 5

    @staticmethod
    def _is_time_between_range(actual_time: datetime.time, start_time: datetime.time, end_time: datetime.time) -> bool:
        return start_time <= actual_time <= end_time

    def _get_round_rule(self, ticker):
        market_info = self.capital_broker_client.get_market_info(ticker)
        return 1 if market_info["dealingRules"]["minDealSize"]["value"] == 0.1 else 0

    @staticmethod
    def _parse_last_earnings_date(earnings: dict):
        if earnings:
            return earnings["quarterlyEarnings"][0]["reportDate"]
        else:
            return None
