# -*- coding: utf-8 -*-

class Enum(set):
    """ Simple enumeration class """
    
    def __getattr__(self, name):
        if name in self:
            return unicode(name)
        raise AttributeError