# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [1.2.1] - 2023-08-21
### Fixed
- EquityLevelTraderBotCapital: updated logging info on start and finish
- trading_bots_active_monitor: corrected displaying Start and Finish of bots
- compress_and_remove_old_rolling_logs_job: added new log paths

## [1.2.1] - 2023-07-21
### Fixed
- EarlyReactionBotBybit: fixed calling parameters in constructors

## [1.2.0] - 2023-07-21
### Added
- EquityLevelTraderBotCapital

### Changes
- Clean code EarlyReactionBybitBot
- Create repositories for load and save data
- Update data folder structure (create sub folders orders, markets and cache)
- Update trading_bots_active_monitor.sh

## [1.1.1] - 2023-07-10
### Added
- EquityTrendScreenerBot: Added section "rotation" into report
- CryptoTrendScreenerBot: Added section "rotation" into report

### Fixed
- CloseTradeAtTimeBybitBot: switch to timing by crontab (better performance)
- EquityTrendScreenerBot: Added prefix before tickers
- Clean code and refactoring project


## [1.1.0] - 2023-06-27
### Added
- EquityTrendScreenerBot
- Unit tests

### Deleted
- ForexTrendScreenerBot

### Changed
- CryptoTrendScreenerBotBybit: add support for find positions trends (3M, Y)

### Fixed
- Precise compute context of market (up-trend, down-trend, start-rotation after up-trend, start rotation after downn-trend)
- Better logging in CryptoTrendScreenerBotBybit and EquityTrendScreenerBot

## [1.0.1] - 2023-06-12
### Fixed
- Missing exception handling for pybit client

## [1.0.0] - 2023-06-09
### Added
- BybitExampleBot
- CheckFuturesMarginLevelBotBybit
- CloseTradesAtTimeBotBybit
- CryptoTrendScreenerBotBybit
- EarlyReactionBotBybit
- ForexTrendScreenerBot
- PlaceTrailingStopsBotBybit
