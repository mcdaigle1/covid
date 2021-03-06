#!/usr/bin/env python3

from utils.string_util import StringUtil
from influx_api import InfluxApi
from influx_base import InfluxBase
from if_state_data import IfStateData
from state_population import StatePopulation

class IfStateMortality(InfluxBase):

    all_state_daily_deaths = {}
    influx_api = None
    state_populations = None
    if_state_data = None

    def __init__(self):
        super().__init__("daily_deaths")
        self.state_populations = StatePopulation()
        self.if_state_data = IfStateData()
        self.influx_api = InfluxApi()

        all_state_data = self.if_state_data.get_all_state_data()
        for state_name in all_state_data:
            self.all_state_daily_deaths[state_name] = {}
            first_row = True
            state_data = all_state_data[state_name]
            for sortable_date in sorted(state_data.keys()):
                if first_row:
                    cum_deaths_yesterday = int(state_data[sortable_date]["cum_deaths"])
                    first_row = False
                else:
                    cum_deaths = int(state_data[sortable_date]["cum_deaths"])
                    daily_deaths = cum_deaths - cum_deaths_yesterday
                    self.all_state_daily_deaths[state_name][sortable_date] = {}
                    self.all_state_daily_deaths[state_name][sortable_date]["value"] = daily_deaths
                    self.all_state_daily_deaths[state_name][sortable_date]["population"] = str(self.state_populations.get_state_population(state_name))
                    self.all_state_daily_deaths[state_name][sortable_date]["epoch_date"] = state_data[sortable_date]["epoch_date"]
                    cum_deaths_yesterday = cum_deaths

    def get_all_state_daily_deaths(self):
        return self.all_state_daily_deaths

    def add_all_state_deaths_to_influxdb(self):
        for state_name in self.all_state_daily_deaths:
            state_daily_deaths = self.all_state_daily_deaths[state_name]
            for sortable_date in sorted(state_daily_deaths.keys()):
                time_series = ""
                time_series += "daily_deaths,"
                time_series += "name=" + StringUtil.canonical(state_name) + " "
                time_series += "population=" + str(state_daily_deaths[sortable_date]["population"]) + ","
                time_series += "value=" + str(state_daily_deaths[sortable_date]["value"]) + " "
                time_series += state_daily_deaths[sortable_date]["epoch_date"]

                self.influx_api.write(time_series)
