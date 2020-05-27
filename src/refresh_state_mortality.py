#!/usr/bin/env python3

from if_state_mortality import IfStateMortality

if_state_mortality = IfStateMortality()
if_state_mortality.clear_measurement()
if_state_mortality.add_all_state_deaths_to_influxdb()
