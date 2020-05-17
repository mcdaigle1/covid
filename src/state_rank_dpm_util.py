#!/usr/bin/env python3

import json
from string_util import string_util
from state_mortality_util import StateMortalityUtil
from grafana_api import GrafanaApi

# rank state deaths by Death Per Million
class StateRankDpmUtil:

    GRAFANA_DPM_DASH_UID = "cFA9bBgGk"

    state_mortality_util = None
    all_state_ranks_dpm = {}

    def __init__(self):
        self.grafana_api = GrafanaApi()
        self.state_mortality_util = StateMortalityUtil()

        all_state_daily_deaths = self.state_mortality_util.get_all_state_daily_deaths()
        for state_name in all_state_daily_deaths:
            state_daily_deaths = all_state_daily_deaths[state_name]
            last_seven_state_deaths = self.get_last_seven(state_daily_deaths)
            death_total = 0
            for state_key in last_seven_state_deaths:
                death_total += last_seven_state_deaths[state_key]["value"]
            population = last_seven_state_deaths[state_key]["population"]

            if int(population) > 0:
                self.all_state_ranks_dpm[state_name] = int(death_total) / int(population) * 1000000

    def update_grafana_dpm_dash(self):
        sorted_states_by_rank = self.sort_all_states_by_rank(self.all_state_ranks_dpm)

        panel_content = "\nStates ranked by death per million in the last seven days\n<br><br>\n\n"

        for states_by_rank in reversed(sorted_states_by_rank) :
            print(states_by_rank)
         #   <a href=\"http://covidgraf.com/grafana/d/fH0__8eZk/individual-state-data-view-multiple-charts-per-state?orgId=2&var-state=Arkansas\">Arkansas (50)</a><br>\n"
         #   <a href=\"http://covidgraf.com/grafana/d/fH0__8eZk/individual-state-data-view-multiple-charts-per-state?orgId=2&var-state=Arkansas\">Kansas (25)</a><br>\n"

            panel_content += "\n\n"

        dash_string = self.grafana_api.getDashByUid(StateRankDpmUtil.GRAFANA_DPM_DASH_UID)
        dash_json = json.loads(dash_string)
        print(json.dumps(dash_json["dashboard"]["panels"][0]["content"]))

    def get_all_state_ranks_dpm(self):
        return self.all_state_trends

    def get_last_seven(self, state_daily_deaths):
        sorted_keys = sorted(state_daily_deaths.keys())
        seven_states = {}
        for key in  sorted_keys[-7:]:
            seven_states[key] = state_daily_deaths[key]
        return seven_states

    def sort_all_states_by_rank(self, all_state_ranks_dpm):
        sorted_states = []

        for state_name in all_state_ranks_dpm:
            state_record = {
                "state_name" : state_name,
                "dpm" : float(all_state_ranks_dpm[state_name]),
                "canonical_name" : string_util.canonical(state_name)}
            inserted = False
            for x in range(len(sorted_states)):
                if state_record["dpm"] < sorted_states[x]["dpm"] and inserted == False:
                    sorted_states.insert(x, state_record)
                    inserted = True
            if inserted == False:
                sorted_states.insert(len(sorted_states), state_record)

        return sorted_states
