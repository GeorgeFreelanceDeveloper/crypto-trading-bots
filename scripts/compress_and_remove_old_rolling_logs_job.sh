#!/bin/bash

APP_LOG_FOLDERS=("/home/prod1/log/close-trades-at-time-bot-bybit-swing/" \
"/home/prod1/log/close-trades-at-time-bot-bybit-intraday/" \
"/home/prod1/log/close-trades-at-time-bot-bybit-position/" \
"/home/prod1/log/equity-trend-screener-bot/" \
"/home/prod1/log/crypto-trend-screener-bot/" \
"/home/prod1/log/place-trailing-stops-bot-bybit-swing/" \
"/home/prod1/log/place-trailing-stops-bot-bybit-intraday/" \
"/home/prod1/log/place-trailing-stops-bot-bybit-position/" \
"/home/prod1/log/early-reaction-bot-bybit-intraday/" \
"/home/prod1/log/early-reaction-bot-bybit-position/" \
"/home/prod1/log/early-reaction-bot-bybit-swing/" \
"/home/prod1/log/check-futures-margin-level-bot-bybit-intraday/" \
"/home/prod1/log/equity-level-trader-bot-capital-position-long/" \
"/home/prod1/log/equity-level-trader-bot-capital-position-short/")

echo "Start job"
for log_folder in "${APP_LOG_FOLDERS[@]}"; do
        echo "Process log folder: ${log_folder}"
        cd $log_folder

        echo "Compress rolling files to gz and move to archive"
        gzip *log.*
        mkdir -p archive
        mv *.gz archive/

        echo "Delete old log files (older than 7 days)"
        cd archive
        find . -name "*log.*" -type f -mtime +7 -delete
done
echo "Finished job"