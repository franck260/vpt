# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from app.utils import Enum
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from sqlalchemy.orm.exc import NoResultFound
from web import config
import collections
import web

users_table = Table("USERS", metadata,
                    Column("id", Integer, primary_key=True, nullable=False),
                    Column("first_name", String(20), nullable=False),
                    Column("last_name", String(20), nullable=False),
                    Column("pseudonym", String(20), nullable=False),
                    Column("email", String(50), unique=True, nullable=False),
                    Column("password", String(32), nullable=False),
                    Column("level", Integer, nullable=False)
                    )

class User(Base):
    
    # Describes the different user levels : the value in the database corresponds to LevelComponent.value
    BaseLevels = Enum(["DISABLED", "GUEST", "CORE", "ADMIN"])
    LevelComponent = collections.namedtuple("LevelComponent",  ["description", "value"])
    Levels = {
        BaseLevels.DISABLED : LevelComponent("Inactif", 0),
        BaseLevels.GUEST : LevelComponent("Guest", 1),
        BaseLevels.CORE : LevelComponent("Fondateur", 2),
        BaseLevels.ADMIN : LevelComponent("Admin", 3)
    }
    
    def __init__(self, first_name=None, last_name=None, pseudonym=None, email=None, password=None, level=None) :
        
        self.first_name = first_name
        self.last_name = last_name
        self.pseudonym = pseudonym
        self.email = email
        self.password = password
        self.level = level
        
    @classmethod
    def all(cls, order_by_clause=None):
        """ Overrides the default all method to guarantee the order by """
        return Base.all.im_func(User, order_by_clause=order_by_clause or User.email) #@UndefinedVariable

    def __repr__(self) : 
        return "<User(%s,%s,%s,%s,%s,%s)>" % (self.first_name, self.last_name, self.pseudonym, self.email, self.password, self.level)

    def __eq__(self, other):

        # Horrible hack to bypass FormAlchemy controls (!?)
        if isinstance(other, type):
            return False

        return self.first_name == other.first_name \
           and self.last_name == other.last_name   \
           and self.pseudonym == other.pseudonym   \
           and self.email == other.email           \
           and self.password == other.password     \
           and self.level == other.level
           
    @property
    def admin(self):
        return self.level == self.Levels[self.BaseLevels.ADMIN].value

    @property
    def active(self):
        return self.level != self.Levels[self.BaseLevels.DISABLED].value
    
    @staticmethod
    def get_user(email):
        
        if not email:
            return None
           
        try:
            user = config.orm.query(User).filter(User.email == email).one() 
        except NoResultFound:
            user = None
            
        return user


mapper(User, users_table)
web.debug("[MODEL] Successfully mapped User class")
