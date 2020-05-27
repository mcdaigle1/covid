#!/usr/bin/env python3

from if_state_cases import IfStateCases

if_state_cases = IfStateCases()
if_state_cases.clear_measurement()
if_state_cases.add_all_state_cases_to_influxdb()
