#!/usr/bin/env python3

import requests

class GrafanaApi:

    GRAFANA_API_LOCATION = "/etc/covid/grafana_api.cfg"
    GRAFANA_API_URL = "http://localhost:3000/grafana/api/"

    grafana_api_key = ""

    def __init__(self):
        f = open(GrafanaApi.GRAFANA_API_LOCATION, "r")
        grafana_api_key = f.read()

    def getDashByUid(self, uid):
        uid = "fH0__8eZk"

        url = GrafanaApi.GRAFANA_API_URL + "dashboards/home"
        headers = {'Authorization': 'Bearer ' + grafana_api_key}

        print("query grafana: " + url)
        r = requests.get(url, headers=headers)
        print(r)

