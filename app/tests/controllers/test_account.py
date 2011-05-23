# -*- coding: utf-8 -*-

'''
Created on 16 mars 2011

@author: Franck
'''

from app.tests import dbfixture, UserData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER
from application import app
from web import config


#TODO: mocker la table SESSIONS plutôt que d'attaquer le composant

class TestAccount(ControllerTestCase):
    
    def setUp(self):
        
        super(TestAccount, self).setUp()
        self.data = dbfixture.data(UserData)
        self.data.setup()
    
    def tearDown(self):
        super(TestAccount, self).tearDown()
        self.data.teardown()
        
    def test_logout_notlogged(self):
        
        response = app.request("/logout") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
 
    def test_logout(self):
        
        self.login()
        self.assertTrue(config.session_manager.is_logged)
        response = app.request("/logout") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        self.assertFalse(config.session_manager.is_logged)

    def test_login_GET(self):
        
        response = app.request("/login", method="GET") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Veuillez entrer vos identifiants de connexion", response.data)
 
    def test_login_POST_OK(self):

        self.assertFalse(config.session_manager.is_logged)
        response = app.request("/login", method="POST", data={"user_id" : 1, "password" : "secret"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        self.assertTrue(config.session_manager.is_logged)  

    def test_login_POST_KO(self):

        self.assertFalse(config.session_manager.is_logged)
        response = app.request("/login", method="POST", data={"user_id" : 1, "password" : "error"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertFalse(config.session_manager.is_logged)  
