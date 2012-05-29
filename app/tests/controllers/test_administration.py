# -*- coding: utf-8 -*-

from app.tests import dbfixture, TournamentData, SessionData, NewsData, UserData, \
    SeasonData, PollData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER, \
    HTTP_FORBIDDEN
from application import app

class TestAdministration(ControllerTestCase):
    
    DT_FORMAT = "%d/%m/%Y"
    
    def setUp(self):
        super(TestAdministration, self).setUp()
        self.data = dbfixture.data(TournamentData, NewsData, SessionData, PollData)
        self.data.setup()
    
    def tearDown(self):
        super(TestAdministration, self).tearDown()
        self.data.teardown()

    def test_admin_seasons_GET_notlogged(self):
        response = app.request("/admin/seasons") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_admin_seasons_GET_notadmin(self):
        self.login("franck.l@gmail.com", "secret1")
        response = app.request("/admin/seasons") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        
    def test_admin_seasons_GET(self):
        self.login("franck.p@gmail.com", "secret2")
        response = app.request("/admin/seasons") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        for season in (SeasonData.season_1, SeasonData.season_2):
            self.assertIn(str(season.start_year), response.data)
            self.assertIn(str(season.end_year), response.data)
        self.assertIn("Modifier", response.data)
        self.assertIn("Créer", response.data)
        
    def test_admin_tournaments_GET_notlogged(self):
        response = app.request("/admin/tournaments") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_admin_tournaments_GET_notadmin(self):
        self.login("franck.l@gmail.com", "secret1")
        response = app.request("/admin/tournaments") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        
    def test_admin_tournaments_GET(self):
        self.login("franck.p@gmail.com", "secret2")
        response = app.request("/admin/tournaments") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        # TODO: automate by looping over the fixture
        self.assertIn("01/09/2009", response.data)
        self.assertIn("01/01/2010", response.data)
        self.assertIn("01/08/2010", response.data)
        self.assertIn("Modifier", response.data)
        self.assertIn("Créer", response.data)
        
    def test_admin_news_GET_notlogged(self):
        response = app.request("/admin/news") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_admin_news_GET_notadmin(self):
        self.login("franck.l@gmail.com", "secret1")
        response = app.request("/admin/news") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        
    def test_admin_news_GET(self):
        self.login("franck.p@gmail.com", "secret2")
        response = app.request("/admin/news") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        # TODO: automate by looping over the fixture
        self.assertIn("27/05/2011", response.data)
        self.assertIn("10/06/2011", response.data)
        self.assertIn("13/07/2011", response.data)
        self.assertIn("15/08/2011", response.data)
        self.assertIn("Modifier", response.data)
        self.assertIn("Créer", response.data)
        
    def test_admin_users_GET_notlogged(self):
        response = app.request("/admin/users") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_admin_users_GET_notadmin(self):
        self.login("franck.l@gmail.com", "secret1")
        response = app.request("/admin/users") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        
    def test_admin_users_GET(self):
        self.login("franck.p@gmail.com", "secret2")
        response = app.request("/admin/users") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        for user in (UserData.franck_l, UserData.franck_p, UserData.fx, UserData.jo, UserData.nico, UserData.rolland, UserData.zoe):
            self.assertIn(user.email, response.data)
        self.assertIn("Modifier", response.data)
        self.assertIn("Créer", response.data)
        
    def test_admin_sessions_GET_notlogged(self):
        response = app.request("/admin/sessions") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_admin_sessions_GET_notadmin(self):
        self.login("franck.l@gmail.com", "secret1")
        response = app.request("/admin/sessions") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        
    def test_admin_sessions_GET(self):
        self.login("franck.p@gmail.com", "secret2")
        response = app.request("/admin/sessions") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn(SessionData.session.session_id, response.data)
        self.assertIn("ip:127.0.0.1", response.data)
        self.assertIn("Modifier", response.data)
        self.assertNotIn("Créer", response.data)
        
    def test_admin_polls_GET_notlogged(self):
        response = app.request("/admin/polls") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)

    def test_admin_polls_GET_notadmin(self):
        self.login("franck.l@gmail.com", "secret1")
        response = app.request("/admin/polls") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        
    def test_admin_polls_GET(self):
        self.login("franck.p@gmail.com", "secret2")
        response = app.request("/admin/polls") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        #TODO: restore
        #for poll in (PollData.poll_1, PollData.poll_2, PollData.poll_3):
            #self.assertIn(poll.title, response.data)
        #self.assertIn("Modifier", response.data)
        #self.assertIn("Créer", response.data)
