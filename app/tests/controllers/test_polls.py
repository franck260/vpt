# -*- coding: utf-8 -*-

from app.models import Poll, PollVote, PollUserChoice, User
from app.tests import dbfixture, PollData, PollVoteData, PollCommentData, \
    UserData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER, \
    HTTP_NOT_FOUND, HTTP_FORBIDDEN
from application import app
from web import config
import datetime
import urllib
try:
    import json
except ImportError:
    import simplejson as json

class TestPolls(ControllerTestCase):
    
    def setUp(self):
        
        super(TestPolls, self).setUp()
        self.data = dbfixture.data(PollData, PollVoteData)
        self.data.setup()
    
    def tearDown(self):
        super(TestPolls, self).tearDown()
        self.data.teardown()

    def test_view_notlogged(self):
        
        response = app.request("/poll/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        
    def test_view_404(self):
        
        self.login()
        response = app.request("/poll/42") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_NOT_FOUND)

    def test_view(self):
        
        self.login()
        response = app.request("/poll/1") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        #TODO: restore
        #self.assertIn(PollData.poll_1.title, response.data)
        #self.assertIn(PollCommentData.comment_11.comment, response.data)
        #self.assertIn(PollCommentData.comment_12.comment, response.data)
        #self.assertIn("<td>" + UserData.nico.pseudonym + "</td>\n<td>\n</td>\n<td>\n√\n</td>\n<td>\n</td>", response.data)

    def test_add_comment_notlogged(self):
        response = app.request("/add/comment", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        
    def test_add_comment_404(self):
        
        self.login()
        response = app.request("/poll/comment", method="POST", data={"poll_id": 42, "comment": "Sondage : salut les copains"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_NOT_FOUND)

    def test_add_comment_new(self):
        
        poll_1 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2012, 4, 5)).one() #@UndefinedVariable
        poll_2 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2011, 5, 28)).one() #@UndefinedVariable
        poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable
        
        self.assertEqual(len(poll_1.comments), 2)
        self.assertEqual(len(poll_2.comments), 1)
        self.assertEqual(len(poll_3.comments), 0)
                
        self.login()
        response = app.request("/poll/comment", method="POST", data={"poll_id": poll_3.id, "comment": "Sondage : salut les copains"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Sondage : salut les copains", response.data)
        
        self.assertEqual(len(poll_1.comments), 2)
        self.assertEqual(len(poll_2.comments), 1)
        self.assertEqual(len(poll_3.comments), 1)

    def test_add_comment_existing(self):

        try:

            poll_1 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2012, 4, 5)).one() #@UndefinedVariable
            poll_2 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2011, 5, 28)).one() #@UndefinedVariable
            poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable
            
            self.assertEqual(len(poll_1.comments), 2)
            self.assertEqual(len(poll_2.comments), 1)
            self.assertEqual(len(poll_3.comments), 0)
            
            self.login()
            response = app.request("/poll/comment", method="POST", data={"poll_id": poll_1.id, "comment": "Sondage : salut les copains"}) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_OK)
            self.assertIn("Sondage : salut les copains", response.data)
            
            self.assertEqual(len(poll_1.comments), 3)
            self.assertEqual(len(poll_2.comments), 1)
            self.assertEqual(len(poll_3.comments), 0)
            
        finally:

            #TODO: should be done by the fixture
            config.orm.delete(poll_1.comments[2])
            config.orm.commit()
            
    def test_vote_notlogged(self):
        response = app.request("/poll/vote", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_vote_404(self):
        self.login()
        response = app.request("/poll/vote", method="POST", data={"poll_id": 42}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_NOT_FOUND)

    def test_vote(self):
        
        self.login("jo@gmail.com", "secret4")
        
        jo = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable
        poll_1 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2012, 4, 5)).one() #@UndefinedVariable
        poll_2 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2011, 5, 28)).one() #@UndefinedVariable
        poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable
        
        self.assertEqual(config.orm.query(PollVote).count(), 5)
        self.assertEqual(config.orm.query(PollUserChoice).count(), 7)
        self.assertEqual(len(poll_1.choices_by_user), 3)
        self.assertEqual(len(poll_2.choices_by_user), 2)
        self.assertEqual(len(poll_3.choices_by_user), 0)
        
        try:
            # Scenario 1 : first vote on a poll, non-empty list of choices
            response = app.request("/poll/vote", method="POST", data=urllib.urlencode({"poll_id": poll_3.id, "poll_user_choices": [0,1]}, True)) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_OK)
  
            # Checks that the JSON response is well-formed
            decoded_json_response = json.loads(response.data)
            self.assertEqual(len(decoded_json_response), 2)
            self.assertIn("partial", decoded_json_response)
            self.assertIn("data", decoded_json_response)
            
            # Checks the partial rendering indicator
            partial = decoded_json_response["partial"]
            self.assertFalse(partial)

            # Checks the data
            data = decoded_json_response["data"]
            #TODO: restore
            #self.assertIn("<table id=\"poll_votes_table\" class=\"results fixed_width\">", data)
            #self.assertIn("<td>" + UserData.jo.pseudonym + "</td>\n<td>\n√\n</td>\n<td>\n√\n</td>", data)
            
            # Checks the model
            self.assertEqual(len(poll_3.choices_by_user[jo]), 2)
            self.assertEqual(poll_3.votes_by_user[jo].first_vote_dt, poll_3.votes_by_user[jo].last_vote_dt)
            self.assertEqual(config.orm.query(PollVote).count(), 6)
            self.assertEqual(config.orm.query(PollUserChoice).count(), 9)
            self.assertEqual(len(poll_1.choices_by_user), 3)
            self.assertEqual(len(poll_2.choices_by_user), 2)
            self.assertEqual(len(poll_3.choices_by_user), 1)

            # Scenario 2 : second vote on a poll, same user, non-empty list of choices
            response = app.request("/poll/vote", method="POST", data=urllib.urlencode({"poll_id": poll_3.id, "poll_user_choices": [0]}, True)) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_OK)

            # Checks that the JSON response is well-formed
            decoded_json_response = json.loads(response.data)
            self.assertEqual(len(decoded_json_response), 2)
            self.assertIn("partial", decoded_json_response)
            self.assertIn("data", decoded_json_response)
            
            # Checks the partial rendering indicator
            partial = decoded_json_response["partial"]
            self.assertTrue(partial)
            
            # Checks the data
            data = decoded_json_response["data"]
            #TODO: restore
            #self.assertNotIn("<table id=\"poll_votes_table\" class=\"results fixed_width\">", data)
            #self.assertIn("<td>" + UserData.jo.pseudonym + "</td>\n<td>\n√\n</td>\n<td>\n</td>", data)
            
            # Checks the model
            self.assertEqual(len(poll_3.choices_by_user[jo]), 1)
            self.assertGreater(poll_3.votes_by_user[jo].last_vote_dt, poll_3.votes_by_user[jo].first_vote_dt)
            self.assertEqual(config.orm.query(PollVote).count(), 6)
            self.assertEqual(config.orm.query(PollUserChoice).count(), 8)
            self.assertEqual(len(poll_1.choices_by_user), 3)
            self.assertEqual(len(poll_2.choices_by_user), 2)
            self.assertEqual(len(poll_3.choices_by_user), 1)
            
            # Scenario 3 : third vote on a poll, same user, empty list of choices
            response = app.request("/poll/vote", method="POST", data=urllib.urlencode({"poll_id": poll_3.id, "poll_user_choices": []}, True)) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_OK)

            # Checks that the JSON response is well-formed
            decoded_json_response = json.loads(response.data)
            self.assertEqual(len(decoded_json_response), 2)
            self.assertIn("partial", decoded_json_response)
            self.assertIn("data", decoded_json_response)
            
            # Checks the partial rendering indicator
            partial = decoded_json_response["partial"]
            self.assertTrue(partial)

            # Checks the data
            data = decoded_json_response["data"]
            self.assertNotIn("<table id=\"poll_votes_table\" class=\"results fixed_width\">", data)
            self.assertIn("<td>" + UserData.jo.pseudonym + "</td>\n<td>\n</td>\n<td>\n</td>", data)
        
            # Checks the model
            self.assertEqual(len(poll_3.choices_by_user[jo]), 0)
            self.assertGreater(poll_3.votes_by_user[jo].last_vote_dt, poll_3.votes_by_user[jo].first_vote_dt)
            self.assertEqual(config.orm.query(PollVote).count(), 6)
            self.assertEqual(config.orm.query(PollUserChoice).count(), 7)
            self.assertEqual(len(poll_1.choices_by_user), 3)
            self.assertEqual(len(poll_2.choices_by_user), 2)
            self.assertEqual(len(poll_3.choices_by_user), 1)

        finally:
            #TODO: should be done by the fixture
            config.orm.delete(poll_3.votes_by_user[jo])
            config.orm.commit()

    def test_vote_expired(self):
            
        self.login()
        
        expired_poll = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2011, 5, 28)).one() #@UndefinedVariable
        self.assertTrue(expired_poll.expired)
        self.assertEqual(len(expired_poll.choices_by_user), 2)
        
        response = app.request("/poll/vote", method="POST", data=urllib.urlencode({"poll_id": expired_poll.id, "poll_user_choices": [0,1]}, True)) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        self.assertEqual(response.data, u"Le sondage a expire")
        
        response = app.request("/poll/vote", method="POST", data=urllib.urlencode({"poll_id": expired_poll.id, "poll_user_choices": [0]}, True)) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        self.assertEqual(response.data, u"Le sondage a expire")

        response = app.request("/poll/vote", method="POST", data=urllib.urlencode({"poll_id": expired_poll.id, "poll_user_choices": []}, True)) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        self.assertEqual(response.data, u"Le sondage a expire")
        
        response = app.request("/poll/vote", method="POST", data=urllib.urlencode({"poll_id": expired_poll.id, "poll_user_choices": []}, True)) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        self.assertEqual(response.data, u"Le sondage a expire")
        
        self.assertEqual(len(expired_poll.choices_by_user), 2)
        
    def test_vote_invalid_choices(self):
        
        self.login("jo@gmail.com", "secret4")
        
        poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable
        self.assertFalse(poll_3.expired)
        self.assertEqual(len(poll_3.choices_by_user), 0)

        response = app.request("/poll/vote", method="POST", data=urllib.urlencode({"poll_id": poll_3.id, "poll_user_choices": [0,2]}, True)) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        self.assertEqual(response.data, u"Un des entiers passes a la methode /poll/vote n'est pas compris dans l'intervalle [0, 1]")
        
        response = app.request("/poll/vote", method="POST", data=urllib.urlencode({"poll_id": poll_3.id, "poll_user_choices": [3]}, True)) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        self.assertEqual(response.data, u"Un des entiers passes a la methode /poll/vote n'est pas compris dans l'intervalle [0, 1]")

        self.assertEqual(len(poll_3.choices_by_user), 0)

