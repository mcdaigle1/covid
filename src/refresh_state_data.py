#!/usr/bin/env python3

from if_state_data import IfStateData

if_state_data = IfStateData()
if_state_data.clear_measurement()
if_state_data.add_all_state_data_to_influxdb()
