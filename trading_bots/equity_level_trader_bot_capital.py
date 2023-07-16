import logging
import sys

from trading_bots.helpers.equity_level_trader_bot_capital_helper import EquityLevelTraderBotCapitalHelper
from trading_bots.repository.equity_level_trader_bot_capital_repository import EquityLevelTraderBotCapitalRepository
from trading_bots.templates.bot import Bot


class EquityLevelTraderBotCapital(Bot):

    def __init__(self, config: dict):
        self.repository = EquityLevelTraderBotCapitalRepository(config["base"]["ordersCsvPath"],
                                                                config["base"]["earningCalendarCsvPath"])
        earning_calendar = self.repository.load_earnings_calendar()
        self.helper = EquityLevelTraderBotCapitalHelper(config, earning_calendar)

    def run(self):
        logging.info("Start EquityLevelTraderCapital")

        if not self.helper.is_open_exchange():
            logging.info("The American stock exchange is currently not open, the bot will not continue working.")
            sys.exit(0)

        orders = self.repository.load_orders()
        self.check_early_reaction(orders)
        self.place_trade(orders)
        self.repository.save_orders(orders)

        logging.info("Finished EquityLevelTraderCapital")

    def check_early_reaction(self, orders):
        logging.info("Start check early reaction step")

        logging.info("Start process orders")
        for order in orders:
            try:
                logging.info(f"Proces order with id: {order['id']}")
                if order["active"]:
                    logging.info(f"Skip active order: [OrderId: {order['id']}]")
                    continue

                if order['early_reaction']:
                    logging.info(f"Skip early reaction order: [OrderId: {order['id']}]")
                    continue

                if order["before_entry"]:
                    logging.info(f"Check price reach profit target: [OrderId: {order['id']}]")
                    if self.helper.check_price_reach_profit_target(order):
                        logging.info("Price reach profit target, order will be mark as early reaction")
                        order["early_reaction"] = True
                    continue

                if self.helper.check_price_reach_before_entry_price(order):
                    logging.info("Price reach before entry price, set attribute before_entry")
                    order["before_entry"] = True
            except Exception as e:
                logging.error(f"Failed proces order [OrderId: {order['id']}]: {str(e)}")

        logging.info("Finished check early reaction step")

    def place_trade(self, orders):
        logging.info("Start place trade step")

        if self.helper.is_open_positions():
            logging.info(
                "The application will not check the orders for entry, because there is an open trade on the exchange.")
            return

        logging.info("Start process orders")
        for order in orders:
            try:
                logging.info(f"Process order with id: {order['id']}")
                ticker = order["ticker"]

                if order["active"]:
                    logging.info(f"Skip active order: [OrderId: {order['id']}]")
                    continue

                if order['early_reaction']:
                    logging.info(f"Skip early reaction order: [OrderId: {order['id']}]")
                    continue

                if self.helper.was_yesterday_earnings(order):
                    logging.info(f"Skip ticker {ticker}, because yesterday was earnings. [OrderId: {order['id']}]")
                    continue

                # Update earnings date in orders
                order["next_earnings_date"] = self.helper.get_next_earnings_date(ticker)

                if self.helper.is_earnings_next_days(order, 10):
                    logging.info(
                        f"Skip ticker {ticker}, because equity has earning in next 10 days. [OrderId: {order['id']}]")
                    continue

                if self.helper.is_price_at_entry_price(order):
                    logging.info("Price is on entry price, order will be place on exchange.")
                    self.helper.place_trade(order)
                    order["active"] = True
                    break
            except Exception as e:
                logging.error(f"Failed place trade [OrderId: {order['id']}]: {str(e)}")

        logging.info("Finished place trade step")
