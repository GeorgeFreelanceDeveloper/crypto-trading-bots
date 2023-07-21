# EquityLevelTraderBotCapital

## About bot
Trading bot for trading US shares through the Capital.com broker. A trading bot that monitors the current price and 
watch whether price arrives at entry price for place trade and if order was an early reaction or not. 
(If the share price reaches 33% before the entry and then react to profit).

## Configuration
-- Long portfolio
* [Bot configuration](../config/EquityLevelTraderBotCapitalPositionLongConfig.yaml)
* [Logger configuration](../config/EquityLevelTraderBotCapitalPositionLongLogger.conf)

-- Short portfolio
* [Bot configuration](../config/EquityLevelTraderBotCapitalPositionShortConfig.yaml)
* [Logger configuration](../config/EquityLevelTraderBotCapitalPositionShortLogger.conf)
## How to run

```commandline
make equityLevelTraderBotCapitalPositionLong 
make equityLevelTraderBotCapitalPositionShort
```

