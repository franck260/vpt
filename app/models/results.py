# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from app.models.users import User
from app.utils import Enum
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relationship
import web


results_table = Table("RESULTS", metadata,
                      Column("id", Integer, primary_key=True, nullable=False),
                      Column("tournament_id", Integer, ForeignKey("TOURNAMENTS.id"), nullable=False),
                      Column("user_id", Integer, ForeignKey("USERS.id"), nullable=False),
                      Column("status", String(1), nullable=False),
                      Column("buyin", Integer, nullable=True),
                      Column("rank", Integer, nullable=True),
                      Column("profit", Integer, nullable=True),
                      )



class _Result(Base):
    
    def __repr__(self):
        #TODO: display the actual class
        return "<Result(%s,%s,%s)>" % (self.user.pseudonym, self.buyin, self.rank)

    @property
    def net_profit(self):
        
        if self.buyin is None or self.profit is None or self.profit <= self.buyin:
            return None
        
        return self.profit - self.buyin  


class Result(_Result):
    """ Represents a tournament result """
    
    # A = Absent, M = Missing, P = Present
    STATUSES = Enum(["A", "M", "P"])
    
    # The last player of the game does not get 0 but MIN_SCORE instead
    MIN_SCORE = 5

    @property
    def actual(self):
        """ Is the result actual, i.e. does it represent real data (to be displayed, for instance) """
        return self.status == Result.STATUSES.P

    @property
    def score(self):
        
        if self.rank is None:
            return None
        
        return 100 - 100 * self.rank / self.tournament.nb_attending_players or self.MIN_SCORE
    
class SeasonResult(_Result):
    """ Represents a season result """
    
    def __init__(self, user, attended, buyin, rank, profit, score):
        self.user = user
        self.attended = attended
        self.buyin = buyin
        self.rank = rank
        self.profit = profit
        self.score = score

    @property
    def actual(self):
        """ Is the result actual, i.e. does it represent real data (to be displayed, for instance) ? """
        return True
        

mapper(Result, results_table, properties={
    "user": relationship(User)
})

web.debug("[MODEL] Successfully mapped Result class")

