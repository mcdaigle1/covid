#!/usr/bin/env python3

class math_util:
    @staticmethod
    def mean_from_state_list(state_list, key):
        list_len = len(state_list)
        item_sum = 0
        for date in state_list:
            item_sum += int(state_list[date][key])
        return item_sum / list_len

    @staticmethod
    def slope_from_state_list(state_list, x_key, y_key, x_mean, y_mean):
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
        
    @staticmethod
    def get_y_intercept(x_mean, y_mean, slope):
        return y_mean - (slope * x_mean)

    @staticmethod
    def get_y_for_x(x, slope, y_intercept):
        return (float(slope) * float(x)) + float(y_intercept)

