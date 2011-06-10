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
        
        franck_l = config.orm.query(User).filter(User.nom == "Lasry").one() #@UndefinedVariable
        jo = config.orm.query(User).filter(User.prenom == "Jonathan").one() #@UndefinedVariable
        francks = config.orm.query(User).filter(User.pseudo.like("Franck%")).all() #@UndefinedVariable
        
        self.assertEquals(franck_l.prenom, "Franck")
        self.assertEquals(jo.prenom, "Jonathan")
        self.assertEqual(len(francks), 2)
                
    
    
    