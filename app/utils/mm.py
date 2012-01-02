# -*- coding: utf-8 -*-

""" Guido's pattern to handle multimethods (http://www.artima.com/weblogs/viewpost.jsp?thread=101605) """

registry = {}

class NoSuchMethod(Exception):
    """ Fired when no suitable method was identified to handle the passed values """
    pass

class MultiMethod(object):
    
    def __init__(self, name):
        self.name = name
        self.typemap = {}
        
    def __call__(self, *args):
        types = tuple(arg.__class__ for arg in args) # a generator expression!
        function = self.typemap.get(types)
        if function is None:
            raise NoSuchMethod("No function registered to handle the types %s" % ",".join(str(typ) for typ in types))
        return function(*args)
    
    def register(self, types, function):
        if types in self.typemap:
            raise TypeError("duplicate registration")
        self.typemap[types] = function

def multimethod(*types):
    
    def register(function):
        name = function.__name__
        mm = registry.get(name)
        if mm is None:
            mm = registry[name] = MultiMethod(name)
        mm.register(types, function)
        return mm
    
    return register