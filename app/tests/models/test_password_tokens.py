# -*- coding: utf-8 -*-

from app.models import PasswordToken, User
from app.tests import dbfixture, UserTokenData, PasswordTokenData, UserData
from app.tests.models import ModelTestCase
from web import config

class TestPasswordToken(ModelTestCase):
    
    def setUp(self):
        super(TestPasswordToken, self).setUp()
        self.data = dbfixture.data(UserTokenData, PasswordTokenData)
        self.data.setup()

    def tearDown(self):
        self.data.teardown()

    def test_all(self):
        
        all_password_tokens = PasswordToken.all()
        self.assertEqual(len(all_password_tokens), 2)
        [self.assertIsInstance(token, PasswordToken) for token in all_password_tokens]
        
    def test_get(self):
        
        password_token_expired = config.orm.query(PasswordToken).join(PasswordToken.user).filter(User.email == "nico@gmail.com").one() #@UndefinedVariable
        password_token_active = config.orm.query(PasswordToken).join(PasswordToken.user).filter(User.email == "jo@gmail.com").one() #@UndefinedVariable
        
        self.assertEquals(password_token_expired.token, "goB9Z7fhsUrjXHDi")
        self.assertEquals(password_token_expired.user, UserData.nico)
        self.assertEquals(password_token_active.token, "xYCPayfPCPEPCPaL")
        self.assertEquals(password_token_active.user, UserData.jo)
        
    def test_get_token(self):
        
        # These tests work because a PasswordTokenData has a similar structure to a PasswordToken
        # When Tournament.__eq__ is called, it compares the fields without caring of the parameters' actual types
        
        self.assertIsNone(PasswordToken.get_token(None))
        self.assertIsNone(PasswordToken.get_token(""))
        self.assertIsNone(PasswordToken.get_token("invalid_token"))
        self.assertIsNone(PasswordToken.get_token("znc9TNqpajeN2nEH"))
        self.assertIsNone(PasswordToken.get_token("xjRp67wh3HdjEI6I"))
        
        self.assertEquals(PasswordToken.get_token("goB9Z7fhsUrjXHDi"), PasswordTokenData.password_token_expired)
        self.assertEquals(PasswordToken.get_token("xYCPayfPCPEPCPaL"), PasswordTokenData.password_token_active)
                
