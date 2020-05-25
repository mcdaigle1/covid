#!/usr/bin/env python3

from if_state_cases import IfStateMortality

if_state_cases = IfStateCases()
if_state_cases.clear_measurements()
if_state_cases.add_all_state_cases_to_influxdb()
