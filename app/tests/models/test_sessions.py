# -*- coding: utf-8 -*-

from app.models import Session
from app.tests import dbfixture, SessionData
from app.tests.models import ModelTestCase

class TestSession(ModelTestCase):
    
    def setUp(self):
        super(TestSession, self).setUp()
        self.data = dbfixture.data(SessionData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_all(self):
        all_sessions = Session.all()
        self.assertEqual(len(all_sessions), 1)
