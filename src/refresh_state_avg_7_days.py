#!/usr/bin/env python3

from if_state_avg_7_days import IfStateAvg7Days

if_state_avg_7_days = IfStateAvg7Days()
if_state_avg_7_days.clear_measurement()
if_state_avg_7_days.add_state_avg_7_day_to_influxdb()
