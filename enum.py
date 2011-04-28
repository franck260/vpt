# -*- coding: utf-8 -*-

'''
Created on 3 avr. 2011

@author: Franck
'''

class Enum(set):
    
    def __getattr__(self, value):
        
        for item in self:
            if item.value == value:
                return item
            
        raise AttributeError

class Status:
    
    def __init__(self, value, long_value):
        self.value = value
        self.long_value = long_value
        
    def __eq__(self, other):
        return self.value == other.value
    
    def __ne__(self, other):
        return self.value != other.value
    
    def __repr__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)
    
