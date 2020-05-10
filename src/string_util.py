#!/usr/bin/env python3

class string_util:

    @staticmethod
    # convert a string to a canonical string
    def canonical(noncannonical_string):
        return noncannonical_string.replace(" ", "_")

    @staticmethod
    # return a "0" if string is empty
    def default_zero(some_number):
        if some_number == "":
            return "0"
        else:
            return str(some_number)

