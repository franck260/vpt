# -*- coding: utf-8 -*-

from app.models import UserToken
from app.tests import dbfixture, UserTokenData, PasswordTokenData
from app.tests.models import ModelTestCase
from web import config

class TestUserToken(ModelTestCase):
    
    def setUp(self):
        super(TestUserToken, self).setUp()
        self.data = dbfixture.data(UserTokenData, PasswordTokenData)
        self.data.setup()

    def tearDown(self):
        self.data.teardown()

    def test_all(self):
        
        all_user_tokens = UserToken.all()
        self.assertEqual(len(all_user_tokens), 2)
        [self.assertIsInstance(token, UserToken) for token in all_user_tokens]
        
    def test_get(self):
        
        user_token_expired = config.orm.query(UserToken).filter(UserToken.email == "oscar.wilde@gmail.com").one() #@UndefinedVariable
        user_token_active = config.orm.query(UserToken).filter(UserToken.email == "dorian.gray@gmail.com").one() #@UndefinedVariable
        level1_tokens = config.orm.query(UserToken).filter(UserToken.level == 1).all() #@UndefinedVariable
        
        self.assertEquals(user_token_expired.token, "znc9TNqpajeN2nEH")
        self.assertEquals(user_token_expired.level, 1)
        self.assertEquals(user_token_active.token, "xjRp67wh3HdjEI6I")
        self.assertEquals(user_token_active.level, 1)
        self.assertEqual(len(level1_tokens), 2)
        
    def test_get_token(self):
        
        # These tests work because a UserTokenData has a similar structure to a UserToken
        # When Tournament.__eq__ is called, it compares the fields without caring of the parameters' actual types
        
        self.assertIsNone(UserToken.get_token(None))
        self.assertIsNone(UserToken.get_token(""))
        self.assertIsNone(UserToken.get_token("invalid_token"))
        self.assertIsNone(UserToken.get_token("goB9Z7fhsUrjXHDi"))
        self.assertIsNone(UserToken.get_token("xYCPayfPCPEPCPaL"))
        
        self.assertEquals(UserToken.get_token("znc9TNqpajeN2nEH"), UserTokenData.user_token_expired)
        self.assertEquals(UserToken.get_token("xjRp67wh3HdjEI6I"), UserTokenData.user_token_active)
                
