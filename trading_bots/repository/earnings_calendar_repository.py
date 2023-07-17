import csv
import logging
import sys
from datetime import datetime


class EarningsCalendarRepository:

    def __init__(self, earnings_calendar_file_path: str, earnings_calendar_old_file_path: str):
        self.earnings_calendar_file_path = earnings_calendar_file_path
        self.earnings_calendar_old_file_path = earnings_calendar_old_file_path

    def load(self) -> list:
        try:
            logging.debug("Start loading earning calendar")
            result = []
            with open(self.earnings_calendar_file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row["reportDate"] = datetime.strptime(row["reportDate"], "%Y-%m-%d").date()
                    row["fiscalDateEnding"] = datetime.strptime(row["fiscalDateEnding"], "%Y-%m-%d").date()
                    result.append(row)
            logging.debug(f"Loaded earning calendar: {result}")
            return result
        except Exception as e:
            logging.error(f"Failed to load earning calendar: {str(e)}")
            sys.exit(-1)

    def load_old(self) -> list:
        try:
            logging.debug("Start loading old earning calendar")
            result = []
            with open(self.earnings_calendar_old_file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row["reportDate"] = datetime.strptime(row["reportDate"], "%Y-%m-%d").date()
                    row["fiscalDateEnding"] = datetime.strptime(row["fiscalDateEnding"], "%Y-%m-%d").date()
                    result.append(row)
            logging.debug(f"Loaded old earning calendar: {result}")
            return result
        except Exception as e:
            logging.error(f"Failed to load old earning calendar: {str(e)}")
            sys.exit(-1)
