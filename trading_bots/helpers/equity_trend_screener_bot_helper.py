import logging
import os
import sys

import pandas as pd
import yfinance as yf


class EquityTrendScreenerBotHelper:

    @staticmethod
    def get_daily_ohlc(ticker: str) -> pd.DataFrame:
        try:
            ticker = ticker.replace(".", "-").split(":")[1]
            # Download ohlc data without splits and dividend [auto_adjust=False]
            ohlc_raw = yf.Ticker(ticker).history(period="120mo", interval="1d", auto_adjust=False)
            ohlc = ohlc_raw[["Open", "High", "Low", "Close"]][::-1].reset_index()
            ohlc.columns = ['startTime', 'open', 'high', 'low', 'close']
            return ohlc
        except Exception as e:
            logging.error(f"Failed get_daily_ohlc for ticker {ticker}: {str(e)}")
            sys.exit(-1)

    @staticmethod
    def create_tw_report(trends: pd.DataFrame) -> str:
        report = []

        report.append("###UP-TREND")
        uptrend_markets_df = trends[trends["context"] == "Up-trend"]
        report.extend(uptrend_markets_df["ticker"].tolist())

        report.append("###START ROTATION AFTER UP-TREND")
        start_rotation_markets_df = trends[trends["context"] == "Start rotation after up-trend"]
        report.extend(start_rotation_markets_df["ticker"].tolist())

        report.append("###DOWN-TREND")
        downtrend_markets_df = trends[trends["context"] == "Down-trend"]
        report.extend(downtrend_markets_df["ticker"].tolist())

        report.append("###START ROTATION AFTER DOWN-TREND")
        start_rotation_markets_df = trends[trends["context"] == "Start rotation after down-trend"]
        report.extend(start_rotation_markets_df["ticker"].tolist())

        report.append("###ROTATION")
        rotation_markets_df = trends[trends["context"] == "Rotation"]
        report.extend(rotation_markets_df["ticker"].tolist())

        return ",".join(report)

    @staticmethod
    def save_tw_report(report: str, file_path: str) -> None:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                file.write(report)
        except Exception as e:
            logging.error(f"Failed save tw report: {str(e)}")
            sys.exit(-1)

    @staticmethod
    def count_items_without_rotation(trends: pd.DataFrame) -> int:
        trends_without_rotations = trends[~(trends["context"] == "Rotation") | (trends["context"] == "N/A")]
        return trends_without_rotations.shape[0]
