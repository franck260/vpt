# -*- coding: utf-8 -*-

'''
Created on 16 mars 2011

@author: Franck
'''

from app.tests import SeasonData, dbfixture, UserData, TournamentData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER
from application import app

#TODO: mocker la table SESSIONS plutôt que d'attaquer le composant

class TestMain(ControllerTestCase):
    
    def setUp(self):
        
        super(TestMain, self).setUp()
        self.data = dbfixture.data(UserData, TournamentData, SeasonData)
        self.data.setup()
    
    def tearDown(self):
        super(TestMain, self).tearDown()
        self.data.teardown()

    def test_index_notlogged(self):
        
        response = app.request("/") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_index(self):
        
        self.login()
        response = app.request("/") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("prochain tournoi", response.data)  

    def test_view_season_notlogged(self):
        
        response = app.request("/season/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER) 

    def test_view_season(self):
        
        self.login()
        response = app.request("/season/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        
        self.assertIn("<h2>Saison 1 (2009 - 2010)</h2>", response.data)
        self.assertIn("<td>%s</td>" %UserData.franck_p.pseudo, response.data)
        self.assertIn("<td>%s</td>" %UserData.jo.pseudo, response.data)
        self.assertIn("<td>%s</td>" %UserData.nico.pseudo, response.data)
        