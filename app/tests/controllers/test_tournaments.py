# -*- coding: utf-8 -*-

from app.models import Result, Tournament, User, Season
from app.tests import dbfixture, TournamentData, UserData, ResultData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER, \
    HTTP_NOT_FOUND, HTTP_FORBIDDEN
from application import app
from web import config
import copy
import datetime
try:
    import json
except ImportError:
    import simplejson as json 



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
        self.assertIn("Tournoi 1 (dimanche 01 août 2010)", response.data)




#    def test_view_statistics(self):
#
#        self.login()        
#        response = app.request("/statistics/1") #@UndefinedVariable
#        self.assertEqual(response.status, HTTP_OK)
#        self.assertIn("Nombre de participants</td><td>3</td>", response.data) 
#        self.assertIn("Absents</td><td>" + UserData.franck_l.pseudonym + "</td>", response.data) 
#        self.assertIn("Somme en jeu</td><td>40 €</td>", response.data)  


        
#    def test_view_results(self):
#        self.login()
#        response = app.request("/results/1") #@UndefinedVariable
#        self.assertEqual(response.status, HTTP_OK)
#        self.assertNotIn(UserData.franck_l.pseudonym, response.data)
#        self.assertIn(UserData.franck_p.pseudonym, response.data)
#        self.assertIn(UserData.jo.pseudonym, response.data)
#        self.assertIn(UserData.nico.pseudonym, response.data)
#        self.assertNotIn(UserData.fx.pseudonym, response.data)
#        self.assertNotIn(UserData.rolland.pseudonym, response.data)
#        self.assertNotIn("</button>", response.data)
        


