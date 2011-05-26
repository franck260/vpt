# -*- coding: utf-8 -*-

from app.utils.formatting import spacesafe, append
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# TODO: le __init__ du paquetage père initialise tout le stack applicatif de test !


class TestUtils(unittest.TestCase):

    def test_spacesafe(self):
        
        self.assertEquals(spacesafe("test"), "test")
        self.assertEquals(spacesafe("test with space"), "test&nbsp;with&nbsp;space")
        self.assertEquals(spacesafe("test with space and\nbackslash"), "test&nbsp;with&nbsp;space&nbsp;and<br />backslash")
        
    def test_append(self):
        
        self.assertIsNone(append(None, None))
        self.assertIsNone(append(None, lambda s: "42"))
        self.assertEquals(append("spam", lambda s: " 42"), "spam 42")
        self.assertEquals(append("eggs", " 42"), "eggs 42")
        self.assertEquals(append(1, lambda s: "er" if s == 1 else "e"), "1er")
        self.assertEquals(append(7, lambda s: "er" if s == 1 else "e"), "7e")
        self.assertEquals(append(8, "e"), "8e")

    
