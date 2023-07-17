import csv
import logging
import sys
from datetime import datetime

import pandas as pd


class EquityLevelTraderBotCapitalRepository:

    def __init__(self, orders_file_path: str, earning_calendar_file_path: str):
        self.orders_file_path = orders_file_path
        self.earning_calendar_file_path = earning_calendar_file_path

    def load_orders(self) -> list:
        try:
            logging.debug("Start load orders")
            result = []
            with open(self.orders_file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    result.append(row)

            logging.debug(f"Loaded orders: \n {result}")
            return result
        except Exception as e:
            logging.error(f"Failed load orders: {str(e)}")
            sys.exit(-1)

    def save_orders(self, orders: list) -> None:
        try:
            logging.debug("Start save orders")
            logging.debug(f"Orders: {orders}")
            pd.DataFrame(orders).to_csv(self.orders_file_path, index=False)
        except Exception as e:
            logging.error(f"Failed save orders: {str(e)}")
            sys.exit(-1)

    def load_earnings_calendar(self) -> list:
        try:
            logging.debug("Start loading earning calendar")
            result = []
            with open(self.earning_calendar_file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row["reportDate"] = datetime.strptime(row["reportDate"], "%Y-%m-%d").date()
                    row["fiscalDateEnding"] = datetime.strptime(row["fiscalDateEnding"], "%Y-%m-%d").date()
                    result.append(row)
            logging.debug(f"Loaded earning calendar: {result}")
            return result
        except Exception as e:
            logging.error(f"Failed load earning calendar: {str(e)}")
            sys.exit(-1)

    def load_earnings_calendar_old(self) -> list:
        # TODO: Lucka implement me
        pass
