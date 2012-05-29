# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from app.models.users import User
from app.utils import Enum
from sqlalchemy import Table, Column, Integer, Text, String, DateTime, \
    ForeignKey
from sqlalchemy.orm import mapper, relationship
import datetime
import web

comments_table = Table("COMMENTS", metadata,
                       Column("comment_id", Integer, primary_key=True, nullable=False),
                       Column("user_id", Integer, ForeignKey("USERS.id"), nullable=False),
                       Column("type", String(1), nullable=False),
                       Column("comment", Text, nullable=False),
                       Column("comment_dt", DateTime, nullable=False)
                       )

tournament_comments_table = Table("TOURNAMENT_COMMENTS", metadata,
                                  Column("comment_id", Integer, ForeignKey("COMMENTS.comment_id"), primary_key=True, nullable=False),
                                  Column("tournament_id", Integer, ForeignKey("TOURNAMENTS.id"), nullable=False)             
                                  )

poll_comments_table = Table("POLL_COMMENTS", metadata,
                            Column("comment_id", Integer, ForeignKey("COMMENTS.comment_id"), primary_key=True, nullable=False),
                            Column("poll_id", Integer, ForeignKey("POLLS.id"), nullable=False)          
                            )

class BaseComment(Base):
    """ Base 'abstract' comment - must be subclassed by actual comments types """ 
    
    TYPES = Enum(["T", "S", "P"])
    
    def __init__(self, user=None, comment=None, comment_dt=None):
        self.user = user
        self.comment = comment
        self.comment_dt = comment_dt or datetime.datetime.now()
    
    def __repr__(self) : 
        return "<Comment(%s,%s,%s)>" % (self.user.pseudonym, self.comment, self.comment_dt)

class TournamentComment(BaseComment):
    """ Tournament comments """
    pass

class PollComment(BaseComment):
    """ Poll comments """
    pass

mapper(BaseComment, comments_table, polymorphic_on=comments_table.c.type, polymorphic_identity=None, properties={
    "user": relationship(User, lazy="joined")
})

mapper(TournamentComment, tournament_comments_table, inherits=BaseComment, polymorphic_identity=BaseComment.TYPES.T)
web.debug("[MODEL] Successfully mapped TournamentComment class")

mapper(PollComment, poll_comments_table, inherits=BaseComment, polymorphic_identity=BaseComment.TYPES.P)
web.debug("[MODEL] Successfully mapped PollComment class")
