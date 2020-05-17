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
        print("headers:")
        print(headers)

        print("query grafana: " + url)
        r = requests.get(url, headers=headers)
        print("response: " + r.text)
