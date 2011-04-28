# -*- coding: utf-8 -*-

'''
Created on 16 mars 2011

@author: Franck
'''

from app.tests import WebTestCase, UserData
from app.utils import session
import config
import web

HTTP_OK = "200 OK"
HTTP_SEE_OTHER = "303 See Other"
HTTP_NOT_FOUND = "404 Not Found"

class ControllerTestCase(WebTestCase):
    """ Superclasse des tests des contrôleurs """
    
    def login(self, user_id = 1, password = "secret"):
        session.get_manager().login(user_id, password)
        
    def logout(self):
        session.get_manager().logout()
    
    def tearDown(self):
        super(ControllerTestCase, self).tearDown()
        self.logout()

