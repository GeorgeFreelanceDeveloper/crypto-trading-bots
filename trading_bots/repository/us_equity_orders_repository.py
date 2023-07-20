import csv
import logging
import sys

import pandas as pd


class UsEquityOrdersRepository:

    def __init__(self, orders_file_path: str):
        self.orders_file_path = orders_file_path

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
            logging.exception(f"Failed load orders: {str(e)}")
            sys.exit(-1)

    def save_orders(self, orders: list) -> None:
        try:
            logging.debug("Start save orders")
            logging.debug(f"Orders: {orders}")
            pd.DataFrame(orders).to_csv(self.orders_file_path, index=False)
        except Exception as e:
            logging.exception(f"Failed save orders: {str(e)}")
            sys.exit(-1)
