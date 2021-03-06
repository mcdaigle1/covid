#!/usr/bin/env python3

from math_util import math_util
from utils.string_util import StringUtil
from if_state_mortality import IfStateMortality
from influx_api import InfluxApi
from influx_base import InfluxBase

class IfStateTrend7Days(InfluxBase):

    if_state_mortality = None
    influx_api = None
    all_state_trends = {}

    def __init__(self):
        super().__init__("trend_daily_deaths_seven_day")
        self.if_state_mortality = IfStateMortality()
        self.influx_api = InfluxApi()

        all_state_daily_deaths = self.if_state_mortality.get_all_state_daily_deaths()
        for state_name in all_state_daily_deaths:
            state_data = all_state_daily_deaths[state_name]
            last_7_state_data = self.get_last_seven(state_data)
            self.all_state_trends[state_name] = {}

            mean_deaths = self.mean_from_state_list(last_7_state_data, "value")
            mean_epoch = self.mean_from_state_list(last_7_state_data, "epoch_date")
            slope = self.slope_from_state_list(last_7_state_data, "epoch_date", "value", mean_epoch, mean_deaths)
            y_intercept = self.get_y_intercept(mean_epoch, mean_deaths, slope)
            min_sortable_date = min(last_7_state_data.keys())
            max_sortable_date = max(last_7_state_data.keys())
            min_epoch = last_7_state_data[min_sortable_date]["epoch_date"]
            y_min = self.get_y_for_x(min_epoch, slope, y_intercept)
            max_epoch = last_7_state_data[max_sortable_date]["epoch_date"]
            y_max = self.get_y_for_x(max_epoch, slope, y_intercept)

            self.all_state_trends[state_name]["mean_deaths"] = mean_deaths
            self.all_state_trends[state_name]["mean_epoch"] = mean_epoch
            self.all_state_trends[state_name]["slope"] = slope
            self.all_state_trends[state_name]["y_intercept"] = y_intercept
            self.all_state_trends[state_name]["min_sortable_date"] = min_sortable_date
            self.all_state_trends[state_name]["min_epoch"] = min_epoch
            self.all_state_trends[state_name]["y_min"] = y_min
            self.all_state_trends[state_name]["max_sortable_date"] = max_sortable_date
            self.all_state_trends[state_name]["max_epoch"] = max_epoch
            self.all_state_trends[state_name]["y_max"] = y_max

    def get_all_state_trends(self):
        return self.all_state_trends

    def add_state_trends_to_influxdb(self):
        for state_name in self.all_state_trends:
            state_trends = self.all_state_trends[state_name]

            time_series = ""
            time_series += "trend_daily_deaths_seven_day,"
            time_series += "name=" + StringUtil.canonical(state_name) + " "
            time_series += "value=" + str(state_trends["y_min"]) + " "
            time_series += state_trends["min_epoch"]

            self.influx_api.write(time_series)

            time_series = ""
            time_series += "trend_daily_deaths_seven_day,"
            time_series += "name=" + StringUtil.canonical(state_name) + " "
            time_series += "value=" + str(state_trends["y_max"]) + " "
            time_series += state_trends["max_epoch"]

            self.influx_api.write(time_series)

    def mean_from_state_list(self, state_list, key):
        list_len = len(state_list)
        item_sum = 0
        for date in state_list:
            item_sum += int(state_list[date][key])
        return item_sum / list_len

    def slope_from_state_list(self, state_list, x_key, y_key, x_mean, y_mean):
        numerator = 0
        denominator = 0
        for date in state_list:
            x_value = state_list[date][x_key]
            y_value = state_list[date][y_key]
            numerator += (float(x_value) - float(x_mean)) * (float(y_value) - float(y_mean))
            denominator += (float(x_value) - float(x_mean)) * (float(x_value) - float(x_mean))
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        return slope

    def get_y_intercept(self, x_mean, y_mean, slope):
        return y_mean - (slope * x_mean)

    def get_y_for_x(self, x, slope, y_intercept):
        return (float(slope) * float(x)) + float(y_intercept)

    def get_last_seven(self, state_daily_deaths):
        sorted_keys = sorted(state_daily_deaths.keys())
        seven_states = {}
        for key in  sorted_keys[-7:]:
            seven_states[key] = state_daily_deaths[key]
        return seven_states
