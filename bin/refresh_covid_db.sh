#!/bin/bash

curl http://localhost:8086/query \
  -d db=covid \
  -d q='drop measurement "state_data"'

/home/mdaigle/covid/src/initial_upload.py
