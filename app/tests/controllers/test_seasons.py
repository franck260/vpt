# -*- coding: utf-8 -*-

from app.tests import SeasonData, dbfixture, UserData, TournamentData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER
from application import app
try:
    import json
except ImportError:
    import simplejson as json 

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
        self.assertIn("Saison 1 (2009 - 2010)", response.data)

    def test_view_season_results_notlogged(self):
        response = app.request("/season/1/results") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_view_season_results(self):
        self.login()
        response = app.request("/season/1/results") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        # Checks that the JSON response is well-formed
        decoded_json_response = json.loads(response.data)
        self.assertEqual(len(decoded_json_response), 2)
        self.assertIn("players", decoded_json_response)
        self.assertIn("results", decoded_json_response)
        # Checks the actual JSON response
        players = decoded_json_response["players"]
        self.assertEqual(len(players), 3)
        self.assertIn(UserData.franck_p.pseudonym, players.values())
        self.assertIn(UserData.jo.pseudonym, players.values())
        self.assertIn(UserData.nico.pseudonym, players.values())
        results = decoded_json_response["results"]
        self.assertEqual(len(results), 2)
        self.assertEqual(len(results[0]), 3)
        self.assertEqual(len(results[1]), 2)