# -*- coding: utf-8 -*-

from app.tests import WebTestCase, UserData
from app.utils import session
from web import config
import web

HTTP_OK = "200 OK"
HTTP_SEE_OTHER = "303 See Other"
HTTP_NOT_FOUND = "404 Not Found"

class ControllerTestCase(WebTestCase):
    """ Parent of all controllers test classes """
    
    def login(self, email = "franck.lasry@gmail.com", password = "secret1"):
        config.session_manager.login(email, password)
        
    def logout(self):
        config.session_manager.logout()
    
    def tearDown(self):
        super(ControllerTestCase, self).tearDown()
        self.logout()

