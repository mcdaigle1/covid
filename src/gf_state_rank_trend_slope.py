#!/usr/bin/env python3

import json
from utils.string_util import StringUtil
from if_state_trend import IfStateTrend
from grafana_api import GrafanaApi

# rank state deaths by Death Per Million
class GfStateRankTrendSlope:

    GRAFANA_DPM_DASH_UID = "jBx1_ZzMz"
    NANOSECONDS_IN_DAY = 86400000000000

    if_state_avg_7_days = None
    grafana_api = None
    all_state_ranks_trend_slope = {}

    def __init__(self):
        self.grafana_api = GrafanaApi()
        self.if_state_trend = IfStateTrend()

    def update_grafana_trend_slope_dash(self):
        all_state_trends = self.if_state_trend.get_all_state_trends()
        sorted_states_by_rank = self.sort_all_states_by_rank(all_state_trends)

        panel_content = "<br>"

        url_list = ""
        for states_by_rank in sorted_states_by_rank :
            url = "&nbsp&nbsp&nbsp<a href=\"http://covidgraf.com/grafana/d/fH0__8eZk/"
            url += "individual-state-data-view-multiple-charts-per-state?orgId=2&var-state="
            url += states_by_rank["canonical_name"] + "\">"
            url += states_by_rank["state_name"]
            url += " (" + str(round(states_by_rank["slope"] * GfStateRankTrendSlope.NANOSECONDS_IN_DAY, 2))
            url += ")</a><br>\n"
            url_list = url + url_list

        panel_content += url_list
        panel_content += "\n\n"

        dash_string = self.grafana_api.getDashByUid(GfStateRankTrendSlope.GRAFANA_DPM_DASH_UID)
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

    def sort_all_states_by_rank(self, all_state_ranks_trend_slope):
        sorted_states = []

        for state_name in all_state_ranks_trend_slope:
            state_ranks_avg_vs_trend = all_state_ranks_trend_slope[state_name]
            state_record = {
                "state_name" : state_name,
                "slope" : float(state_ranks_avg_vs_trend["slope"]),
                "canonical_name" : StringUtil.canonical(state_name)}
            inserted = False
            for x in range(len(sorted_states)):
                if state_record["slope"] < sorted_states[x]["slope"] and inserted == False:
                    sorted_states.insert(x, state_record)
                    inserted = True
            if inserted == False:
                sorted_states.insert(len(sorted_states), state_record)

        return sorted_states
