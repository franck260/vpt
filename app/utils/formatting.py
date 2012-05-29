# -*- coding: utf-8 -*-

""" Formatting utility methods """

# TODO: more test cases
# TODO: match several languages for rank

import locale
import re
import web

# Simple formatters
first_lower = lambda s: s[:1].lower() + s[1:] if s else ""
spacesafe = lambda s: web.websafe(s).replace("\n", " <br /> ") # no more .replace(" ", "&nbsp;")
to_rank = lambda i: "er" if i == 1 else "e"
urlize = lambda s: re.sub(r"\b(http://[^\s]+)", r"<a href='\1' target='_blank'>\1</a>", s)
uncapitalize = lambda s: s[0].lower() + s[1:] if s else s

# Ajax image generator
ajax_animation = lambda id: "<img style=\"display: none;\" id=\"%s\" src=\"/public/img/ajax-loader.gif\" />" % id

# Script generators
include_js = lambda script_name: "<script type=\"text/javascript\" src=\"/public/js/%s\"></script>" % script_name
INCLUDE_JQUERY = include_js("jquery-1.7.2.min.js")
INCLUDE_JQUERYUI = "%s\n%s" % (include_js("jquery-ui-1.8.20.custom.min.js"), include_js("jquery.ui.datepicker-fr.js"))
INCLUDE_JQUERY_WITH_FORMS = "%s\n%s" % (INCLUDE_JQUERY, include_js("forms.js"))

# CSS generator
include_css = lambda css_name: "<link href=\"/public/css/%s\" rel=\"stylesheet\" type=\"text/css\"/>" % css_name

def format_date(dt, format):
    """ Hackish method to properly format a date no matter the actual locale - returns unicode """
    return dt.strftime(format).decode(locale.getlocale()[1])

def append(s, ext):
    """ Appends ext or ext(s) to the string representation of s """
    
    if s is None:
        return None
    
    s2 = ext(s) if callable(ext) else ext
    
    return "%s%s" % (s, s2)
