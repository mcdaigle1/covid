#!/usr/bin/env python3

from state_mortality_util import StateMortalityUtil

state_mortality_util = StateMortalityUtil()
state_mortality_util.clear_state_daily_deaths_from_influxdb()
state_mortality_util.add_all_state_deaths_to_influxdb()
