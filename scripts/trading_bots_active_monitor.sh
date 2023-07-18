#!/bin/bash

# TODO: Lucka trading-bots-activity-monitor.sh nakonfigurovat pouze pro earlyReaction, placeTrailingStop crypto swing + levelTrader US stock

BOT_NAMES=("early-reaction-bot-bybit-intraday" \
"early-reaction-bot-bybit-swing" \
"early-reaction-bot-bybit-position" \
"place-trailing-stops-bot-bybit-intraday" \
"place-trailing-stops-bot-bybit-swing" \
"place-trailing-stops-bot-bybit-position" \
"check-futures-margin-level-bot-bybit-intraday" \
"crypto-trend-screener-bot" \
"equity-trend-screener-bot")

LOG_PATHS=("${HOME}/log/early-reaction-bot-bybit-intraday/early_reaction_bot_bybit_intraday.log" \
"${HOME}/log/early-reaction-bot-bybit-swing/early_reaction_bot_bybit_swing.log" \
"${HOME}/log/early-reaction-bot-bybit-position/early_reaction_bot_bybit_position.log" \
"${HOME}/log/place-trailing-stops-bot-bybit-intraday/place_trailing_stops_bot_bybit_intraday.log" \
"${HOME}/log/place-trailing-stops-bot-bybit-swing/place_trailing_stops_bot_bybit_swing.log" \
"${HOME}/log/place-trailing-stops-bot-bybit-position/place_trailing_stops_bot_bybit_position.log" \
"${HOME}/log/check-futures-margin-level-bot-bybit-intraday/check_futures_margin_level_bot_bybit_intraday.log" \
"${HOME}/log/crypto-trend-screener-bot/crypto_trend_screener_bot.log" \
"${HOME}/log/equity-trend-screener-bot/equity_trend_screener_bot.log")


echo "---------------------------------------------------"
echo Trading bots active monitor
echo "---------------------------------------------------"

echo
echo

for i in "${!BOT_NAMES[@]}"
do
	echo "********************************************"
	echo "# ${BOT_NAMES[$i]}"
	echo "********************************************"
	grep "INFO - Start\|INFO - Finished" ${LOG_PATHS[$i]} | tail -2
  echo
done

echo
echo