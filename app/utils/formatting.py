# -*- coding: utf-8 -*-

""" Formatting utility methods """

import web

first_lower = lambda s: s[:1].lower() + s[1:] if s else ""

spacesafe = lambda s: web.websafe(s).replace(" ", "&nbsp;").replace("\n", "<br />")

def append(s, ext):
    """ Appends ext or ext(s) to the string representation of s """
    
    if s is None:
        return None
    
    s2 = ext(s) if callable(ext) else ext
    
    return "%s%s" % (s, s2)
