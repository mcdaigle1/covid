#!/bin/bash

curl http://localhost:8086/query \
  -d db=covid \
  -d q='drop measurement "daily_deaths"'

curl http://localhost:8086/query \
  -d db=covid \
  -d q='drop measurement "state_data"'

curl http://localhost:8086/query \
  -d db=covid \
  -d q='drop measurement "trend_daily_deaths"'

/home/mdaigle/covid/src/initial_upload.py
