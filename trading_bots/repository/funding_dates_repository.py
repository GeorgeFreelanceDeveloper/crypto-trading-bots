import logging
import sys
import json
from datetime import datetime


class FundingDatesRepository:

    def __init__(self, funding_dates_json_path: str):
        self.funding_dates_json_path = funding_dates_json_path

    def load(self) -> list:
        try:
            logging.debug("Start loading funding dates list")
            with open(self.funding_dates_json_path) as f:
                content = f.read()
                if content:
                    string_list = json.loads(content)
                logging.debug(f"Loaded funding dates list: {content}")
            return [datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S') for dt_str in string_list]
        except Exception as e:
            logging.exception(f"Failed to load funding dates list: {str(e)}")
            sys.exit(-1)

    def save(self, funding_dates: list) -> None:
        try:
            logging.debug("Start saving funding dates list")
            logging.debug(f"Funding dates: {funding_dates}")
            with open(self.funding_dates_json_path, 'w') as f:
                json.dump([dt.strftime('%Y-%m-%d %H:%M:%S') for dt in funding_dates], f, indent=4)
        except Exception as e:
            logging.exception(f"Failed to save funding dates list: {str(e)}")
            sys.exit(-1)
