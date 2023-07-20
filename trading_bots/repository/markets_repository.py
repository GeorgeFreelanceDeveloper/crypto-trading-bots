import logging
import sys

import pandas as pd


class MarketsRepository:

    def __init__(self, config):
        self.most_traded_us_stocks_file_path = config["mostTradedUsStocks"]["tickersFilePath"]
        self.russell_2000_file_path = config["sp500:"]["tickersFilePath:"]
        self.sp_500_file_path = config["russell2k"]["tickersFilePath"]

    def load_most_traded_us_stocks(self):
        self._get_tickers(self.most_traded_us_stocks_file_path)

    def load_russell_2000(self):
        self._get_tickers(self.russell_2000_file_path)

    def load_sp_500(self):
        self._get_tickers(self.sp_500_file_path)

    @staticmethod
    def _get_tickers(file_path: str) -> list:
        try:
            df = pd.read_csv(file_path)
            logging.debug(f"Tickers (first 5):\n {df.head()}")
            return df["Ticker"].tolist()
        except Exception as e:
            logging.exception(f"Failed read tickers from file {file_path}: {str(e)}")
            sys.exit(-1)
