#!/usr/bin/env python3

class file_util:

    @staticmethod
    # convert a date from the file, like: 2020-04-12 23:18:15 to an epoch date representing 00:00:00 that day
    # extract the file time from the full input file path.
    def file_to_sortable_date(file_path):
        split_string = file_path.split('/')[-1].split('.')[0].split('-')
        return split_string[2] + split_string[0] + split_string[1]

