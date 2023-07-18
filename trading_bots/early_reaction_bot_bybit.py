import logging

from trading_bots.helpers.early_reaction_bot_bybit_helper import EarlyReactionBotBybitHelper
from trading_bots.templates.bybit_bot import BybitBot


class EarlyReactionBotBybit(BybitBot):

    def __init__(self, config: dict):
        super().__init__(config)
        self.helper = EarlyReactionBotBybitHelper(self.pybit_client, self.config["base"]["beforeEntryIdsJsonPath"])
        self.before_entry_ids = self.helper.load_before_entry_ids_list()
        logging.info("Before entry ids: {}".format(self.before_entry_ids))

    def run(self) -> None:
        logging.info("Start EarlyReactionBotBybit")

        pending_orders = self.helper.get_pending_orders()
        logging.info("Count pending orders: {}".format(len(pending_orders)))
        logging.debug("Pending orders: {}".format(pending_orders))

        # TODO: lucka simplify code like this
        for order in pending_orders:
            order_id = order["orderId"]
            logging.info(f"Process order: {order_id}")

            if order_id in self.before_entry_ids:
                logging.info(f"Check price reach profit target")
                if self.helper.check_price_reach_profit_target(order):
                    logging.info("Price reach profit target, order will be cancel")
                    self.helper.cancel_pending_order(order_id, order["symbol"])
                    self.before_entry_ids.remove(order_id)
                    continue

            if self.helper.check_price_reach_before_entry_price(order):
                logging.info("Price reach before entry price, set attribute before_entry")
                self.before_entry_ids.append(order_id)

        for order in pending_orders:
            logging.info("Process order {}".format(order["orderId"]))

            take_profit = float(order["takeProfit"])
            stop_loss = float(order["stopLoss"])
            entry_price = float(order["price"])
            percentage_before_entry = self.config["base"]["percentageBeforeEntry"]
            symbol = order["symbol"]
            order_side = order["side"]
            order_id = order["orderId"]

            last_closed_bar = self.helper.get_last_closed_bar(symbol)

            if take_profit == 0 or stop_loss == 0:
                logging.warning(f"Order {order_id} does not have bracket orders (profit target and stop loss), "
                                "continuing to the next order.")
                continue

            before_entry_price = entry_price + ((entry_price - stop_loss) * percentage_before_entry)
            logging.info(f"Before entry price: {before_entry_price}")

            logging.info(f"Last closed bar: {last_closed_bar}")

            if order_id not in self.before_entry_ids:
                if (order_side == "Buy" and before_entry_price >= last_closed_bar["lowPrice"]) or (
                        order_side == "Sell" and before_entry_price <= last_closed_bar["highPrice"]):
                    logging.info(
                        f"""
                        Price arrived before entry: [Order Id: {order_id}, Before Entry Price: {before_entry_price}, "
                        Last Bar Low: {last_closed_bar["lowPrice"]}, last Bar High: {last_closed_bar["highPrice"]}]
                        """
                    )
                    self.before_entry_ids.append(order_id)
            else:
                if (order_side == "Buy" and take_profit <= last_closed_bar["highPrice"]) or (
                        order_side == "Sell" and take_profit >= last_closed_bar["lowPrice"]):
                    logging.info(
                        f"""
                        Price arrived to TakeProfit before reaching EntryPrice and make EarlyReaction,
                        pending order will be canceled.: [Order Id: {order_id}, Take Profit: {take_profit},
                        Last Bar Low: {last_closed_bar["lowPrice"],} Last Bar High: {last_closed_bar["highPrice"]}]
                        """
                    )
                    self.helper.cancel_pending_order(order_id, symbol)
                    self.before_entry_ids.remove(order_id)

        self.helper.remove_not_exists_ids(self.before_entry_ids, pending_orders)
        self.helper.save_before_entry_ids_list(self.before_entry_ids)
        logging.info("Finished EarlyReactionBotBybit")
