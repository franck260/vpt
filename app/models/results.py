# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from app.models.users import User
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relationship
import web

                       
# Définition de la table
results_table = Table('RESULTS', metadata,
                      Column('id', Integer, primary_key=True, nullable=False),
                      Column('tournament_id', Integer, ForeignKey('TOURNAMENTS.id'), nullable=False),
                      Column('user_id', Integer, ForeignKey('USERS.id'), nullable=False),
                      Column('statut', String(1), nullable=False),
                      Column('buyin', Integer, nullable=True),
                      Column('rank', Integer, nullable=True),
                      Column('profit', Integer, nullable=True),
                      )

# Enumération simple
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

class _Result(Base):
    
    def __repr__(self):
        #TODO: afficher le nom de la classe
        return "<Result(%s,%s,%s)>" % (self.user.pseudo, self.buyin, self.rank)

    @property
    def net_profit(self):
        
        if self.buyin is None or self.profit is None or self.profit <= self.buyin:
            return None
        
        return self.profit - self.buyin  


# Définition de la classe
class Result(_Result):
    
    STATUSES = Enum(["A", "M", "P"])
    MIN_SCORE = 5

    @property
    def score(self):
        
        if self.rank is None:
            return None
        
        return 100 - 100 * self.rank / self.tournament.nb_presents or self.MIN_SCORE
        #return 100 * round(1 - float(self.rank) / self.tournament.nb_presents, 2) or 0
    
class SeasonResult(_Result):
    
    def __init__(self, user, attended, buyin, rank, profit, score):
        self.user = user
        self.attended = attended
        self.buyin = buyin
        self.rank = rank
        self.profit = profit
        self.score = score

        

# Définition du mapping
mapper(Result, results_table, properties={
    "user": relationship(User)
})

web.debug("[MODEL] Armement OK du mapping Result")

