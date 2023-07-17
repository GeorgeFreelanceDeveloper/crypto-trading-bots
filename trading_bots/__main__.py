import logging.config
import sys

from trading_bots.__version__ import __version__
from trading_bots.constants import __logo__
from trading_bots.repository.config_repository import ConfigRepository
from trading_bots.utils import create_bot

bot_names = ["BybitExampleBot", "CryptoTrendScreenerBot", "EquityTrendScreenerBot",
             "PlaceTrailingStopsBotBybitIntraday", "PlaceTrailingStopsBotBybitSwing",
             "PlaceTrailingStopsBotBybitPosition", "EarlyReactionBotBybitIntraday",
             "EarlyReactionBotBybitSwing", "EarlyReactionBotBybitPosition",
             "PlaceTrailingStopsBotBybitPosition", "CloseTradesAtTimeBotBybitIntraday",
             "CloseTradesAtTimeBotBybitSwing", "CloseTradesAtTimeBotBybitPosition",
             "CheckFuturesMarginLevelBotBybitIntraday", "EquityLevelTraderBotCapitalPositionLong",
             "EquityLevelTraderBotCapitalPositionShort"]

if __name__ == "__main__":
    bot_name = sys.argv[1]

    if bot_name not in bot_names:
        raise ValueError(f"Not supported bot with name: {bot_name}")

    logger_config_file_path = f"config/{bot_name}Logger.conf"
    config_file_path = "config/{}Config.yaml".format(bot_name)

    logging.config.fileConfig(fname=logger_config_file_path, disable_existing_loggers=False)
    logging.info(__logo__.format(bot_name=bot_name, app_version=__version__))

    try:
        config = ConfigRepository(config_file_path).load_config()
        bot = create_bot(bot_name, config)
        bot.run()
    except SystemExit as e:
        logging.warning(f"Close application with code: {str(e)}")
    except Exception as e:
        logging.exception("Error in app: ")
