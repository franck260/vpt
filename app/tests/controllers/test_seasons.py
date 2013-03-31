# -*- coding: utf-8 -*-


from app.tests import SeasonData, dbfixture, UserData, TournamentData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER
from application import app


class TestSeasons(ControllerTestCase):
    
    def setUp(self):
        
        super(TestSeasons, self).setUp()
        self.data = dbfixture.data(UserData, TournamentData, SeasonData)
        self.data.setup()
    
    def tearDown(self):
        super(TestSeasons, self).tearDown()
        self.data.teardown()


    def test_view_season_notlogged(self):
        
        response = app.request("/season/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER) 

    def test_view_season(self):
        
        self.login()
        response = app.request("/season/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("<h1>\nSaison 1 (2009 - 2010)\n</h1>", response.data)
        self.assertIn("%s</td>" % UserData.franck_p.pseudonym, response.data)
        self.assertIn("%s</td>" % UserData.jo.pseudonym, response.data)
        self.assertIn("%s</td>" % UserData.nico.pseudonym, response.data)
        