#    def test_view_comments(self):
#        self.login()
#        response = app.request("/comments/3") #@UndefinedVariable
#        self.assertEqual(response.status, HTTP_OK)
#        self.assertIn("Salut&nbsp;les&nbsp;amis&nbsp;!<br />Je&nbsp;suis&nbsp;Franck", response.data)
        
    def test_update_status_notlogged(self):
        response = app.request("/update/status", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_update_status_new(self):
        
        try:
            
            tournament_11 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
            self.assertEqual(len(tournament_11.results), 5)
            self.assertFalse(config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 6).all()) #@UndefinedVariable
            
            self.login("rolland.quillevere@gmail.com", "secret6")
            response = app.request("/update/status", method="POST", data={"tournament_id" : 1, "status" : Result.STATUSES.P}) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_OK)
            
            self.assertEqual(len(tournament_11.results), 6)
            inserted_row = config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 6).one() #@UndefinedVariable
            self.assertEquals(inserted_row.status, Result.STATUSES.P)
            
            # Checks that the JSON response is well-formed
            decoded_json_response = json.loads(response.data)
            self.assertEqual(len(decoded_json_response), 2)
            self.assertIn("statistics", decoded_json_response)
            self.assertIn("results", decoded_json_response)
            
            # Checks the statistics
            statistics = decoded_json_response["statistics"]
            self.assertIn("Nombre de participants</td><td>4</td>", statistics) 
            self.assertIn("Absents</td><td>%s</td>" %UserData.franck_l.pseudonym, statistics) 
            self.assertIn(u"Somme en jeu</td><td>50 €</td>", statistics)  
            
            # Checks the results
            results = decoded_json_response["results"]
            self.assertNotIn(UserData.franck_l.pseudonym, results)
            self.assertIn(UserData.franck_p.pseudonym, results)
            self.assertIn(UserData.jo.pseudonym, results)
            self.assertIn(UserData.nico.pseudonym, results)
            self.assertNotIn(UserData.fx.pseudonym, results)
            self.assertIn(UserData.rolland.pseudonym, results)
            self.assertNotIn("</button>", results)
        
        finally:
            #TODO: should be done by the fixture
            config.orm.delete(inserted_row)
            config.orm.commit()

    def test_update_status_existing(self):
        tournament_11 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        self.assertEqual(len(tournament_11.results), 5)
        self.assertTrue(config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 1).one()) #@UndefinedVariable
        
        self.login("franck.lasry@gmail.com", "secret1")
        response = app.request("/update/status", method="POST", data={"tournament_id" : 1, "status" : Result.STATUSES.M}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        
        self.assertEqual(len(tournament_11.results), 5)
        updated_row = config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 1).one() #@UndefinedVariable
        self.assertEquals(updated_row.status, Result.STATUSES.M)
        
        # Checks that the JSON response is well-formed
        decoded_json_response = json.loads(response.data)
        self.assertEqual(len(decoded_json_response), 2)
        self.assertIn("statistics", decoded_json_response)
        self.assertIn("results", decoded_json_response)
        
        # Checks the statistics
        statistics = decoded_json_response["statistics"]
        self.assertIn("Nombre de participants</td><td>3</td>", statistics)
        self.assertIn(u"Peut-être</td><td>%s,%s</td>" %(UserData.franck_l.pseudonym, UserData.fx.pseudonym), statistics) 
        self.assertIn(u"Somme en jeu</td><td>40 €</td>", statistics)  
        
        # Checks the results
        results = decoded_json_response["results"]
        self.assertNotIn(UserData.franck_l.pseudonym, results)
        self.assertIn(UserData.franck_p.pseudonym, results)
        self.assertIn(UserData.jo.pseudonym, results)
        self.assertIn(UserData.nico.pseudonym, results)
        self.assertNotIn(UserData.fx.pseudonym, results)
        self.assertNotIn(UserData.rolland.pseudonym, results)
        self.assertNotIn("</button>", results)
           
    def test_add_comment_notlogged(self):
        response = app.request("/add/comment", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        
    def test_add_comment_new(self):
        tournament_11 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        self.assertEqual(len(tournament_11.comments), 0)
        self.login()
        response = app.request("/add/comment", method="POST", data={"tournament_id" : 1, "comment" : "Salut les copains"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertEqual(len(tournament_11.comments), 1)
        
        # Checks that the JSON response is well-formed
        decoded_json_response = json.loads(response.data)
        self.assertEqual(len(decoded_json_response), 1)
        self.assertIn("comments", decoded_json_response)
        
        # Checks the comments
        comments = decoded_json_response["comments"]
        self.assertIn("Salut&nbsp;les&nbsp;copains", comments)

    def test_add_comment_existing(self):
        
        try:
            
            tournament_21 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable
            self.assertEqual(len(tournament_21.comments), 1)
            self.login()
            response = app.request("/add/comment", method="POST", data={"tournament_id" : 3, "comment" : "Salut les copains"}) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_OK)
            self.assertEqual(len(tournament_21.comments), 2)
            
            # Checks that the JSON response is well-formed
            decoded_json_response = json.loads(response.data)
            self.assertEqual(len(decoded_json_response), 1)
            self.assertIn("comments", decoded_json_response)
            
            # Checks the comments
            comments = decoded_json_response["comments"]
            self.assertIn("Salut&nbsp;les&nbsp;amis&nbsp;!<br />Je&nbsp;suis&nbsp;Franck", comments)
            self.assertIn("Salut&nbsp;les&nbsp;copains", comments)
            
        finally:
            #TODO: should be done by the fixture
            config.orm.delete(tournament_21.comments[1])
            config.orm.commit()
            
    def test_admin_results_GET_notlogged(self):
        response = app.request("/admin/results/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_admin_results_GET_notadmin(self):
        self.login("franck.lasry@gmail.com", "secret1")
        response = app.request("/admin/results/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        
    def test_admin_results_GET(self):
        self.login("franck.perez@gmail.com", "secret2")
        response = app.request("/admin/results/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn(UserData.franck_l.pseudonym, response.data)
        self.assertIn(UserData.franck_p.pseudonym, response.data)
        self.assertIn(UserData.jo.pseudonym, response.data)
        self.assertIn(UserData.nico.pseudonym, response.data)
        self.assertIn(UserData.fx.pseudonym, response.data)
        self.assertNotIn(UserData.rolland.pseudonym, response.data)
        self.assertIn("</button>", response.data)
        
    def test_admin_results_POST_notlogged(self):
        response = app.request("/admin/results/1", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_admin_results_POST_notadmin(self):
        self.login("franck.lasry@gmail.com", "secret1")
        response = app.request("/admin/results/1", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        
    def test_admin_results_POST(self):
        
        tournament_21 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable
        jo = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable
        fx = config.orm.query(User).filter(User.last_name == "Clair").one() #@UndefinedVariable
        
        updated_results = [Result(user=jo, status=Result.STATUSES.P, buyin=10, rank=1, profit=30),
                           Result(user=fx, status=Result.STATUSES.P, buyin=20, rank=2)
                           ]


        updated_results_data = {"Result-9-status" : "P",
                                "Result-9-buyin" : "20",
                                "Result-9-rank" : "2",
                                "Result-9-profit" : "",
                                "Result-10-status" : "P",
                                "Result-10-buyin" : "10",
                                "Result-10-rank" : "1",
                                "Result-10-profit" : "30"}
        
        self.login("franck.perez@gmail.com", "secret2")

        # Makes sure that the update fails with invalid data (1)
        invalid_results_data = copy.deepcopy(updated_results_data)
        invalid_results_data["Result-9-buyin"] = ""
        response = app.request("/admin/results/3", method="POST", data=invalid_results_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Mandatory value (status=P)", response.data)
        decoded_json_response = json.loads(response.data)
        self.assertEqual(len(decoded_json_response), 2)
        self.assertIn("results", decoded_json_response)
        self.assertIn("statistics", decoded_json_response)
        self.assertIsNone(decoded_json_response["statistics"])
        self.assertNotEqual(tournament_21.results, updated_results)
        self.assertEqual(tournament_21.results, [ResultData.result21_fx, ResultData.result21_jo])
        
        # Makes sure that the update fails with invalid data (2)
        invalid_results_data = copy.deepcopy(updated_results_data)
        invalid_results_data["Result-9-status"] = "M"
        invalid_results_data["Result-9-buyin"] = "20"
        invalid_results_data["Result-9-rank"] = ""
        invalid_results_data["Result-9-profit"] = ""
        response = app.request("/admin/results/3", method="POST", data=invalid_results_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Forbidden value (status=M)", response.data)
        decoded_json_response = json.loads(response.data)
        self.assertEqual(len(decoded_json_response), 2)
        self.assertIn("results", decoded_json_response)
        self.assertIn("statistics", decoded_json_response)
        self.assertIsNone(decoded_json_response["statistics"])
        self.assertNotEqual(tournament_21.results, updated_results)
        self.assertEqual(tournament_21.results, [ResultData.result21_fx, ResultData.result21_jo])

        # Makes sure that the update fails with invalid data (3)
        invalid_results_data = copy.deepcopy(updated_results_data)
        invalid_results_data["Result-9-status"] = "M"
        invalid_results_data["Result-9-buyin"] = ""
        invalid_results_data["Result-9-rank"] = "2"
        invalid_results_data["Result-9-profit"] = ""
        response = app.request("/admin/results/3", method="POST", data=invalid_results_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Forbidden value (status=M)", response.data)
        decoded_json_response = json.loads(response.data)
        self.assertEqual(len(decoded_json_response), 2)
        self.assertIn("results", decoded_json_response)
        self.assertIn("statistics", decoded_json_response)
        self.assertIsNone(decoded_json_response["statistics"])
        self.assertNotEqual(tournament_21.results, updated_results)
        self.assertEqual(tournament_21.results, [ResultData.result21_fx, ResultData.result21_jo])
        
        # Makes sure that the update fails with invalid data (4)
        invalid_results_data = copy.deepcopy(updated_results_data)
        invalid_results_data["Result-9-status"] = "M"
        invalid_results_data["Result-9-buyin"] = ""
        invalid_results_data["Result-9-rank"] = ""
        invalid_results_data["Result-9-profit"] = "0"
        response = app.request("/admin/results/3", method="POST", data=invalid_results_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Forbidden value (status=M)", response.data)
        decoded_json_response = json.loads(response.data)
        self.assertEqual(len(decoded_json_response), 2)
        self.assertIn("results", decoded_json_response)
        self.assertIn("statistics", decoded_json_response)
        self.assertIsNone(decoded_json_response["statistics"])
        self.assertNotEqual(tournament_21.results, updated_results)
        self.assertEqual(tournament_21.results, [ResultData.result21_fx, ResultData.result21_jo])

        # Makes sure that the update fails with invalid data (5)
        invalid_results_data = copy.deepcopy(updated_results_data)
        invalid_results_data["Result-9-status"] = "A"
        invalid_results_data["Result-9-buyin"] = "20"
        invalid_results_data["Result-9-rank"] = ""
        invalid_results_data["Result-9-profit"] = ""
        response = app.request("/admin/results/3", method="POST", data=invalid_results_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Forbidden value (status=A)", response.data)
        decoded_json_response = json.loads(response.data)
        self.assertEqual(len(decoded_json_response), 2)
        self.assertIn("results", decoded_json_response)
        self.assertIn("statistics", decoded_json_response)
        self.assertIsNone(decoded_json_response["statistics"])
        self.assertNotEqual(tournament_21.results, updated_results)
        self.assertEqual(tournament_21.results, [ResultData.result21_fx, ResultData.result21_jo])

        # Makes sure that the update fails with invalid data (6)
        invalid_results_data = copy.deepcopy(updated_results_data)
        invalid_results_data["Result-9-status"] = "A"
        invalid_results_data["Result-9-buyin"] = ""
        invalid_results_data["Result-9-rank"] = "2"
        invalid_results_data["Result-9-profit"] = ""
        response = app.request("/admin/results/3", method="POST", data=invalid_results_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Forbidden value (status=A)", response.data)
        decoded_json_response = json.loads(response.data)
        self.assertEqual(len(decoded_json_response), 2)
        self.assertIn("results", decoded_json_response)
        self.assertIn("statistics", decoded_json_response)
        self.assertIsNone(decoded_json_response["statistics"])
        self.assertNotEqual(tournament_21.results, updated_results)
        self.assertEqual(tournament_21.results, [ResultData.result21_fx, ResultData.result21_jo])
        
        # Makes sure that the update fails with invalid data (7)
        invalid_results_data = copy.deepcopy(updated_results_data)
        invalid_results_data["Result-9-status"] = "A"
        invalid_results_data["Result-9-buyin"] = ""
        invalid_results_data["Result-9-rank"] = ""
        invalid_results_data["Result-9-profit"] = "0"
        response = app.request("/admin/results/3", method="POST", data=invalid_results_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Forbidden value (status=A)", response.data)
        decoded_json_response = json.loads(response.data)
        self.assertEqual(len(decoded_json_response), 2)
        self.assertIn("results", decoded_json_response)
        self.assertIn("statistics", decoded_json_response)
        self.assertIsNone(decoded_json_response["statistics"])
        self.assertNotEqual(tournament_21.results, updated_results)
        self.assertEqual(tournament_21.results, [ResultData.result21_fx, ResultData.result21_jo])

        # Makes sure that the update works with valid data        
        response = app.request("/admin/results/3", method="POST", data=updated_results_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        decoded_json_response = json.loads(response.data)
        self.assertEqual(len(decoded_json_response), 2)
        self.assertIn("results", decoded_json_response)
        self.assertIn("statistics", decoded_json_response)
        self.assertIsNotNone(decoded_json_response["statistics"])
        self.assertEqual(tournament_21.results, updated_results)
        self.assertNotEqual(tournament_21.results, [ResultData.result21_fx, ResultData.result21_jo])