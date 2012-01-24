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
        self.assertEqual(len(User.all()), 7)
    
    def test_get(self):
        
        franck_l = config.orm.query(User).filter(User.pseudonym == "Franck L").one() #@UndefinedVariable
        jo = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable
        francks = config.orm.query(User).filter(User.pseudonym.like("Franck%")).all() #@UndefinedVariable
        
        self.assertEquals(franck_l.first_name, "Franck")
        self.assertEquals(jo.first_name, "Jonathan")
        self.assertEqual(len(francks), 2)
                
    def test_get_user(self):
        
        franck_l = config.orm.query(User).filter(User.pseudonym == "Franck L").one() #@UndefinedVariable
        jo = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable
        
        self.assertIsNone(User.get_user(None))
        self.assertEquals(User.get_user("franck.l@gmail.com"), franck_l)
        self.assertEquals(User.get_user("jo@gmail.com"), jo)
        
    def test_properties(self):

        franck_l = config.orm.query(User).filter(User.email == "franck.l@gmail.com").one() #@UndefinedVariable
        franck_p = config.orm.query(User).filter(User.email == "franck.p@gmail.com").one() #@UndefinedVariable
        fx = config.orm.query(User).filter(User.email == "fx@gmail.com").one() #@UndefinedVariable
        jo = config.orm.query(User).filter(User.email == "jo@gmail.com").one() #@UndefinedVariable
        nico = config.orm.query(User).filter(User.email == "nico@gmail.com").one() #@UndefinedVariable
        rolland = config.orm.query(User).filter(User.email == "rolland@gmail.com").one() #@UndefinedVariable
        zoe = config.orm.query(User).filter(User.email == "zoe@gmail.com").one() #@UndefinedVariable
        
        self.assertTrue(franck_l.active)
        self.assertFalse(franck_l.admin)

        self.assertTrue(franck_p.active)
        self.assertTrue(franck_p.admin)
        
        self.assertTrue(fx.active)
        self.assertFalse(fx.admin)        

        self.assertTrue(jo.active)
        self.assertFalse(jo.admin)
        
        self.assertTrue(nico.active)
        self.assertFalse(nico.admin)   
    
        self.assertTrue(rolland.active)
        self.assertFalse(rolland.admin)
        
        self.assertFalse(zoe.active)
        self.assertFalse(zoe.admin)