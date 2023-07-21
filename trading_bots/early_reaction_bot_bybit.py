import logging

from trading_bots.helpers.early_reaction_bot_bybit_helper import EarlyReactionBotBybitHelper
from trading_bots.repository.before_entry_ids_repository import BeforeEntryIdsRepository
from trading_bots.templates.bybit_bot import BybitBot


class EarlyReactionBotBybit(BybitBot):

    def __init__(self, config: dict):
        super().__init__(config)
        self.helper = EarlyReactionBotBybitHelper(self.config, self.pybit_client)
        self.before_entry_ids_repository = BeforeEntryIdsRepository(config["base"]["beforeEntryIdsJsonPath"])
        self.before_entry_ids = self.before_entry_ids_repository.load()
        logging.info("Before entry ids: {}".format(self.before_entry_ids))

    def run(self) -> None:
        logging.info("Start EarlyReactionBotBybit")

        pending_orders = self.helper.get_pending_orders()
        logging.info("Count pending orders: {}".format(len(pending_orders)))
        logging.debug("Pending orders: {}".format(pending_orders))

        for order in pending_orders:
            order_id = order["orderId"]
            logging.info(f"Process order: {order_id}")
            last_closed_bar = self.helper.get_last_closed_bar(order["symbol"])

            if order_id in self.before_entry_ids:
                logging.info(f"Check price reach profit target")
                if self.helper.check_price_reach_profit_target(order, last_closed_bar):
                    logging.info("Price reach profit target, order will be cancel")
                    self.helper.cancel_pending_order(order_id, order["symbol"])
                    self.before_entry_ids.remove(order_id)
                    continue

            if self.helper.check_price_reach_before_entry_price(order, last_closed_bar):
                logging.info("Price reach before entry price, set attribute before_entry")
                self.before_entry_ids.append(order_id)

        self.helper.remove_not_exists_ids(self.before_entry_ids, pending_orders)
        self.before_entry_ids_repository.save(self.before_entry_ids)

        logging.info("Finished EarlyReactionBotBybit")
