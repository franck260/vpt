# -*- coding: utf-8 -*-

'''
Created on 20 janv. 2011

@author: fperez
'''

from app.models import metadata, Base
from app.models.users import User
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import mapper, relationship
import datetime
import web

                       
# Définition de la table
comments_table = Table('COMMENTS', metadata,
                      Column('id', Integer, primary_key=True, nullable=False),
                      Column('tournament_id', Integer, ForeignKey('TOURNAMENTS.id'), nullable=False),
                      Column('user_id', Integer, ForeignKey('USERS.id'), nullable=False),
                      Column('comment', String, nullable=False),
                      Column('comment_dt', TIMESTAMP, default=datetime.datetime.now(), nullable=False)                  
                      )

# Définition de la classe
class Comment(Base):
    
    def __init__(self, user=None, comment=None):
        self.user = user
        self.comment = comment
    
    def __repr__(self) : 
        return "<Comment('%s','%s','%s')>" % (self.user.pseudo, self.comment, self.comment_dt)
    
        
# Définition du mapping
mapper(Comment, comments_table, properties={
    "user": relationship(User)
})

web.debug("[MODEL] Armement OK du mapping Comment")

