#!/bin/bash

#curl http://localhost:8086/query \
#  -d db=covid \
#  -d q='drop measurement "daily_deaths"'
#
#curl http://localhost:8086/query \
#  -d db=covid \
#  -d q='drop measurement "state_data"'
#
#curl http://localhost:8086/query \
#  -d db=covid \
#  -d q='drop measurement "trend_daily_deaths"'

/home/mdaigle/covid/src/refresh_state_data.py
/home/mdaigle/covid/src/refresh_state_mortality.py
/home/mdaigle/covid/src/refresh_state_trends.py
/home/mdaigle/covid/src/refresh_state_trends_7_days.py