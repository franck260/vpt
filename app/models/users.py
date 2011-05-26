# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from sqlalchemy import Table, Column, Integer, String, Text
from sqlalchemy.orm import mapper
import web

# TODO password should have a size
users_table = Table("USERS", metadata,
                    Column("id", Integer, primary_key=True, nullable=False),
                    Column("prenom", String(20), nullable=False),
                    Column("nom", String(20), nullable=False),
                    Column("pseudo", String(20), nullable=False),
                    Column("email", String(50), unique = True, nullable=False),
                    Column("is_admin", Integer, nullable=False),
                    Column("password", Text, nullable=False),
                    )

class User(Base):
    
#    def __init__(self, prenom, nom, pseudo, email, is_admin, password) :
#        
#        self.prenom = prenom
#        self.nom = nom
#        self.pseudo = pseudo
#        self.email = email
#        self.is_admin = is_admin
#        self.password = password
        
        
    def __repr__(self) : 
        return "<User(%s,%s,%s,%s,%s,%s)>" % (self.prenom, self.nom, self.pseudo, self.email, self.is_admin, self.password)

mapper(User, users_table)
web.debug("[MODEL] Successfully mapped User class")
