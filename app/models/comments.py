# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from app.models.users import User
from app.utils import Enum
from sqlalchemy import Table, Column, Integer, Text, String, TIMESTAMP, \
    ForeignKey
from sqlalchemy.orm import mapper, relationship
import datetime
import web

comments_table = Table("COMMENTS", metadata,
                       Column("comment_id", Integer, primary_key=True, nullable=False),
                       Column("user_id", Integer, ForeignKey("USERS.id"), nullable=False),
                       Column("type", String(1), nullable=False),
                       Column("comment", Text, nullable=False),
                       Column("comment_dt", TIMESTAMP, default=datetime.datetime.now(), nullable=False)
                       )

tournament_comments_table = Table("TOURNAMENT_COMMENTS", metadata,
                                  Column("comment_id", Integer, ForeignKey("COMMENTS.comment_id"), primary_key=True, nullable=False),
                                  Column("tournament_id", Integer, ForeignKey("TOURNAMENTS.id"), nullable=False),                 
                                  )


class BaseComment(Base):
    """ Base 'abstract' comment - must be subclassed by actual comments types """ 
    
    TYPES = Enum(["T", "S"])
    
    def __init__(self, user=None, comment=None):
        self.user = user
        self.comment = comment
    
    def __repr__(self) : 
        return "<Comment(%s,%s,%s)>" % (self.user.pseudo, self.comment, self.comment_dt)

class TournamentComment(BaseComment):
    """ Tournament comments """
    pass

mapper(BaseComment, comments_table, polymorphic_on=comments_table.c.type, polymorphic_identity=None, properties={
    "user": relationship(User)
})

mapper(TournamentComment, tournament_comments_table, inherits=BaseComment, polymorphic_identity=BaseComment.TYPES.T)

web.debug("[MODEL] Successfully mapped TournamentComment class")

