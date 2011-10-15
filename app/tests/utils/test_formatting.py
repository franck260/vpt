# -*- coding: utf-8 -*-

from app.utils.formatting import spacesafe, append, first_lower, format_date, \
    urlize
import datetime
import locale
import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# TODO: the __init__ method initializes too many things

class TestFormatting(unittest.TestCase):

    def test_first_lower(self):
        
        self.assertEquals(first_lower(None), "")
        self.assertEquals(first_lower(""), "")
        self.assertEquals(first_lower("Hey buddies"), "hey buddies")
        self.assertEquals(first_lower("Hey Buddies"), "hey Buddies")

    def test_spacesafe(self):
        
        self.assertEquals(spacesafe("test"), "test")
        # self.assertEquals(spacesafe("test with space"), "test&nbsp;with&nbsp;space")
        self.assertEquals(spacesafe("test with space"), "test with space")
        # self.assertEquals(spacesafe("test with space and\nbackslash"), "test&nbsp;with&nbsp;space&nbsp;and<br />backslash")
        self.assertEquals(spacesafe("test with space and\nbackslash"), "test with space and <br /> backslash")
        
    def test_urlize(self):
        
        self.assertEquals(urlize("test"), "test")
        self.assertEquals(urlize("http://www.google.com"), "<a href='http://www.google.com' target='_blank'>http://www.google.com</a>")
        self.assertEquals(urlize("Lien 1 : http://www.google.com <br /> et lien 2 : http://microsoft.com"),
                                 "Lien 1 : <a href='http://www.google.com' target='_blank'>http://www.google.com</a> <br /> et lien 2 : <a href='http://microsoft.com' target='_blank'>http://microsoft.com</a>")
    
    def test_format_date(self):

        # Enforces the locale
        if sys.platform == "win32":
            locale.setlocale(locale.LC_ALL, "fra")
        else:
            locale.setlocale(locale.LC_ALL, "fr_FR")
        
        # Testing parameters
        DATE_FORMAT = "%A %d %B %Y"
        JULY_15 = datetime.date(2011, 7, 15)
        AUGUST_15 = datetime.date(2011, 8, 15)
        DECEMBER_15 = datetime.date(2011, 12, 15)
        
        # Checks that French dates are properly formatted
        formatted_dt = format_date(JULY_15, DATE_FORMAT)
        self.assertIsInstance(formatted_dt, unicode)
        self.assertEqual(formatted_dt, u"vendredi 15 juillet 2011")
        
        formatted_dt = format_date(AUGUST_15, DATE_FORMAT)
        self.assertIsInstance(formatted_dt, unicode)
        self.assertEqual(formatted_dt, u"lundi 15 août 2011")
        
        formatted_dt = format_date(DECEMBER_15, DATE_FORMAT)
        self.assertIsInstance(formatted_dt, unicode)
        self.assertEqual(formatted_dt, u"jeudi 15 décembre 2011")
    
    def test_append(self):
        
        self.assertIsNone(append(None, None))
        self.assertIsNone(append(None, lambda s: "42"))
        self.assertEquals(append("spam", lambda s: " 42"), "spam 42")
        self.assertEquals(append("eggs", " 42"), "eggs 42")
        self.assertEquals(append(1, lambda s: "er" if s == 1 else "e"), "1er")
        self.assertEquals(append(7, lambda s: "er" if s == 1 else "e"), "7e")
        self.assertEquals(append(8, "e"), "8e")

    
