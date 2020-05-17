#!/usr/bin/env python3

import requests

class GrafanaApi:

    GRAFANA_API_LOCATION = "/etc/covid/grafana_api.cfg"
    GRAFANA_API_URL = "http://covidgraf.com/grafana/api/"

    grafana_api_key = ""

    def __init__(self):
        f = open(GrafanaApi.GRAFANA_API_LOCATION, "r")
        self.grafana_api_key = f.read().rstrip('\n')

    def getDashByUid(self, uid):
        url = GrafanaApi.GRAFANA_API_URL + "dashboards/uid/" + uid
        headers = {}
        headers["Authorization"] = 'Bearer ' + self.grafana_api_key

        r = requests.get(url, headers=headers)
        return r.text

    def updateDash(self, json_string):

        url = GrafanaApi.GRAFANA_API_URL + "dashboards/db"
        headers = {}
        headers["Authorization"] = 'Bearer ' + self.grafana_api_key
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"

        r = requests.post(url, headers=headers, data=json_string)
