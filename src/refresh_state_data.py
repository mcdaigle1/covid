#!/usr/bin/env python3

from state_data_util import StateDataUtil

state_data_util = StateDataUtil()
state_data_util.clear_measurement()
state_data_util.add_all_state_data_to_influxdb()
