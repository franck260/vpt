# -*- coding: utf-8 -*-

""" Date-related utility methods """

from pytz import timezone

PACIFIC = timezone("US/Pacific-New")
PARIS = timezone("Europe/Paris")

#TODO: store all dates in UTC and remove the hard-coded references here !

def change_timezone(dt, source_timezone = PACIFIC, target_timezone = PARIS):
    """ Returns a new date based on the timezones provided """
    return source_timezone.localize(dt).astimezone(target_timezone)