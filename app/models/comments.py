# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from app.models.users import User
from sqlalchemy import Table, Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import mapper, relationship
import datetime
import web

comments_table = Table("COMMENTS", metadata,
                      Column("id", Integer, primary_key=True, nullable=False),
                      Column("tournament_id", Integer, ForeignKey("TOURNAMENTS.id"), nullable=False),
                      Column("user_id", Integer, ForeignKey("USERS.id"), nullable=False),
                      Column("comment", Text, nullable=False),
                      Column("comment_dt", TIMESTAMP, default=datetime.datetime.now(), nullable=False)                  
                      )

class Comment(Base):
    
    def __init__(self, user=None, comment=None):
        self.user = user
        self.comment = comment
    
    def __repr__(self) : 
        return "<Comment(%s,%s,%s)>" % (self.user.pseudo, self.comment, self.comment_dt)
    
        
mapper(Comment, comments_table, properties={
    "user": relationship(User)
})

web.debug("[MODEL] Successfully mapped Comment class")

