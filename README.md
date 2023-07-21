# Trading bots
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

[![Build Status](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/downloads/)
![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

Trading bots for automate trading and risk management in crypto futures and stocks market.

## Table of Contents

- [About](#about)
- [Development](#development)
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)

## About
This repository contains trading bots designed for automated trading, allowing for the execution of trades based on predefined rules and strategies. Additionally, these bots incorporate risk management techniques, such as setting stop-loss orders and managing position sizes, to effectively mitigate potential losses. The bots are specifically tailored for the crypto futures market and are implemented using the Python programming language.

**Developed trading bots:**
* CryptoTrendScreenerBot
* EquityTrendScreenerBot
* PlaceTrailingStopsBotBybit
* EarlyReactionBotBybit
* CloseTradesAtTimeBotBybit
* CheckFuturesMarginLevelBotBybit
* EquityLevelTraderBotCapital

**Exchange api documentation:**
* [Bybit rest api v5 documentation](https://bybit-exchange.github.io/docs/v5/intro)


## Development
Project is being actively develop and maintained.

## Installation
Trading bots require Python 3.11 and higher, creating virtual environment venv and install dependencies.

For creating venv and install dependencies type in terminal:

```bash
make prepare
```

## Usage

### CryptoTrendScreenerBot
A trading bot designed to identify swing and position trends on the USDT perpetual futures markets of the Bybit exchange.

```bash
make CryptoTrendScreenerBot
```

### EquityTrendScreenerBot
A trading bot that scans for position trends across a wide range of US-traded stocks, including those with weekly options, small-cap stocks in the Russell 2000 index, and large-cap stocks in the S&P 500 index.

```bash
make EquityTrendScreenerBot
```

### PlaceTrailingStopsBotBybit
A trading bot that automatically sets trailing stop-loss orders for open futures positions on the Bybit exchange.

```bash
make placeTrailingStopsBotBybitIntraday # Intraday bot
make placeTrailingStopsBotBybitSwing # Swing bot
make placeTrailingStopsBotBybitPosition # Position bot
```

### EarlyReactionBotBybit
A trading bot that executes close early reaction trades, where the price reaches 33% before entry and then the market turns in favor of profit.

```bash
make EarlyReactionBotBybitIntraday
make EarlyReactionBotBybitSwing
make EarlyReactionBotBybitPosition
```

### CloseTradesAtTimeBotBybit
A trading bot that closes pending orders and positions at a specific predefined time.

```bash
make CloseTradesAtTimeBotBybitIntraday # Intraday bot
make CloseTradesAtTimeBotBybitSwing # Swing bot
make CloseTradesAtTimeBotBybitPosition # Position bot
```


### CheckFuturesMarginLevelBotBybit
A trading bot that regularly checks the margin level on the futures exchange. If the margin falls below the specified limit, the bot automatically funding the futures account to the defined level after a certain time interval expires.

```bash
make CheckFuturesMarginLevelBotBybitIntraday # Intraday bot
make CheckFuturesMarginLevelBotBybitSwing # Swing bot
make CheckFuturesMarginLevelBotBybitPosition # Position bot
```

### EquityLevelTraderBotCapital
Trading bot for trading US shares through the Capital.com broker. A trading bot that monitors the current price and 
watch whether price arrives at entry price for place trade and if order was an early reaction or not. 
(If the share price reaches 33% before the entry and then react to profit).

```bash
make equityLevelTraderBotCapitalPositionLong # Position long portfolio
make equityLevelTraderBotCapitalPositionShort # Position short portfolio
```
## Contributors
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
     <td align="center"><a href="https://github.com/GeorgeQuantAnalyst"><img src="https://avatars.githubusercontent.com/u/112611533?v=4" width="100px;" alt=""/><br /><sub><b>GeorgeQuantAnalyst</b></sub></a><br /><a href="https://github.com/GeorgeQuantAnalyst" title="Ideas">🤔</a></td>
    <td align="center"><a href="https://github.com/LucyQuantAnalyst"><img src="https://avatars.githubusercontent.com/u/115091833?v=4" width="100px;" alt=""/><br /><sub><b>LucyQuantAnalyst</b></sub></a><br /><a href="https://github.com/LucyQuantAnalyst" title="Code">💻</a></td>
  </tr>
</table>
