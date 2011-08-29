# -*- coding: utf-8 -*-

""" JSON-related utility methods """

try:
    import json
except ImportError:
    import simplejson as json 
import web


def jsonify(func):
    """ Wraps a controller method. When called :
    
    0) Sets the HTTP response header to "application/json"
    1) Runs the wrapped GET/POST (which must return a Python dict !)
    2) Stringifies the returned values (typically template bodies) to make sure the output is serializable
    3) Returns a JSON-encoded dictionary """
    
    def wrapped_func(*args):        

        # Sets the HTTP header
        web.header("Content-Type", "application/json")
       
        # Runs the GET/POST and cleans the values
        results = dict((k,v and str(v) or None) for k,v in func(*args).items())
        
        # Returns a JSON-encoded dictionary
        return json.dumps(results)  
        
    return wrapped_func
