#!/usr/bin/env python3

import requests

class InfluxApi:

    INFLUX_WRITE_ENDPOINT = "http://localhost:8086/write?db=covid"

    # convert a date from the file, like: 2020-04-12 23:18:15 to an epoch date representing 00:00:00 that day
    def write(time_series)
        print("writing to influx: " + time_series)
        r = requests.post(url = API_WRITE_ENDPOINT, data = time_series)
        print(r)

