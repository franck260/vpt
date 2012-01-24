# -*- coding: utf-8 -*-

""" HTTP-related utility methods """
from web import config
import web

try:
    import json
except ImportError:
    import simplejson as json 

HTTP_OK = "200 OK"
HTTP_SEE_OTHER = "303 See Other"

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

def sqlalchemy_wrapper(func):
    """ Convenient decorator to manually surround a method with a commit """
    
    def wrapped_func(*args):
        sqlalchemy_processor(lambda: func(*args))
            
    return wrapped_func

def sqlalchemy_processor(handler):
    """ Makes sure a commit appends at the end of each request """
    try:
        return handler()
    except web.HTTPError:
        config.orm.commit()
        raise
    except:
        config.orm.rollback()
        raise
    finally:
        config.orm.commit()

def init_hooks():
    """ Initializes an empty hooks list inside the context at the beginning of every request """
    web.ctx.post_request_hooks = []
    
def register_hook(hook):
    """ Appends the provided hook (which must be executable) to the hooks list for further execution """
    web.ctx.post_request_hooks.append(hook)
    
def execute_hooks():
    """ If the request is successful, executes every hook submitted by the controllers """
    if web.ctx.status in (HTTP_OK, HTTP_SEE_OTHER):
        [hook() for hook in web.ctx.post_request_hooks]
