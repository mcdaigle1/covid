#!/usr/bin/env python3

from utils.string_util import StringUtil
from influx_api import InfluxApi
from influx_base import InfluxBase
from if_state_data import IfStateData
from state_population import StatePopulation

class IfStateCases(InfluxBase):

    all_state_daily_cases = {}
    influx_api = None
    state_populations = None
    if_state_data = None

    def __init__(self):
        super().__init__("daily_cases")
        self.state_populations = StatePopulation()
        self.if_state_data = IfStateData()
        self.influx_api = InfluxApi()

        all_state_data = self.if_state_data.get_all_state_data()
        for state_name in all_state_data:
            self.all_state_daily_cases[state_name] = {}
            first_row = True
            state_data = all_state_data[state_name]
            for sortable_date in sorted(state_data.keys()):
                if first_row:
                    cum_cases_yesterday = int(state_data[sortable_date]["active"])
                    first_row = False
                else:
                    cum_cases = int(state_data[sortable_date]["active"])
                    daily_cases = cum_cases - cum_cases_yesterday

                    self.all_state_daily_cases[state_name][sortable_date] = {}
                    self.all_state_daily_cases[state_name][sortable_date]["value"] = daily_cases
                    self.all_state_daily_cases[state_name][sortable_date]["population"] = str(self.state_populations.get_state_population(state_name))
                    self.all_state_daily_cases[state_name][sortable_date]["epoch_date"] = state_data[sortable_date]["epoch_date"]
                    cum_cases_yesterday = cum_cases

    def get_all_state_daily_cases(self):
        return self.all_state_daily_cases

    def add_all_state_cases_to_influxdb(self):
        for state_name in self.all_state_daily_cases:
            state_daily_cases = self.all_state_daily_cases[state_name]
            for sortable_date in sorted(state_daily_cases.keys()):
                time_series = ""
                time_series += "daily_cases,"
                time_series += "name=" + StringUtil.canonical(state_name) + " "
                time_series += "population=" + str(state_daily_cases[sortable_date]["population"]) + ","
                time_series += "value=" + str(state_daily_cases[sortable_date]["value"]) + " "
                time_series += state_daily_cases[sortable_date]["epoch_date"]

                self.influx_api.write(time_series)
