# -*- coding: utf-8 -*-

'''
Created on 13 janv. 2011

@author: fperez
'''

from app.models import metadata, Base
from sqlalchemy import Table, Column, String, TIMESTAMP
from sqlalchemy.orm import mapper
import web

                       
# Définition de la table
sessions_table = Table('SESSIONS', metadata,
                       Column('session_id', String(128), primary_key=True),
                       Column('atime', TIMESTAMP, nullable=False),
                       Column('data', String)
                       )

# Définition de la classe
class Session(Base):
    
    def __init__(self, session_id, atime, data) :
        
        self.session_id = session_id
        self.atime = atime
        self.data = data
        
    def __repr__(self) : 
        return "<Session('%s','%s','%s')>" % (self.session_id, self.atime, self.data)

# Définition du mapping
mapper(Session, sessions_table)
web.debug("[MODEL] Armement OK du mapping Session")