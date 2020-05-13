#!/usr/bin/env python3

import glob
import csv
from string_util import string_util
from file_util import file_util
from date_util import date_util
from influx_api import InfluxApi
from state_population import StatePopulation

class StateDataUtil():

    data_dir = "/var/lib/covid/data/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/"

    all_state_data = {}
    influx_api = None
    input_files = None
    state_populations = None

    def __init__(self):
        self.state_populations = StatePopulation()
        self.input_files = [f for f in glob.glob(self.data_dir + "*.csv")]
        self.influx_api = InfluxApi()

        for input_file in self.input_files:
            first_line = True
            sortable_date = file_util.file_to_sortable_date(input_file)
            with open(input_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if first_line:
                        first_line = False
                    else:
                        if row[1] == "US" and row[2] != "" and row[0] != "Recovered":
                            state_row = {}
                            state_row["state"] = row[0]
                            state_row["country"] = row[1]
                            state_row["last_update"] = row[2]
                            state_row["lat"] = row[3]
                            state_row["long"] = row[4]
                            state_row["confirmed"] = row[5]
                            state_row["cum_deaths"] = row[6]
                            state_row["recovered"] = row[7]
                            state_row["active"] = row[8]
                            state_row["fips"] = row[9]
                            state_row["incident_rate"] = row[10]
                            state_row["people_tested"] = row[11]
                            state_row["people_hospitalized"] = row[12]
                            state_row["mortality_rate"] = row[13]
                            state_row["uid"] = row[14]
                            state_row["iso3"] = row[15]
                            state_row["testing_rate"] = row[16]
                            state_row["hopitalization_rate"] = row[17]
                            state_row["population"] = self.state_populations.get_state_population(row[0])

                            state_row["epoch_date"] = date_util.date_to_epoch(sortable_date)

                            state_name = row[0]
                            if state_name in self.all_state_data:
                                self.all_state_data[state_name][sortable_date] = state_row
                            else:
                                self.all_state_data[state_name] = {sortable_date: state_row}

    def get_all_state_data():
        return self.all_state_data

    def clear_state_data_from_influxdb(self):
        self.influx_api.delete_measurement("state_data")

    def add_all_state_data_to_influxdb(self):
        print("in add_all_state_data_to_influxdb")
        for state_name in self.all_state_data:
            print(state_name)
            self.add_single_state_data_to_influxdb(self.all_state_data[state_name])

    def add_single_state_data_to_influxdb(self, state_data):
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

            self.influx_api.write(time_series)
