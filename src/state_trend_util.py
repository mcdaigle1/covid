#!/usr/bin/env python3

from math_util import math_util

class StateTrendUtil:

    mean_deaths = 0
    mean_epoch = 0
    slope = 0
    y_intercept = 0
    x_min = 0
    y_min = 0

    def __init__(self, state_data):
        self.mean_deaths = self.mean_from_state_list(state_data, "value")
        self.mean_epoch = self.mean_from_state_list(state_data, "epoch_date")
        self.slope = self.slope_from_state_list(state_data, "epoch_date", "value", self.mean_epoch, self.mean_deaths)
        self.y_intercept = self.get_y_intercept(self.mean_epoch, self.mean_deaths, self.slope)
        min_sortable_date = min(state_data.keys())
        self.x_min = trend_util.get_y_for_x(state_data[min_sortable_date]["epoch_date"])
        max_sortable_date = max(state_data.keys())
        self.y_min = trend_util.get_y_for_x(state_data[max_sortable_date]["epoch_date"])

    def get_slope(self):
        return self.slope

    def get_mean_deaths(self):
        return self.mean_deaths

    def get_mean_epoch(self):
        return self.mean_epoch

    def get_y_intercept(self):
        return self.y_intercept

    def get_x_min(self):
        return self.x_min

    def get_y_min(self):
        return self.y_min

    def mean_from_state_list(self, state_list, key):
        list_len = len(state_list)
        item_sum = 0
        for date in state_list:
            item_sum += int(state_list[date][key])
        return item_sum / list_len

    def slope_from_state_list(self, state_list, x_key, y_key, x_mean, y_mean):
        numerator = 0
        denominator = 0
        for date in state_list:
            x_value = state_list[date][x_key]
            y_value = state_list[date][y_key]
            numerator += (float(x_value) - float(x_mean)) * (float(y_value) - float(y_mean))
            denominator += (float(x_value) - float(x_mean)) * (float(x_value) - float(x_mean))
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        return slope

    def get_y_intercept(self, x_mean, y_mean, slope):
        return y_mean - (slope * x_mean)

    def get_y_for_x(self, x):
        return (float(self.slope) * float(x)) + float(self.y_intercept)
