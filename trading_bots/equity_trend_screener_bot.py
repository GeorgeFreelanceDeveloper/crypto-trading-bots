import logging

import pandas as pd

from trading_bots.helpers.equity_trend_screener_bot_helper import EquityTrendScreenerBotHelper
from trading_bots.repository.markets_repository import MarketsRepository
from trading_bots.templates.bot import Bot
from trading_bots.trading_math import convert_ohlc, calculate_context


class EquityTrendScreenerBot(Bot):
    SEPARATOR = "------------------------"

    def __init__(self, config):
        super().__init__(config)
        self.helper = EquityTrendScreenerBotHelper()
        self.markets = MarketsRepository(config)

    def run(self) -> None:
        logging.info("Start EquityTrendScreenerBot")

        tickers = self.loading_tickers()
        trends = self.find_trends(tickers)
        self.create_tw_trends_report(trends)

        logging.info("Finished EquityTrendScreenerBot")

    def loading_tickers(self) -> dict[str, list]:
        logging.info(self.SEPARATOR)
        logging.info("Loading tickers")
        logging.info(self.SEPARATOR)

        if self.config["mostTradedUsStocks"]["enable"]:
            tickers_most_traded_us_stocks = self.markets.load_most_traded_us_stocks()
        else:
            tickers_most_traded_us_stocks = []

        if self.config["sp500"]["enable"]:
            tickers_sp_500 = self.markets.load_sp_500()
        else:
            tickers_sp_500 = []

        if self.config["russell2k"]["enable"]:
            tickers_russell_2k = self.markets.load_russell_2000()
        else:
            tickers_russell_2k = []

        logging.info(f"Loaded {len(tickers_most_traded_us_stocks)} tickers for Most traded US stocks")
        logging.info(f"Loaded {len(tickers_sp_500)} tickers for index S&P 500")
        logging.info(f"Loaded {len(tickers_russell_2k)} tickers for index Russell 2000")

        return {
            "tickers_most_traded_us_stocks": tickers_most_traded_us_stocks,
            "tickers_sp_500": tickers_sp_500,
            "tickers_russell_2k": tickers_russell_2k
        }

    def find_trends(self, tickers: dict[str, list]) -> dict[str, pd.DataFrame]:
        logging.info(self.SEPARATOR)
        logging.info("Find trends")
        logging.info(self.SEPARATOR)

        def process_tickers(ticker_list, category_list):
            logging.info(f"Find trends in {category_list} tickers")
            quarterly_trends = []
            yearly_trends = []

            for ticker in ticker_list:
                logging.info(f"Process {ticker} ticker")
                daily_ohlc = self.helper.get_daily_ohlc(ticker)
                quarterly_ohlc = convert_ohlc(daily_ohlc, "Q")
                yearly_ohlc = convert_ohlc(daily_ohlc, "Y")

                logging.debug(f"Daily ohlc (last 10 candles): \n {daily_ohlc}")
                logging.debug(f"Quarterly ohlc (last 10 candles): \n {quarterly_ohlc}")
                logging.debug(f"Yearly ohlc (last 10 candles): \n {yearly_ohlc}")

                quarterly_context = calculate_context(quarterly_ohlc)
                yearly_context = calculate_context(yearly_ohlc)

                logging.debug(f"Quarterly context: {quarterly_context}")
                logging.debug(f"Yearly context: {yearly_context}")

                quarterly_trends.append({
                    "ticker": ticker,
                    "context": quarterly_context
                })

                yearly_trends.append({
                    "ticker": ticker,
                    "context": yearly_context
                })

            return pd.DataFrame(quarterly_trends), pd.DataFrame(yearly_trends)

        most_traded_us_stocks_quarterly_trends, most_traded_us_stocks_yearly_trends = process_tickers(
            tickers["tickers_most_traded_us_stocks"], "Most traded US stocks")
        sp_500_quarterly_trends, sp_500_yearly_trends = process_tickers(tickers["tickers_sp_500"], "S&P 500")
        russell_2k_quarterly_trends, russell_2k_yearly_trends = process_tickers(tickers["tickers_russell_2k"],
                                                                                "Russell 2000")

        return {
            "most_traded_us_stocks_quarterly_trends": most_traded_us_stocks_quarterly_trends,
            "most_traded_us_stocks_yearly_trends": most_traded_us_stocks_yearly_trends,
            "sp_500_quarterly_trends": sp_500_quarterly_trends,
            "sp_500_yearly_trends": sp_500_yearly_trends,
            "russell_2k_quarterly_trends": russell_2k_quarterly_trends,
            "russell_2k_yearly_trends": russell_2k_yearly_trends
        }

    def create_tw_trends_report(self, trends):
        logging.info(self.SEPARATOR)
        logging.info("Create TradingView trends report")
        logging.info(self.SEPARATOR)

        reports_folder = self.config["base"]["reportsFolder"]

        def create_report(trend_data, report_name):
            if not trend_data.empty:
                report_path = f"{reports_folder}/{report_name}.txt"
                trend_report = self.helper.create_tw_report(trend_data)
                self.helper.save_tw_report(trend_report, report_path)

        create_report(trends["most_traded_us_stocks_quarterly_trends"], "Most traded US stocks 3M trends")
        create_report(trends["most_traded_us_stocks_yearly_trends"], "Most traded US stocks Y trends")
        create_report(trends["sp_500_quarterly_trends"], "S&P 500 3M trends")
        create_report(trends["sp_500_yearly_trends"], "S&P 500 Y trends")

        def create_russell_report(trend_data, report_name):
            if not trend_data.empty:
                if self.helper.count_items_without_rotation(trend_data) > 1000:
                    report_path_part1 = f"{reports_folder}/{report_name} part1.txt"
                    report_path_part2 = f"{reports_folder}/{report_name} part2.txt"

                    n = trend_data.shape[0]
                    trend_data_part1 = trend_data.head(n // 2)
                    trend_data_part2 = trend_data.tail(n // 2)

                    trend_report_part1 = self.helper.create_tw_report(trend_data_part1)
                    trend_report_part2 = self.helper.create_tw_report(trend_data_part2)

                    self.helper.save_tw_report(trend_report_part1, report_path_part1)
                    self.helper.save_tw_report(trend_report_part2, report_path_part2)
                else:
                    report_path = f"{reports_folder}/{report_name}.txt"
                    trend_report = self.helper.create_tw_report(trend_data)
                    self.helper.save_tw_report(trend_report, report_path)

        create_russell_report(trends["russell_2k_quarterly_trends"], "Russell 2000 3M trends")
        create_russell_report(trends["russell_2k_yearly_trends"], "Russell 2000 Y trends")
