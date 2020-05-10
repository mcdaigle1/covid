#!/usr/bin/env python3

import csv
import glob
import requests
from datetime import datetime
from math_util import math_util

data_dir = "/var/lib/covid/data/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/"
pop_csv_path = "/home/mdaigle/covid/data/state_population.csv"
API_ENDPOINT = "http://localhost:8086/write?db=covid"

all_state_data = {}
state_populations = {}

input_files = [f for f in glob.glob("/var/lib/covid/data/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/*.csv")]

# extract the file time from the full input file path.
def file_to_sortable_date(file_path):
    split_string = file_path.split('/')[-1].split('.')[0].split('-')
    return split_string[2] + split_string[0] + split_string[1]

# convert a date from the file, like: 2020-04-12 23:18:15 to an epoch date representing 00:00:00 that day
def date_to_epoch(raw_date):
    cal_date = raw_date.split(' ')[0]
    return  datetime.strptime(cal_date, "%Y%m%d").strftime('%s') + "000000000"

def canonical(noncannonical_string):
    return noncannonical_string.replace(" ", "_") 

def default_zero(some_number):
    if some_number == "":
        return "0"
    else:
        return str(some_number)    


# create state population dict from file
first_row = True
with open(pop_csv_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if first_row:
            first_row = False
        else:
            state = row[1]
            population = row[2]
            state_populations[state] = population


# populate state data from files
for input_file in input_files:
    first_line = True
    sortable_date = file_to_sortable_date(input_file)
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if first_line:
                first_line = False
            else:
                if row[1] == "US" and row[2] != "" and row[0] != "Recovered":
                    state_row = {};
                    state_row["state"] = row[0]
                    state_row["country"] = row[1]
                    state_row["last_update"] = row[2]
                    state_row["lat"] = row[3]
                    state_row["long"] = row[4]
                    state_row["confirmed"] = row[5]
                    state_row["cum_deaths"] = row[6]
                    state_row["recovered"] = row[7]
                    state_row["active"] = row[8]
                    state_row["fips"] = row[9]
                    state_row["incident_rate"] = row[10]
                    state_row["people_tested"] = row[11]
                    state_row["people_hospitalized"] = row[12]
                    state_row["mortality_rate"] = row[13]
                    state_row["uid"] = row[14]
                    state_row["iso3"] = row[15]
                    state_row["testing_rate"] = row[16]
                    state_row["hopitalization_rate"] = row[17]
               
                    state_row["epoch_date"] = date_to_epoch(sortable_date)

                    state_name = row[0]
                    if state_name in all_state_data:
                        all_state_data[state_name][sortable_date] = state_row
                    else:
                        all_state_data[state_name] = {sortable_date: state_row}
                

for state_name in all_state_data:
    if state_name in state_populations:
        state_population = state_populations[state_name]
    else:
        state_population = 0

    # print("processing state " + state_name)
    state_data = all_state_data[state_name]
    for sortable_date in sorted(state_data.keys()):
        time_series = ""
        time_series += "state_data,"

        time_series += "name=" + canonical(state_name) + ","
        time_series += "country=" + state_data[sortable_date]["country"] + " "

        time_series += "state=\"" + state_name + "\","
        time_series += "population=" + default_zero(state_population) + ","
        time_series += "last_update=\"" + state_data[sortable_date]["last_update"] + "\","
        time_series += "lat=" + default_zero(state_data[sortable_date]["lat"]) + ","
        time_series += "long=" + default_zero(state_data[sortable_date]["long"]) + ","
        time_series += "confirmed=" + default_zero(state_data[sortable_date]["confirmed"]) + ","
        time_series += "cum_deaths=" + default_zero(state_data[sortable_date]["cum_deaths"]) + ","
        time_series += "recovered=" + default_zero(state_data[sortable_date]["recovered"]) + ","
        time_series += "active=" + default_zero(state_data[sortable_date]["active"]) + ","
        time_series += "fips=" + state_data[sortable_date]["fips"] + ","
        time_series += "incident_rate=" + default_zero(state_data[sortable_date]["incident_rate"]) + ","
        time_series += "people_tested=" + default_zero(state_data[sortable_date]["people_tested"]) + ","
        time_series += "people_hospitalized=" + default_zero(state_data[sortable_date]["people_hospitalized"]) + ","
        time_series += "mortality_rate=" + default_zero(state_data[sortable_date]["mortality_rate"]) + ","
        time_series += "uid=" + state_data[sortable_date]["uid"] + ","
        time_series += "iso3=\"" + state_data[sortable_date]["iso3"] + "\","
        time_series += "testing_rate=" + default_zero(state_data[sortable_date]["testing_rate"]) + ","
        time_series += "hopitalization_rate=" + default_zero(state_data[sortable_date]["hopitalization_rate"]) + " "

        time_series += state_data[sortable_date]["epoch_date"] 

        print("writing to influx: " + time_series)
        r = requests.post(url = API_ENDPOINT, data = time_series)
        print(r)
            

# rates are cumulative, so calculate daily death rates base on delta from previous day's count
all_state_daily_deaths = {}
for state_name in all_state_data:
    if state_name in state_populations:
        state_population = state_populations[state_name]
    else:
        state_population = 0

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
            all_state_daily_deaths[state_name][sortable_date]["population"] = default_zero(state_population)
            all_state_daily_deaths[state_name][sortable_date]["epoch_date"] = state_data[sortable_date]["epoch_date"]
            cum_deaths_yesterday = cum_deaths

for state_name in all_state_daily_deaths:
    state_daily_deaths = all_state_daily_deaths[state_name]
    for sortable_date in sorted(state_daily_deaths.keys()):
        time_series = ""
        time_series += "daily_deaths,"
        time_series += "name=" + canonical(state_name) + " "
        time_series += "population=" + str(state_daily_deaths[sortable_date]["population"]) + ","
        time_series += "value=" + str(state_daily_deaths[sortable_date]["value"]) + " "
        time_series += state_daily_deaths[sortable_date]["epoch_date"] 
        print("writing to influx: " + time_series)
        r = requests.post(url = API_ENDPOINT, data = time_series)
        print(r)


for state_name in all_state_daily_deaths:
    state_data = all_state_daily_deaths[state_name]
    mean_deaths = math_util.mean_from_state_list(state_data, "value")
    mean_epoch = math_util.mean_from_state_list(state_data, "epoch_date")
    slope = math_util.slope_from_state_list(state_data, "epoch_date", "value", mean_epoch, mean_deaths)
    y_intercept = math_util.get_y_intercept(mean_epoch, mean_deaths, slope)

    min_sortable_date = min(state_data.keys())
    min_y = math_util.get_y_for_x(state_data[min_sortable_date]["epoch_date"], slope, y_intercept)
    max_sortable_date = max(state_data.keys())
    max_y = math_util.get_y_for_x(state_data[max_sortable_date]["epoch_date"], slope, y_intercept)

    time_series = ""
    time_series += "trend_daily_deaths,"
    time_series += "name=" + canonical(state_name) + " "
    time_series += "value=" + str(min_y) + " "  
    time_series += state_data[min_sortable_date]["epoch_date"] 

    print("writing to influx: " + time_series)
    r = requests.post(url = API_ENDPOINT, data = time_series)
    print(r)

    time_series = ""
    time_series += "trend_daily_deaths,"
    time_series += "name=" + canonical(state_name) + " "
    time_series += "value=" + str(max_y) + " "
    time_series += state_data[max_sortable_date]["epoch_date"]

    print("writing to influx: " + time_series)
    r = requests.post(url = API_ENDPOINT, data = time_series)
    print(r)
