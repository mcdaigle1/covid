#!/usr/bin/env python3

from state_trend_util import StateTrendUtil

state_trend_util = StateTrendUtil()
state_trend_util.clear_state_data_from_influxdb()
state_trend_util.add_state_trends_to_influxdb()
