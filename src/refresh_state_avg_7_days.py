#!/usr/bin/env python3

from state_trend_7_days_util import StateTrend7DaysUtil

state_trend_7_days_util = StateTrend7DaysUtil()
state_trend_7_days_util.clear_state_trends_from_influxdb()
state_trend_7_days_util.add_state_trends_to_influxdb()
