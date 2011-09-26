# -*- coding: utf-8 -*-

from app.tests import dbfixture, TournamentData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER, \
    HTTP_FORBIDDEN
from application import app

class TestAdministration(ControllerTestCase):
    
    def setUp(self):
        
        super(TestAdministration, self).setUp()
        self.data = dbfixture.data(TournamentData)
        self.data.setup()
    
    def tearDown(self):
        super(TestAdministration, self).tearDown()
        self.data.teardown()

    def test_admin_seasons_GET_notlogged(self):
        response = app.request("/admin/seasons") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_admin_seasons_GET_notadmin(self):
        self.login("franck.lasry@gmail.com", "secret1")
        response = app.request("/admin/seasons") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        
    def test_admin_seasons_GET(self):
        self.login("franck.perez@gmail.com", "secret2")
        response = app.request("/admin/seasons") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Créer", response.data)
        self.assertIn("Modifier", response.data)
        
    def test_admin_tournaments_GET_notlogged(self):
        response = app.request("/admin/tournaments") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_admin_tournaments_GET_notadmin(self):
        self.login("franck.lasry@gmail.com", "secret1")
        response = app.request("/admin/tournaments") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        
    def test_admin_tournaments_GET(self):
        self.login("franck.perez@gmail.com", "secret2")
        response = app.request("/admin/tournaments") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Créer", response.data)
        self.assertIn("Modifier", response.data)
