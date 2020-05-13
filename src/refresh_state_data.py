#!/usr/bin/env python3

from state_data import StateData

state_data = StateData()
state_data.clear_state_data_from_influxdb()
state_data.add_all_state_data_to_influxdb
