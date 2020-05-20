#!/usr/bin/env python3

from state_avg_7_days_util import StateAvg7DaysUtil

state_avg_7_days_util = StateAvg7DaysUtil()
state_avg_7_days_util.clear_state_trends_from_influxdb()
state_avg_7_days_util.add_state_trends_to_influxdb()
