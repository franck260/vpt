# -*- coding: utf-8 -*-

""" Formatting utility methods """

# TODO: more test cases
# TODO: match several languages for rank

import locale
import re
import web

# Simple formatters
first_lower = lambda s: s[:1].lower() + s[1:] if s else ""
spacesafe = lambda s: web.websafe(s).replace("\n", " <br> ")
to_rank = lambda i: "er" if i == 1 else "e"
urlize = lambda s: re.sub(r"\b(http://[^\s]+)", r"<a href='\1' target='_blank'>\1</a>", s)

def format_date(dt, frmt):
    """ Formats a date using the pre-defined locale """
    # Explicitly calls lower() due to implementation differences across platforms
    return dt.strftime(frmt).decode(locale.getlocale()[1]).lower()

def append(s, ext):
    """ Appends ext or ext(s) to the string representation of s """
    
    if s is None:
        return None
    
    s2 = ext(s) if callable(ext) else ext
    
    return "%s%s" % (s, s2)
