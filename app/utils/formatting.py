# -*- coding: utf-8 -*-

""" Formatting utility methods """

import web

def spacesafe(text):
    return web.websafe(text).replace(" ", "&nbsp;").replace("\n", "<br />")

def append(s, ext):
    """ Appends ext or ext(s) to the string representation of s """
    
    if s is None:
        return None
    
    s2 = ext(s) if callable(ext) else ext
    
    return "%s%s" % (s, s2)
