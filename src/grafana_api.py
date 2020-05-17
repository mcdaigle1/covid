#!/usr/bin/env python3

#import requests

class GrafanaApi:

    GRAFANA_API_LOCATION = "/etc/covid/grafana_api.cfg"
    grafana_api = ""

    def __init__(self):
        f = open(GrafanaApi.GRAFANA_API_LOCATION, "r")
        grafana_api = f.read()
        print("Grafana API: " + grafana_api)


