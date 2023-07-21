import yaml

from trading_bots.bybit_example_bot import BybitExampleBot
from trading_bots.check_futures_margin_level_bot_bybit import CheckFuturesMarginLevelBotBybit
from trading_bots.close_trades_at_time_bot_bybit import CloseTradesAtTimeBotBybit
from trading_bots.crypto_trend_screener_bot import CryptoTrendScreenerBot
from trading_bots.early_reaction_bot_bybit import EarlyReactionBotBybit
from trading_bots.equity_level_trader_bot_capital import EquityLevelTraderBotCapital
from trading_bots.equity_trend_screener_bot import EquityTrendScreenerBot
from trading_bots.place_trailing_stops_bot_bybit import PlaceTrailingStopsBotBybit
from trading_bots.templates.bot import Bot


def create_bot(bot_name: str, config: dict) -> Bot:
    match bot_name:
        case "BybitExampleBot":
            return BybitExampleBot(config)
        case "CryptoTrendScreenerBot":
            return CryptoTrendScreenerBot(config)
        case "EquityTrendScreenerBot":
            return EquityTrendScreenerBot(config)
        case "PlaceTrailingStopsBotBybitIntraday":
            return PlaceTrailingStopsBotBybit(config)
        case "PlaceTrailingStopsBotBybitSwing":
            return PlaceTrailingStopsBotBybit(config)
        case "PlaceTrailingStopsBotBybitPosition":
            return PlaceTrailingStopsBotBybit(config)
        case "EarlyReactionBotBybitIntraday":
            return EarlyReactionBotBybit(config)
        case "EarlyReactionBotBybitSwing":
            return EarlyReactionBotBybit(config)
        case "EarlyReactionBotBybitPosition":
            return EarlyReactionBotBybit(config)
        case "CloseTradesAtTimeBotBybitIntraday":
            return CloseTradesAtTimeBotBybit(config)
        case "CloseTradesAtTimeBotBybitSwing":
            return CloseTradesAtTimeBotBybit(config)
        case "CloseTradesAtTimeBotBybitPosition":
            return CloseTradesAtTimeBotBybit(config)
        case "CheckFuturesMarginLevelBotBybitIntraday":
            return CheckFuturesMarginLevelBotBybit(config)
        case "EquityLevelTraderBotCapitalPositionLong":
            return EquityLevelTraderBotCapital(config)
        case "EquityLevelTraderBotCapitalPositionShort":
            return EquityLevelTraderBotCapital(config)
        case _:
            raise ValueError(f"Not supported bot_name: {bot_name}")
