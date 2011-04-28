# -*- coding: utf-8 -*-

'''
Created on 7 mars 2011

@author: Franck
'''

import web

def spacesafe(text):
    return web.websafe(text).replace(" ", "&nbsp;").replace("\n", "<br />")

def append(s, ext):
    """ Ajoute ext ou ext(s) à la représentation texte de s """
    
    if s is None:
        return None
    
    s2 = ext(s) if callable(ext) else ext
    
    return "%s%s" %(s, s2)