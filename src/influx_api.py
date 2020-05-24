#!/usr/bin/env python3

import requests

class InfluxApi:

    INFLUX_WRITE_ENDPOINT = "http://localhost:8086/write?db=covid"
    INFLUX_QUERY_ENDPOINT = "http://localhost:8086/query?db=covid"

    # convert a date from the file, like: 2020-04-12 23:18:15 to an epoch date representing 00:00:00 that day
    def write(self, time_series):
        r = requests.post(url = self.INFLUX_WRITE_ENDPOINT, data = time_series)
        if r.status_code < 200 or r.status_code > 299:
            print("writing to influx: " + time_series)
            print(r)

    def query(self, query):
        url = self.INFLUX_QUERY_ENDPOINT + "&q=" + query
        r = requests.get(url)
        if r.status_code < 200 or r.status_code > 299:
            print("query influx: " + url)
            print(r)

    def delete_measurement(self, measurement):
        self.query('drop measurement "' + measurement + '"')
