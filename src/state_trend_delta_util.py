#!/usr/bin/env python3

# from math_util import math_util
# from string_util import string_util
from state_mortality_util import StateMortalityUtil
from state_trend_util import StateTrendUtil
from state_trend_7_days_util import StateTrend7DaysUtil
from influx_api import InfluxApi

# Get the full and seven day trend data.  Do some comparisons and save in delta_daily_deaths measurement in influxdb.
# The goal is to come up with some common delta values that we can use to determine if the changes in death rates per
# state are significant.  We'll try to get a normalized delta value from:
# -- relative height of 7 day trend vs full trend
# -- differences in slope of 7 day trend vs full trend
class StateTrendDeltaUtil:

    all_state_deltas = {}

    def __init__(self):
        state_mortality_util = StateMortalityUtil()
        state_trend_util = StateTrendUtil()
        state_trend_7_days_util = StateTrend7DaysUtil()

        self.influx_api = InfluxApi()

        all_state_daily_deaths = state_mortality_util.get_all_state_daily_deaths()
        all_state_trends = state_trend_util.get_all_state_trends()
        all_state_trends_7_days = state_trend_7_days_util.get_all_state_trends()

        for state_name in all_state_trends:
            print("state: " + state_name)
            state_trends = all_state_trends[state_name]
            state_trends_7_days = all_state_trends_7_days[state_name]
            state_daily_deaths = all_state_daily_deaths[state_name]

            # get the fourth from last daily death record.  We use this to compare the height of the
            # full trend line with the seven day trend.
            daily_deaths_minus_four_key = self.get_fourth_from_last_key(state_daily_deaths)
            daily_death_minus_four = state_daily_deaths[daily_deaths_minus_four_key]
            # Get the fourth from last y value for both the full and 7 day trend.  We do this because we want to
            # compare the middle of the 7 day trend with the same day on the full trend
            trend_full_minus_four_y = state_trend_util.get_y_for_x(
                    daily_death_minus_four["epoch_date"], 
                    state_trends["slope"], 
                    state_trends["y_intercept"])
            trend_7_days_minus_four_y = state_trend_7_days_util.get_y_for_x(
                    daily_death_minus_four["epoch_date"],
                    state_trends_7_days["slope"],
                    state_trends_7_days["y_intercept"])

            normalized_delta = self.calculate_normalized_delta(
                    state_trends["slope"],
                    state_trends_7_days["slope"],
                    trend_full_minus_four_y,
                    trend_7_days_minus_four_y,
                    daily_death_minus_four[population])

            # populate the all_state_deltas structure
            self.all_state_deltas[state_name] = {}
            self.all_state_deltas[state_name]["slope_total"] = state_trends["slope"]
            self.all_state_deltas[state_name]["slope_7_day"] = state_trends_7_days["slope"]
            self.all_state_deltas[state_name]["minus_four_y"] = trend_full_minus_four_y
            self.all_state_deltas[state_name]["minus_four_y_7_day"] = trend_7_days_minus_four_y
            self.all_state_deltas[state_name]["normalized_delta"] = normalized_delta

    def get_all_state_deltas(self):
        return self.all_state_deltas

    def clear_state_deltas_from_influxdb(self):
        self.influx_api.delete_measurement("delta_daily_deaths")

    def add_state_deltas_to_influxdb(self):
        for state_name in self.all_state_deltas:
            state_trends = self.all_state_trends[state_name]

            time_series = ""
            time_series += "trend_daily_deaths,"
            time_series += "name=" + string_util.canonical(state_name) + " "
            time_series += "value=" + str(state_trends["y_min"]) + " "
            time_series += state_trends["min_epoch"]

            self.influx_api.write(time_series)

            time_series = ""
            time_series += "trend_daily_deaths,"
            time_series += "name=" + string_util.canonical(state_name) + " "
            time_series += "value=" + str(state_trends["y_max"]) + " "
            time_series += state_trends["max_epoch"]

            self.influx_api.write(time_series)

    # get the key for the fourth from the last state daily death record.  We get the fourth from last record
    # because we want to compare the height of the middle of the seven day trend with the height of the full
    # trend on the same day
    def get_fourth_from_last_key(self, state_daily_deaths):
        sorted_keys = sorted(state_daily_deaths.keys())
        return sorted_keys[-4]

    # calculate a constant delta value that represents the amount of change in the last seven day trend from the
    # full dataset trend.  This is a combination of the average height of the seven day trend relative to
    # the full trend at the same time, compared to the slope differences
    def calculate_normalized_delta(self, slope_total, slope_7_day, minus_four_y, minus_four_y_7_day, population):

        if minus_four_y == 0:
            percent_height_diff = (minus_four_y_7_day - minus_four_y) / .0001
        else:
            percent_height_diff = (minus_four_y_7_day - minus_four_y) / minus_four_y
            
        slope_diff = slope_7_day - slope_total

        print("total slope: " + str(slope_total) + ", slope 7 day; " + str(slope_7_day))
        print("slope diff: " + str(slope_diff))

        print("y total: " + str(minus_four_y) + ", 7 day y total: " + str(minus_four_y_7_day))
        print("percent height diff: " + str(percent_height_diff))
