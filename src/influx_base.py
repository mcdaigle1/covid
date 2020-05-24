#!/usr/bin/env python3

from influx_api import InfluxApi

class InfluxBase():
    measurement_name = ""

    def __init__(self, measurement_name):
        self.measurement_name = measurement_name

    def clear_measurement(self):
        if self.measurement_name == "":
            raise Exception("measurement_name is empty")
        print("Deleting measurement: " + self.measurement_name)
        self.influx_api.delete_measurement(self.measurement_name)
