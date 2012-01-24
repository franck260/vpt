# -*- coding: utf-8 -*-

from app.models import UserToken
from app.models.tokens import BaseToken
from app.tests import dbfixture, UserTokenData
from app.tests.models import ModelTestCase
from web import config

class TestBaseToken(ModelTestCase):
    
    def setUp(self):
        super(TestBaseToken, self).setUp()
        self.data = dbfixture.data(UserTokenData)
        self.data.setup()

    def tearDown(self):
        self.data.teardown()
    
    def test_generate_random_token(self):
        
        TOKEN_LENGTH = 16
        NUMBER_OF_TOKENS = 50
        
        tokens = [BaseToken.generate_random_token(TOKEN_LENGTH) for _ in xrange(NUMBER_OF_TOKENS)]
        [self.assertEquals(len(token), TOKEN_LENGTH) for token in tokens]
        self.assertEquals(len(set(tokens)), NUMBER_OF_TOKENS)
        
    def text_expired(self):
        
        user_token_expired = config.orm.query(UserToken).filter(UserToken.email == "oscar.wilde@gmail.com").one() #@UndefinedVariable
        user_token_active = config.orm.query(UserToken).filter(UserToken.email == "dorian.gray@gmail.com").one() #@UndefinedVariable
        
        self.assertTrue(user_token_expired.expired)
        self.assertFalse(user_token_active.expired)
        
    def test_expires(self):
        
        user_token_active = config.orm.query(UserToken).filter(UserToken.email == "dorian.gray@gmail.com").one() #@UndefinedVariable
        user_token_active.expire()
        self.assertTrue(user_token_active.expired)
        