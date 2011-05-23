# -*- coding: utf-8 -*-

from app.tests import WebTestCase, UserData
from app.utils import session
from web import config
import web

HTTP_OK = "200 OK"
HTTP_SEE_OTHER = "303 See Other"
HTTP_NOT_FOUND = "404 Not Found"

class ControllerTestCase(WebTestCase):
    """ Superclasse des tests des contrôleurs """
    
    def login(self, user_id = 1, password = "secret"):
        config.session_manager.login(user_id, password)
        
    def logout(self):
        config.session_manager.logout()
    
    def tearDown(self):
        super(ControllerTestCase, self).tearDown()
        self.logout()

