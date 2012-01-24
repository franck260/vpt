# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from app.models.users import User
from app.utils import Enum
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.orm.exc import NoResultFound
from web import config
import datetime
import random
import web

tokens_table = Table("TOKENS", metadata,
                     Column("token_id", Integer, primary_key=True, nullable=False),
                     Column("token", String(16), unique=True, nullable=False),
                     Column("type", String(1), nullable=False),
                     Column("creation_dt", DateTime, nullable=False),
                     Column("expiration_dt", DateTime, nullable=False)
                     )

user_tokens_table = Table("USER_TOKENS", metadata,
                          Column("token_id", Integer, ForeignKey("TOKENS.token_id"), primary_key=True, nullable=False),
                          Column("email", String(50), nullable=False),
                          Column("level", Integer, nullable=False)
                          )

password_tokens_table = Table("PASSWORD_TOKENS", metadata,
                              Column("token_id", Integer, ForeignKey("TOKENS.token_id"), primary_key=True, nullable=False),
                              Column("user_id", Integer, ForeignKey("USERS.id"), nullable=False)
                              )

class BaseToken(Base):
    """ Base 'abstract' token - must be subclassed by actual tokens types """ 
    
    @classmethod
    def get_token(cls, token):
        """ Returns the user token matching the parameter, or None if it could not be found """
        
        if not token:
            return None
        
        try:
            result = config.orm.query(cls).filter(cls.token == token).one()
        except NoResultFound:
            result = None
        
        return result

    @staticmethod
    def generate_random_token(token_length):
        """ Simple token generator (http://code.activestate.com/recipes/473852-password-generator) """
    
        lefthand = "789yuiophjknmYUIPHJKLNM"
        righthand = "23456qwertasdfgzxcvbQWERTASDFGZXCVB"
        
        result = []
        
        for i in xrange(token_length):
            available_characters = lefthand if i % 2 else righthand
            result.append(random.choice(available_characters))
            
        return "".join(result)
    
    TYPES = Enum([
        "U", # UserToken
        "P"  # PasswordToken
    ])
    
    # Default token validity in days
    DEFAULT_VALIDITY = 30
    
    def __init__(self, token=None, creation_dt=None, validity=None) :
        
        self.token = token
        self.creation_dt = creation_dt or datetime.datetime.now()
        validity = validity or self.DEFAULT_VALIDITY
        self.expiration_dt = self.creation_dt + datetime.timedelta(days=validity)

    def __repr__(self) : 
        return "<BaseToken(%s,%s,%s)>" % (self.token, self.creation_dt, self.expiration_dt)
    
    @property
    def expired(self):
        return datetime.datetime.now() >= self.expiration_dt
    
    def expire(self):
        """ Forces the immediate expiration of a token (typically when successfully used) """
        self.expiration_dt = datetime.datetime.now()
    
class UserToken(BaseToken):
    """ User tokens """
  
    def __eq__(self, other):

        # Horrible hack to bypass FormAlchemy controls (!?)
        if isinstance(other, type):
            return False

        return self.token == other.token                   \
           and self.creation_dt == other.creation_dt       \
           and self.expiration_dt == other.expiration_dt   \
           and self.email == other.email                   \
           and self.level == other.level

class PasswordToken(BaseToken):
    """ Password tokens """

    def __init__(self, token=None, creation_dt=None, validity=None, user=None) :
        
        super(PasswordToken, self).__init__(token, creation_dt, validity)
        self.user = user

    @staticmethod
    def get_password_token(email):
        """ Returns the active password token matching the email, or None if no such token could be found """
        
        if not email:
            return None
        
        try:
            password_token = config.orm.query(PasswordToken)                                          \
                                       .join(PasswordToken.user)                                      \
                                       .filter(User.email == email)                                   \
                                       .filter(PasswordToken.expiration_dt > datetime.datetime.now()) \
                                       .one()
        except NoResultFound:
            password_token = None
        
        return password_token
    
    def __eq__(self, other):

        return self.token == other.token                   \
           and self.creation_dt == other.creation_dt       \
           and self.expiration_dt == other.expiration_dt   \
           and self.user == other.user

mapper(BaseToken, tokens_table, polymorphic_on=tokens_table.c.type, polymorphic_identity=None)
mapper(UserToken, user_tokens_table, inherits=BaseToken, polymorphic_identity=BaseToken.TYPES.U)
mapper(PasswordToken, password_tokens_table, inherits=BaseToken, polymorphic_identity=BaseToken.TYPES.P, properties={
    "user": relationship(User)
})

web.debug("[MODEL] Successfully mapped UserToken class")
