#!/usr/bin/env python3

import requests
from string_util import string_util
from influx_api import InfluxApi

#API_ENDPOINT = "http://localhost:8086/write?db=covid"

class StateData(InfluxApi):

    def add_state_data(this, state_data):
        for sortable_date in sorted(state_data.keys()):
            time_series = ""
            time_series += "state_data,"

            time_series += "name=" + string_util.canonical(state_data[sortable_date]["state"]) + ","
            time_series += "country=" + state_data[sortable_date]["country"] + " "

            time_series += "state=\"" + state_data[sortable_date]["state"] + "\","
            time_series += "population=" + str(state_data[sortable_date]["population"]) + ","
            time_series += "last_update=\"" + state_data[sortable_date]["last_update"] + "\","
            time_series += "lat=" + string_util.default_zero(state_data[sortable_date]["lat"]) + ","
            time_series += "long=" + string_util.default_zero(state_data[sortable_date]["long"]) + ","
            time_series += "confirmed=" + string_util.default_zero(state_data[sortable_date]["confirmed"]) + ","
            time_series += "cum_deaths=" + string_util.default_zero(state_data[sortable_date]["cum_deaths"]) + ","
            time_series += "recovered=" + string_util.default_zero(state_data[sortable_date]["recovered"]) + ","
            time_series += "active=" + string_util.default_zero(state_data[sortable_date]["active"]) + ","
            time_series += "fips=" + state_data[sortable_date]["fips"] + ","
            time_series += "incident_rate=" + string_util.default_zero(state_data[sortable_date]["incident_rate"]) + ","
            time_series += "people_tested=" + string_util.default_zero(state_data[sortable_date]["people_tested"]) + ","
            time_series += "people_hospitalized=" + string_util.default_zero(state_data[sortable_date]["people_hospitalized"]) + ","
            time_series += "mortality_rate=" + string_util.default_zero(state_data[sortable_date]["mortality_rate"]) + ","
            time_series += "uid=" + state_data[sortable_date]["uid"] + ","
            time_series += "iso3=\"" + state_data[sortable_date]["iso3"] + "\","
            time_series += "testing_rate=" + string_util.default_zero(state_data[sortable_date]["testing_rate"]) + ","
            time_series += "hopitalization_rate=" + string_util.default_zero(state_data[sortable_date]["hopitalization_rate"]) + " "

            time_series += state_data[sortable_date]["epoch_date"]

            super().write(time_series)
            #print("writing to influx: " + time_series)
            #r = requests.post(url = API_ENDPOINT, data = time_series)
            #print(r)
