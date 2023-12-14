# Signifies our desired python version
# Makefile macros (or variables) are defined a little bit differently than traditional bash, keep in mind that in the Makefile there's top-level Makefile-only syntax, and everything else is bash script syntax.
PYTHON = python3.11
# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY = help prepare test run clean

# Defining an array variable
FILES = input output

# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo "To prepare the project type make prepare"
	@echo "To test the project type make test"
	@echo "To clean the project type make run"
	@echo "To build the project type make build"
	@echo "To run the project type make run"
	@echo "------------------------------------"

prepare:
	@echo "Prepaparing ..."
	${PYTHON} -m venv venv
	. venv/bin/activate && ${PYTHON} -m pip install -U pip wheel setuptools
	. venv/bin/activate && pip install -r requirements.txt

test:
	@echo "Testing ..."
	. venv/bin/activate && ${PYTHON} -m unittest discover -v

build:
	@echo "Building ..."
	${PYTHON} setup.py sdist

clean:
	@echo "Cleaning ..."
	rm -rf dist
	rm -rf *.egg-info
	rm -rf venv

bybitExampleBot:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots BybitExampleBot

cryptoTrendScreenerBot:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots CryptoTrendScreenerBot

equityTrendScreenerBot:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots EquityTrendScreenerBot

placeTrailingStopsBotBybitIntraday:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots PlaceTrailingStopsBotBybitIntraday

placeTrailingStopsBotBybitSwing:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots PlaceTrailingStopsBotBybitSwing

placeTrailingStopsBotBybitPosition:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots PlaceTrailingStopsBotBybitPosition

earlyReactionBotBybitIntraday:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots EarlyReactionBotBybitIntraday

earlyReactionBotBybitSwing:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots EarlyReactionBotBybitSwing

earlyReactionBotBybitPosition:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots EarlyReactionBotBybitPosition

closeTradesAtTimeBotBybitIntraday:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots CloseTradesAtTimeBotBybitIntraday

closeTradesAtTimeBotBybitSwing:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots CloseTradesAtTimeBotBybitSwing

closeTradesAtTimeBotBybitPosition:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots CloseTradesAtTimeBotBybitPosition

checkFuturesMarginLevelBotBybitIntraday:
	@echo "Run bot..."
	. venv/bin/activate && ${PYTHON} -m trading_bots CheckFuturesMarginLevelBotBybitIntraday
