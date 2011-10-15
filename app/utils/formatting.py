# -*- coding: utf-8 -*-

""" Formatting utility methods """

# TODO: test ajax_animation & rank
# TODO: match several languages for rank

import locale
import re
import web

first_lower = lambda s: s[:1].lower() + s[1:] if s else ""
spacesafe = lambda s: web.websafe(s).replace("\n", " <br /> ") # no more .replace(" ", "&nbsp;")
to_rank = lambda i: "er" if i == 1 else "e"
ajax_animation = lambda id: "<img style=\"display: none;\" id=\"%s\" src=\"/public/img/ajax-loader.gif\" />" %id
urlize = lambda s: re.sub(r"\b(http://[^\s]+)", r"<a href='\1' target='_blank'>\1</a>", s)

def format_date(dt, format):
    """ Hackish method to properly format a date no matter the actual locale - returns unicode """
    return dt.strftime(format).decode(locale.getlocale()[1])

def append(s, ext):
    """ Appends ext or ext(s) to the string representation of s """
    
    if s is None:
        return None
    
    s2 = ext(s) if callable(ext) else ext
    
    return "%s%s" % (s, s2)
