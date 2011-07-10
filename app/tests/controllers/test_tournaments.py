# -*- coding: utf-8 -*-

from app.models import Result, Tournament
from app.tests import dbfixture, TournamentData, UserData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER, \
    HTTP_NOT_FOUND
from application import app
from web import config
import datetime



class TestTournaments(ControllerTestCase):
    
    def setUp(self):
        
        super(TestTournaments, self).setUp()
        self.data = dbfixture.data(UserData, TournamentData)
        self.data.setup()
    
    def tearDown(self):
        super(TestTournaments, self).tearDown()
        self.data.teardown()

    def test_view_notlogged(self):
        
        response = app.request("/tournament/2/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        
    def test_view_404(self):
        
        self.login()
        response = app.request("/tournament/2/9") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_NOT_FOUND)

    def test_view(self):
        
        self.login()
        response = app.request("/tournament/2/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Tournoi 1 (mercredi 01 septembre 2010)", response.data)


    def test_view_statistics_notlogged(self):
        
        response = app.request("/statistics/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_view_statistics(self):

        self.login()        
        response = app.request("/statistics/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Nombre de participants</td><td>3</td>", response.data) 
        self.assertIn("Absents</td><td>" + UserData.franck_l.pseudonym + "</td>", response.data) 
        self.assertIn("Somme en jeu</td><td>40 €</td>", response.data)  

    def test_view_results_notlogged(self):
        response = app.request("/results/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        
    def test_view_results(self):
        self.login()
        response = app.request("/results/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertNotIn(UserData.franck_l.pseudonym, response.data)
        self.assertIn(UserData.franck_p.pseudonym, response.data)
        self.assertIn(UserData.jo.pseudonym, response.data)
        self.assertIn(UserData.nico.pseudonym, response.data)
        self.assertNotIn(UserData.fx.pseudonym, response.data)
        self.assertNotIn(UserData.rolland.pseudonym, response.data)
        
    def test_view_comments_notlogged(self):
        response = app.request("/comments/3") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_view_comments(self):
        self.login()
        response = app.request("/comments/3") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Salut&nbsp;les&nbsp;amis&nbsp;!<br />Je&nbsp;suis&nbsp;Franck", response.data)
        
    def test_update_status_notlogged(self):
        response = app.request("/updateStatus", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_update_status_new(self):
        tournament_11 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        self.assertEqual(len(tournament_11.results), 5)
        self.assertFalse(config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 6).all()) #@UndefinedVariable
        
        self.login("rolland.quillevere@gmail.com", "secret6")
        response = app.request("/updateStatus", method="POST", data={"tournament_id" : 1, "status" : Result.STATUSES.P}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        
        self.assertEqual(len(tournament_11.results), 6)
        inserted_row = config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 6).one() #@UndefinedVariable
        self.assertEquals(inserted_row.status, Result.STATUSES.P)
        
        #TODO: should be done by the fixture
        config.orm.delete(inserted_row)
        config.orm.commit()

    def test_update_status_existing(self):
        tournament_11 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        self.assertEqual(len(tournament_11.results), 5)
        self.assertTrue(config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 1).one()) #@UndefinedVariable
        
        self.login("franck.lasry@gmail.com", "secret1")
        response = app.request("/updateStatus", method="POST", data={"tournament_id" : 1, "status" : Result.STATUSES.M}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        
        self.assertEqual(len(tournament_11.results), 5)
        updated_row = config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 1).one() #@UndefinedVariable
        self.assertEquals(updated_row.status, Result.STATUSES.M)
           
    def test_add_comment_notlogged(self):
        response = app.request("/addComment", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        
    def test_add_comment(self):
        tournament_11 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        self.assertEqual(len(tournament_11.comments), 0)
        self.login()
        response = app.request("/addComment", method="POST", data={"tournament_id" : 1, "comment" : "Salut les copains"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertEqual(len(tournament_11.comments), 1)
