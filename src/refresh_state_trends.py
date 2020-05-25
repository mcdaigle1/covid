#!/usr/bin/env python3

from if_state_trend import IfStateTrend

if_state_trend = IfStateTrend()
if_state_trend.clear_measurement()
if_state_trend.add_state_trends_to_influxdb()
