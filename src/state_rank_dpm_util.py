#!/usr/bin/env python3

# from math_util import math_util
# from string_util import string_util
from state_mortality_util import StateMortalityUtil
# from influx_api import InfluxApi

# rank state deaths by Death Per Million
class StateRankDpmUtil:

    state_mortality_util = None
#    influx_api = None
    all_state_ranks_dpm = {}

    def __init__(self):
        self.state_mortality_util = StateMortalityUtil()
#        self.influx_api = InfluxApi()

        all_state_daily_deaths = self.state_mortality_util.get_all_state_daily_deaths()
        for state_name in all_state_daily_deaths:
            state_daily_deaths = all_state_daily_deaths[state_name]
            last_seven_state_deaths = self.get_last_seven(state_daily_deaths)
            death_total = 0
            for state_key in last_seven_state_deaths:
                death_total += last_seven_state_deaths[state_key]["value"]
            population = last_seven_state_deaths[state_key]["population"]

            all_state_ranks_dpm[state_name] = death_total / population

            Print("state: " + state_name + ", deaths/pop last week: " + str(all_state_ranks_dpm[state_name]))

    def get_all_state_ranks_dpm(self):
        return self.all_state_trends

#     def clear_state_trends_from_influxdb(self):
#         self.influx_api.delete_measurement("trend_daily_deaths")

#     def add_state_trends_to_influxdb(self):
#         for state_name in self.all_state_trends:
#             state_trends = self.all_state_trends[state_name]
#
#             time_series = ""
#             time_series += "trend_daily_deaths,"
#             time_series += "name=" + string_util.canonical(state_name) + " "
#             time_series += "value=" + str(state_trends["y_min"]) + " "
#             time_series += state_trends["min_epoch"]
#
#             self.influx_api.write(time_series)
#
#             time_series = ""
#             time_series += "trend_daily_deaths,"
#             time_series += "name=" + string_util.canonical(state_name) + " "
#             time_series += "value=" + str(state_trends["y_max"]) + " "
#             time_series += state_trends["max_epoch"]
#
#             self.influx_api.write(time_series)

    def get_last_seven(self, state_daily_deaths):
        sorted_keys = sorted(state_daily_deaths.keys())
        seven_states = {}
        for key in  sorted_keys[-7:]:
            seven_states[key] = state_daily_deaths[key]
        return seven_states
