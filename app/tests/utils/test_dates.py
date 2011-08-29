# -*- coding: utf-8 -*-

from app.utils.dates import change_timezone
import datetime
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestDates(unittest.TestCase):

    def test_change_timezone(self):
        
        source_date = datetime.datetime(2002, 10, 27, 6, 0, 0)
        self.assertEquals(change_timezone(source_date).strftime("%d/%m/%y %H:%M"), "27/10/02 15:00")
        


    
