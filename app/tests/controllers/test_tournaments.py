# -*- coding: utf-8 -*-

'''
Created on 16 mars 2011

@author: Franck
'''

from app.models import orm
from app.models.results import Result
from app.models.tournaments import Tournament
from app.tests import dbfixture, TournamentData, UserData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER, \
    HTTP_NOT_FOUND
from application import app
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
        self.assertNotIn("Précédent", response.data)
        self.assertNotIn("Suivant", response.data)

    def test_view_with_next_paging(self):
        
        self.login()
        response = app.request("/tournament/1/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Tournoi 1 (mardi 01 septembre 2009)", response.data)
        self.assertNotIn("Tournoi précédent", response.data)
        self.assertIn("Tournoi suivant", response.data)
        
    def test_view_with_previous_paging(self):
        
        self.login()
        response = app.request("/tournament/1/2") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Tournoi 2 (vendredi 01 janvier 2010)", response.data)
        self.assertIn("Tournoi précédent", response.data)
        self.assertNotIn("Tournoi suivant", response.data)


    def test_view_stats_notlogged(self):
        
        response = app.request("/stats/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_view_stats(self):

        self.login()        
        response = app.request("/stats/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Présents: 3", response.data) 
        self.assertIn("Absents: 1", response.data) 
        self.assertIn("En jeu: 40 euros", response.data)  

    def test_view_results_notlogged(self):
        response = app.request("/results/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        
    def test_view_results(self):
        self.login()
        response = app.request("/results/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn(UserData.franck_l.pseudo, response.data)
        self.assertIn(UserData.franck_p.pseudo, response.data)
        self.assertIn(UserData.jo.pseudo, response.data)
        self.assertIn(UserData.nico.pseudo, response.data)
        self.assertIn(UserData.fx.pseudo, response.data)
        self.assertNotIn(UserData.rolland.pseudo, response.data)
        
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
        tournament_11 = orm.query(Tournament).filter(Tournament.date_tournoi == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        self.assertEqual(len(tournament_11.results), 5)
        self.assertFalse(orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 6).all()) #@UndefinedVariable
        
        self.login(user_id=6)
        response = app.request("/updateStatus", method="POST", data={"tournament_id" : 1, "statut" : Result.STATUSES.P}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        
        self.assertEqual(len(tournament_11.results), 6)
        inserted_row = orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 6).one() #@UndefinedVariable
        self.assertEquals(inserted_row.statut, Result.STATUSES.P)
        
        #TODO devrait être fait par la fixture
        orm.delete(inserted_row)
        orm.commit()

    def test_update_status_existing(self):
        tournament_11 = orm.query(Tournament).filter(Tournament.date_tournoi == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        self.assertEqual(len(tournament_11.results), 5)
        self.assertTrue(orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 1).one()) #@UndefinedVariable
        
        self.login(user_id=1)
        response = app.request("/updateStatus", method="POST", data={"tournament_id" : 1, "statut" : Result.STATUSES.M}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        
        self.assertEqual(len(tournament_11.results), 5)
        updated_row = orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 1).one() #@UndefinedVariable
        self.assertEquals(updated_row.statut, Result.STATUSES.M)
           
    def test_add_comment_notlogged(self):
        response = app.request("/addComment", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        
    def test_add_comment(self):
        tournament_11 = orm.query(Tournament).filter(Tournament.date_tournoi == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        self.assertEqual(len(tournament_11.comments), 0)
        self.login()
        response = app.request("/addComment", method="POST", data={"tournament_id" : 1, "comment" : "Salut les copains"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertEqual(len(tournament_11.comments), 1)
