# -*- coding: utf-8 -*-


from app.tests import SeasonData, dbfixture, UserData, TournamentData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER
from application import app


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

        
