#!/usr/bin/env python3

from datetime import datetime

class date_util:

    @staticmethod
    # convert a date from the file, like: 2020-04-12 23:18:15 to an epoch date representing 00:00:00 that day
    def date_to_epoch(raw_date):
        cal_date = raw_date.split(' ')[0]
        return  datetime.strptime(cal_date, "%Y%m%d").strftime('%s') + "000000000"

