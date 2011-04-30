# -*- coding: utf-8 -*-

'''
Created on 17 nov. 2010

@author: fperez
'''

from app.models import metadata, Base
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
import web

                       
# Définition de la table
users_table = Table('USERS', metadata,
                    Column('id', Integer, primary_key=True, nullable=False),
                    Column('prenom', String, nullable=False),
                    Column('nom', String, nullable=False),
                    Column('pseudo', String, nullable=False),
                    Column('email', String, nullable=False),
                    Column('is_admin', Integer, nullable=False),
                    Column('password', String, nullable=False),
                    )

# Définition de l'objet User
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
        return "<User('%s','%s','%s','%s','%s','%s')>" % (self.prenom, self.nom, self.pseudo, self.email, self.is_admin, self.password)

# Définition du mapping
mapper(User, users_table)
web.debug("[MODEL] Armement OK du mapping User")