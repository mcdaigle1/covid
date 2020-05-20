#!/usr/bin/env python3

from math_util import math_util
from string_util import string_util
from state_mortality_util import StateMortalityUtil
from state_trend_util import StateTrendUtil
from influx_api import InfluxApi

class StateAvg7DaysUtil:

    state_mortality_util = None
    state_trend_util = None
    influx_api = None
    all_state_avgs = {}

    def __init__(self):
        self.state_mortality_util = StateMortalityUtil()
        self.state_trend_util = StateTrendUtil()
        self.influx_api = InfluxApi()

        all_state_daily_deaths = self.state_mortality_util.get_all_state_daily_deaths()
        for state_name in all_state_daily_deaths:
            state_daily_death = all_state_daily_deaths[state_name]
            last_7_state_data = self.get_last_seven(state_daily_death)
            self.all_state_avgs[state_name] = {}

            mean_7_day_deaths = self.mean_from_state_list(last_7_state_data, "value")
            fourth_from_last_key = self.get_fourth_from_last_key(state_daily_death)
            fourth_from_last_epoch = state_daily_death[fourth_from_last_key]["epoch_date"]
            trend_slope = self.state_trend_util.get_all_state_trends()[state_name]["slope"]
            trend_y_intercept = self.state_trend_util.get_all_state_trends()[state_name]["y_intercept"]

            all_state_trends = self.state_trend_util.get_all_state_trends()
            fourth_from_last_trend_value = self.state_trend_util.get_y_for_x(fourth_from_last_epoch, trend_slope, trend_y_intercept)
            fourth_from_last_delta = mean_7_day_deaths - fourth_from_last_trend_value

            self.all_state_avgs[state_name]["mean_deaths"] = mean_7_day_deaths
            self.all_state_avgs[state_name]["fourth_from_last_trend_value"] = fourth_from_last_trend_value
            self.all_state_avgs[state_name]["fourth_from_last_delta"] = fourth_from_last_delta

        print(self.all_state_avgs)

    def get_all_state_trends(self):
        return self.all_state_trends

    def clear_state_trends_from_influxdb(self):
        self.influx_api.delete_measurement("trend_daily_deaths_seven_day")

#    def add_state_trends_to_influxdb(self):
#        for state_name in self.all_state_avgs:
#            state_trends = self.all_state_trends[state_name]
#
#            time_series = ""
#            time_series += "trend_daily_deaths_seven_day,"
#            time_series += "name=" + string_util.canonical(state_name) + " "
#            time_series += "value=" + str(state_trends["y_min"]) + " "
#            time_series += state_trends["min_epoch"]
#
#            self.influx_api.write(time_series)
#
#            time_series = ""
#            time_series += "trend_daily_deaths_seven_day,"
#            time_series += "name=" + string_util.canonical(state_name) + " "
#            time_series += "value=" + str(state_trends["y_max"]) + " "
#            time_series += state_trends["max_epoch"]
#
#            self.influx_api.write(time_series)

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

    def get_fourth_from_last_key(self, state_daily_deaths):
        sorted_keys = sorted(state_daily_deaths.keys())
        return sorted_keys[-4]
