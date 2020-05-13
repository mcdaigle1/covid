#!/usr/bin/env python3

import csv
import glob
import requests
from date_util import date_util
from file_util import file_util
from string_util import string_util
from math_util import math_util
from state_data import StateData
from state_population import StatePopulation
from state_trend_util import StateTrendUtil

data_dir = "/var/lib/covid/data/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/"
API_ENDPOINT = "http://localhost:8086/write?db=covid"

state_data = StateData()
all_state_data = {}
state_populations = StatePopulation()

input_files = [f for f in glob.glob("/var/lib/covid/data/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/*.csv")]

# populate state data from files
# for input_file in input_files:
#     first_line = True
#     sortable_date = file_util.file_to_sortable_date(input_file)
#     with open(input_file) as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         for row in csv_reader:
#             if first_line:
#                 first_line = False
#             else:
#                 if row[1] == "US" and row[2] != "" and row[0] != "Recovered":
#                     state_row = {}
#                     state_row["state"] = row[0]
#                     state_row["country"] = row[1]
#                     state_row["last_update"] = row[2]
#                     state_row["lat"] = row[3]
#                     state_row["long"] = row[4]
#                     state_row["confirmed"] = row[5]
#                     state_row["cum_deaths"] = row[6]
#                     state_row["recovered"] = row[7]
#                     state_row["active"] = row[8]
#                     state_row["fips"] = row[9]
#                     state_row["incident_rate"] = row[10]
#                     state_row["people_tested"] = row[11]
#                     state_row["people_hospitalized"] = row[12]
#                     state_row["mortality_rate"] = row[13]
#                     state_row["uid"] = row[14]
#                     state_row["iso3"] = row[15]
#                     state_row["testing_rate"] = row[16]
#                     state_row["hopitalization_rate"] = row[17]
#                     state_row["population"] = state_populations.get_state_population(row[0])
#
#                     state_row["epoch_date"] = date_util.date_to_epoch(sortable_date)
#
#                     state_name = row[0]
#                     if state_name in all_state_data:
#                         all_state_data[state_name][sortable_date] = state_row
#                     else:
#                         all_state_data[state_name] = {sortable_date: state_row}
#
# for state_name in all_state_data:
#     state_data.add_state_data(all_state_data[state_name])
    
# rates are cumulative, so calculate daily death rates base on delta from previous day's count
all_state_daily_deaths = {}
for state_name in all_state_data:
    all_state_daily_deaths[state_name] = {}
    first_row = True
    state_data = all_state_data[state_name]
    for sortable_date in sorted(state_data.keys()):
        if first_row:
            cum_deaths_yesterday = int(state_data[sortable_date]["cum_deaths"])
            first_row = False
        else:
            cum_deaths = int(state_data[sortable_date]["cum_deaths"])
            daily_deaths = cum_deaths - cum_deaths_yesterday
            all_state_daily_deaths[state_name][sortable_date] = {}
            all_state_daily_deaths[state_name][sortable_date]["value"] = daily_deaths
            all_state_daily_deaths[state_name][sortable_date]["population"] = str(state_populations.get_state_population(state_name))
            all_state_daily_deaths[state_name][sortable_date]["epoch_date"] = state_data[sortable_date]["epoch_date"]
            cum_deaths_yesterday = cum_deaths

for state_name in all_state_daily_deaths:
    state_daily_deaths = all_state_daily_deaths[state_name]
    for sortable_date in sorted(state_daily_deaths.keys()):
        time_series = ""
        time_series += "daily_deaths,"
        time_series += "name=" + string_util.canonical(state_name) + " "
        time_series += "population=" + str(state_daily_deaths[sortable_date]["population"]) + ","
        time_series += "value=" + str(state_daily_deaths[sortable_date]["value"]) + " "
        time_series += state_daily_deaths[sortable_date]["epoch_date"] 
        print("writing to influx: " + time_series)
        r = requests.post(url = API_ENDPOINT, data = time_series)
        print(r)


for state_name in all_state_daily_deaths:
    state_data = all_state_daily_deaths[state_name]
    trend_util = StateTrendUtil(state_data)

    min_sortable_date = min(state_data.keys())
    min_y = trend_util.get_y_for_x(state_data[min_sortable_date]["epoch_date"])
    max_sortable_date = max(state_data.keys())
    max_y = trend_util.get_y_for_x(state_data[max_sortable_date]["epoch_date"])

    time_series = ""
    time_series += "trend_daily_deaths,"
    time_series += "name=" + string_util.canonical(state_name) + " "
    time_series += "value=" + str(min_y) + " "  
    time_series += state_data[min_sortable_date]["epoch_date"] 

    print("writing to influx: " + time_series)
    r = requests.post(url = API_ENDPOINT, data = time_series)
    print(r)

    time_series = ""
    time_series += "trend_daily_deaths,"
    time_series += "name=" + string_util.canonical(state_name) + " "
    time_series += "value=" + str(max_y) + " "
    time_series += state_data[max_sortable_date]["epoch_date"]

    print("writing to influx: " + time_series)
    r = requests.post(url = API_ENDPOINT, data = time_series)
    print(r)


for state_name in all_state_daily_deaths:
    state_data = all_state_daily_deaths[state_name]

