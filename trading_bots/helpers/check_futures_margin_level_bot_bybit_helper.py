import json
import logging
import uuid

from datetime import datetime

from trading_bots import constants


class CheckFuturesMarginLevelBotBybitHelper:

    def __init__(self, pybit_client, funding_dates_json_path):
        self.pybit_client = pybit_client
        self.funding_dates_json_path = funding_dates_json_path
        self.funding_dates = self.load_funding_dates_list()

    def get_available_balance_on_futures_account(self) -> float:
        response = self.pybit_client.get_wallet_balance(
            accountType="CONTRACT",
            coin="USDT")
        logging.debug("Response get_wallet_balance: {}".format(response))

        total_balance = float(response["result"]["list"][0]["coin"][0]["walletBalance"])
        free_balance = float(response["result"]["list"][0]["coin"][0]["availableToWithdraw"])

        logging.info(
            "Total balance: {} USDT, Available balance to withdraw: {} USDT".format(round(total_balance, 2),
                                                                                    round(free_balance, 2)))

        return total_balance

    def is_open_positions(self) -> bool:
        response = self.pybit_client.get_positions(category=constants.BYBIT_LINEAR_CATEGORY, settleCoin="USDT")
        logging.debug("Response get_positions: {}".format(response))
        return len(response["result"]["list"]) > 0

    def was_funding_account_today(self) -> bool:
        if len(self.funding_dates) == 0:
            return False

        last_funding_date = self.funding_dates[-1]
        logging.info("LastFundingDate: {}".format(last_funding_date))
        now = datetime.now()
        return last_funding_date.year == now.year and last_funding_date.month == now.month and last_funding_date.day == now.day

    def get_last_position_close_date(self) -> datetime:
        response = self.pybit_client.get_closed_pnl(category=constants.BYBIT_LINEAR_CATEGORY, limit=2)
        logging.debug("Response get_closed_pnl: {}".format(response))

        last_position_closed_unix_time = float(response["result"]["list"][0]["createdTime"])
        dt = datetime.fromtimestamp(last_position_closed_unix_time / 1000)

        return dt

    def funding_futures_account(self, margin_level: float, available_balance: float):
        funding_amount = round(margin_level - available_balance, 2) + 0.1
        logging.debug("Start funding futures account from spot with amount: {} USDT".format(funding_amount))
        response = self.pybit_client.create_internal_transfer(transferId=str(uuid.uuid4()),
                                                              coin="USDT",
                                                              amount=str(funding_amount),
                                                              fromAccountType="SPOT",
                                                              toAccountType="CONTRACT")
        self.funding_dates.append(datetime.now())
        self.save_funding_dates_list(self.funding_dates)
        logging.debug("Response create_internal_transfer: {}".format(response))

    def load_funding_dates_list(self) -> list:
        with open(self.funding_dates_json_path) as f:
            content = f.read()
            if content:
                string_list = json.loads(content)
        return [datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S') for dt_str in string_list]

    def save_funding_dates_list(self, funding_dates):
        with open(self.funding_dates_json_path, 'w') as f:
            json.dump([dt.strftime('%Y-%m-%d %H:%M:%S') for dt in funding_dates], f, indent=4)
