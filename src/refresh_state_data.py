#!/usr/bin/env python3

from state_data import StateData

state_data = StateData()
state_data.clear_state_data_from_influxdb()
state_data.add_all_state_data_to_influxdb
    
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

