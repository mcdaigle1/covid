#!/usr/bin/env python3

import json
from string_util import string_util
from state_avg_7_days_util import StateAvg7DaysUtil
from grafana_api import GrafanaApi

# rank state deaths by Death Per Million
class StateRankAvgVsTrendUtil:

    GRAFANA_DPM_DASH_UID = "9_lnnikGz"

    state_avg_7_days_util = None
    grafana_api = None
    all_state_ranks_avg_vs_trend = {}

    def __init__(self):
        self.grafana_api = GrafanaApi()
        self.state_avg_7_days_util = StateAvg7DaysUtil()

    def update_grafana_avg_vs_trend_dash(self):
        sorted_states_by_rank = self.sort_all_states_by_rank(self.all_state_ranks_avg_vs_trend)

        panel_content = "<br>"

        url_list = ""
        for states_by_rank in sorted_states_by_rank :
            url = "&nbsp&nbsp&nbsp<a href=\"http://covidgraf.com/grafana/d/fH0__8eZk/"
            url += "individual-state-data-view-multiple-charts-per-state?orgId=2&var-state="
            url += states_by_rank["canonical_name"] + "\">"
            url += states_by_rank["state_name"] + " (" + str(round(states_by_rank["dpm"], 2))
            url += ")</a><br>\n"
            url_list = url + url_list

        panel_content += url_list
        panel_content += "\n\n"

        dash_string = self.grafana_api.getDashByUid(StateRankDpmUtil.GRAFANA_DPM_DASH_UID)
        dash_json = json.loads(dash_string)
        for panel in dash_json["dashboard"]["panels"]:
            if panel["id"] == 4:
                panel["content"] = panel_content
        self.grafana_api.updateDash(json.dumps(dash_json))

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
