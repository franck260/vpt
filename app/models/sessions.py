# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from sqlalchemy import Table, Column, String, Text, TIMESTAMP
from sqlalchemy.orm import mapper
import web

                       
sessions_table = Table("SESSIONS", metadata,
                       Column("session_id", String(128), primary_key=True),
                       Column("atime", TIMESTAMP, nullable=False),
                       Column("data", Text)
                       )

class Session(Base):
    
    def __init__(self, session_id, atime, data) :
        
        self.session_id = session_id
        self.atime = atime
        self.data = data
        
    def __repr__(self) : 
        return "<Session(%s,%s,%s)>" % (self.session_id, self.atime, self.data)

mapper(Session, sessions_table)
web.debug("[MODEL] Successfully mapped Session class")