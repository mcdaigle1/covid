#!/usr/bin/env python3

from influx_api import InfluxApi

class (InfluxBase):
    measurement_name = ""

    def clear_state_data_from_influxdb(self):
        if measurement_name == ""
            raise("measurement_name is empty")
        self.influx_api.delete_measurement(measurement_name)