#!/usr/bin/env python3

from if_state_trend_7_days import IfStateTrend7Days

if_state_trend_7_days = IfStateTrend7Days()
if_state_trend_7_days.clear_measurement()
if_state_trend_7_days.add_state_trends_to_influxdb()
