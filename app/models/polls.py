# -*- coding: utf-8 -*-

from app.models.comments import PollComment
from app.models.meta import metadata, Base
from app.models.users import User
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, Date, \
    Table
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.orm.collections import MappedCollection
from sqlalchemy.util import OrderedDict
import datetime
import operator
import web

class OrderedMappedCollection(OrderedDict, MappedCollection):
    
    def __init__(self, keyfunc):
        MappedCollection.__init__(self, keyfunc)
        OrderedDict.__init__(self) #@UndefinedVariable

poll_choices_table = Table(
    "POLL_CHOICES",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("poll_id", Integer, ForeignKey("POLLS.id"), nullable=False),
    Column("choice_dt", Date, nullable=False)
)

poll_votes_table = Table(
    "POLL_VOTES",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("poll_id", Integer, ForeignKey("POLLS.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("USERS.id"), nullable=False),
    Column("first_vote_dt", DateTime, nullable=False, default=lambda context: context.current_parameters["last_vote_dt"]),
    Column("last_vote_dt", DateTime, nullable=False)
)

poll_user_choices_table = Table(
    "POLL_USER_CHOICES",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("poll_vote_id", Integer, ForeignKey("POLL_VOTES.id"), nullable=False),
    Column("poll_choice_id", Integer, ForeignKey("POLL_CHOICES.id"), nullable=False)
)

polls_table = Table(
    "POLLS",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("title", String(50), nullable=False),
    Column("start_dt", Date, nullable=False, default=datetime.datetime.now),
    Column("end_dt", Date)
)

class PollChoice(Base):
    
    def __init__(self, choice_dt=None):
        self.choice_dt = choice_dt
    
    def __repr__(self) : 
        return "<PollChoice(%s)>" % (self.choice_dt)

class PollVote(Base):

    choices = association_proxy("user_choices", "choice")  

    def __init__(self, user=None, choices=[]):
        self.user = user
        self.choices = choices

    def __repr__(self) : 
        return "<PollVote(%s,%s,%s,%s)>" % (self.user, self.choices, self.first_vote_dt, self.last_vote_dt)

class PollUserChoice(Base):

    def __repr__(self) : 
        return "<PollUserChoice(%s)>" % (self.choice)

    def __init__(self, choice=None):
        self.choice = choice

class Poll(Base):

    possible_dates = association_proxy("choices", "choice_dt")
    choices_by_user = association_proxy("votes_by_user", "choices")

    @classmethod
    def all(cls, order_by_clause=None, joined_attrs=[]):
        """ Overrides the default all method to guarantee the order by """
        return Base.all.im_func(Poll, order_by_clause=order_by_clause or Poll.start_dt, joined_attrs=joined_attrs) #@UndefinedVariable

    def __repr__(self) : 
        return "<Poll(%s)>" % (self.title)
    
    @property
    def expired(self):
        return self.end_dt and self.end_dt < datetime.date.today()
    
    @property
    def has_votes(self):
        return bool(self.choices_by_user)
    
    def vote(self, user, choices):

        if self.expired:
            raise ValueError, u"Le sondage a expire"
        
        if any(choice.poll is not self for choice in choices):
            raise ValueError, u"Un des choix passes ne correspond pas au sondage %s" % (self)
        
        self.choices_by_user[user] = choices
        poll_vote = self.votes_by_user[user]
        poll_vote.last_vote_dt = datetime.datetime.now()
        
        return poll_vote
        
    def add_comment(self, user, comment):
        """ Adds the comment to this poll instance """
        comment = PollComment(user, comment)
        self.comments.append(comment)
        return comment

mapper(PollChoice, poll_choices_table)
web.debug("[MODEL] Successfully mapped PollChoice class")

mapper(PollVote, poll_votes_table, properties={
    "user": relationship(User, lazy="joined"),
    "user_choices": relationship(PollUserChoice, lazy="joined", collection_class=set, cascade="all, delete-orphan")
})
web.debug("[MODEL] Successfully mapped PollVote class")

mapper(PollUserChoice, poll_user_choices_table, properties={
    "choice": relationship(PollChoice, lazy="joined")                                              
})
web.debug("[MODEL] Successfully mapped PollUserChoice class")

mapper(Poll, polls_table, properties={
    "comments": relationship(PollComment, backref="poll", order_by=PollComment.comment_dt, cascade="save-update, merge, delete"),
    "choices": relationship(PollChoice, backref="poll", order_by=PollChoice.choice_dt, cascade="all, delete-orphan"),
    "votes_by_user": relationship(
        PollVote,
        backref="poll",
        order_by=PollVote.first_vote_dt,
        collection_class=lambda: OrderedMappedCollection(operator.attrgetter("user"))
    )
})
web.debug("[MODEL] Successfully mapped Poll class")
