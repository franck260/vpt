# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
import web

users_table = Table("USERS", metadata,
                    Column("id", Integer, primary_key=True, nullable=False),
                    Column("first_name", String(20), nullable=False),
                    Column("last_name", String(20), nullable=False),
                    Column("pseudonym", String(20), nullable=False),
                    Column("email", String(50), unique = True, nullable=False),
                    Column("is_admin", Integer, nullable=False),
                    Column("password", String(32), nullable=False),
                    )

class User(Base):
    
    def __init__(self, first_name=None, last_name=None, pseudonym=None, email=None, is_admin=None, password=None) :
        
        self.first_name = first_name
        self.last_name = last_name
        self.pseudonym = pseudonym
        self.email = email
        self.is_admin = is_admin
        self.password = password
        
        
    def __repr__(self) : 
        return "<User(%s,%s,%s,%s,%s,%s)>" % (self.first_name, self.last_name, self.pseudonym, self.email, self.is_admin, self.password)

    def __eq__(self, other):
        
        return self.first_name == other.first_name \
           and self.last_name == other.last_name   \
           and self.pseudonym == other.pseudonym   \
           and self.email == other.email           \
           and self.is_admin == other.is_admin     \
           and self.password == other.password
           

mapper(User, users_table)
web.debug("[MODEL] Successfully mapped User class")
