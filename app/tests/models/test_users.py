# -*- coding: utf-8 -*-

from app.models import User
from app.tests import dbfixture, UserData
from app.tests.models import ModelTestCase
from web import config


class TestUser(ModelTestCase):
    
    def setUp(self):
        super(TestUser, self).setUp()
        self.data = dbfixture.data(UserData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_all(self):
        
        all_users = User.all()
        print all_users
        self.assertEqual(len(all_users), 6)
    
    def test_get(self):
        
        franck_l = config.orm.query(User).filter(User.last_name == "Lasry").one() #@UndefinedVariable
        jo = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable
        francks = config.orm.query(User).filter(User.pseudonym.like("Franck%")).all() #@UndefinedVariable
        
        self.assertEquals(franck_l.first_name, "Franck")
        self.assertEquals(jo.first_name, "Jonathan")
        self.assertEqual(len(francks), 2)
                
    
    
    