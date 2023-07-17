#!/bin/bash

EARNING_CALENDAR_URL="https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey=demo"
EARNING_CALENDAR="../data/earnings_calendar.csv"
EARNING_CALENDAR_OLD="../data/earnings_calendar_old.csv"

cp ${EARNING_CALENDAR} ${EARNING_CALENDAR_OLD}
wget ${EARNING_CALENDAR_URL} -O ${EARNING_CALENDAR}