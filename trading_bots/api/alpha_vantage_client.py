import csv
import logging
from io import StringIO

import requests


class AlphaVantageClient:
    CALL_LIMIT_ERROR = "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day."

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_earnings(self, ticker: str) -> dict:
        try:
            url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={self.api_key}"
            response = requests.get(url)

            if response.status_code != 200:
                raise Exception(f"HTTP Error {response.status_code}: {response.reason}")

            if self.CALL_LIMIT_ERROR in response.text:
                raise Exception(self.CALL_LIMIT_ERROR)

            logging.debug(f"Response get_earnings: {response.text}]")

            return response.json()
        except Exception as e:
            logging.error(f"Failed call GET method /query?function=EARNINGS on www.alphavantage.co REST api: {str(e)}")
            return {}

    def get_earnings_calendar(self, ticker: str) -> list:
        try:
            horizon = "12month"
            url = f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol={ticker}&horizon={horizon}&apikey={self.api_key}"
            response = requests.get(url)

            if response.status_code != 200:
                raise Exception(f"HTTP Error {response.status_code}: {response.reason}")

            response_text = response.text
            if self.CALL_LIMIT_ERROR in response_text:
                raise Exception(self.CALL_LIMIT_ERROR)

            logging.debug(f"Response get_earnings: {response.text}]")

            csv_reader = csv.DictReader(StringIO(response_text))
            return list(csv_reader)
        except Exception as e:
            logging.error(
                f"Failed call GET method /query?function=EARNINGS_CALENDAR on www.alphavantage.co REST api: {str(e)}")
            return []

