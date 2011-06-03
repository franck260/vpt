# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from app.models.comments import TournamentComment
from app.models.results import Result, results_table
from sqlalchemy import Table, Column, Integer, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.expression import desc
import datetime
import web
from web import config

                       
tournaments_table = Table("TOURNAMENTS", metadata,
                          Column("id", Integer, primary_key=True, nullable=False),
                          Column("date_tournoi", Date, nullable=False),
                          Column("buyin", Integer, nullable=False),
                          Column("season_id", Integer, ForeignKey("SEASONS.id"), nullable=False),
                          Column("position", Integer, nullable=True)
                          )

class Tournament(Base):
    
    @staticmethod
    def get_tournaments(season_id, position):
        """
        Returns a tuple composed of 3 items : (tournament, previous_tournament, next_tournament)
        where tournament.season_id and tournament.position correspond to the parameters.
        
        Each item may be None (the resulting tuple has a constant size).
        """
        
        # Fetches the tournament and its surrounders (if any)
        tournaments = config.orm.query(Tournament)                                             \
                           .filter(Tournament.season_id == season_id)                          \
                           .filter(Tournament.position.between(position - 1, position + 1))    \
                           .all()
        
        tournaments_by_position = dict([(tournament.position, tournament) for tournament in tournaments])
        return (tournaments_by_position.get(position), tournaments_by_position.get(position - 1), tournaments_by_position.get(position + 1))
        
    
    @staticmethod
    def next_tournament():
        """ Returns the next scheduled tournament, based on the system date """
        
        return config.orm.query(Tournament)                                              \
                         .filter(Tournament.date_tournoi >= datetime.date.today())       \
                         .order_by(Tournament.date_tournoi)                              \
                         .first()                                                 
        
    def __repr__(self) : 
        return "<Tournament(#%s-%s, %s, %d)>" % (self.season.id, self.position, self.date_tournoi, self.buyin)
    
    def __eq__(self, other):
        return self.date_tournoi == other.date_tournoi and self.buyin == other.buyin
    
    def subscribe(self, user, statut):
        """ Subscribes or modifies the subscription (INSERT OR UPDATE) of the user for this tournament instance """
        
        # Calculates the buyin
        buyin = self.buyin if statut == Result.STATUSES.P else None
            
        # Fetches the result already in the database (if any)
        current_result = self.ordered_results.get(user)
        
        if not current_result :
            current_result = Result()
            self.results.append(current_result)
            current_result.user = user

        current_result.statut = statut
        current_result.buyin = buyin
        current_result.rank = None
        current_result.profit = None

    
    def add_comment(self, user, comment):
        """ Adds the comment to this tournament instance """
        self.comments.append(TournamentComment(user, comment))
    
    def _count_results(self, status):
        return [result.statut for result in self.results].count(status)
    
    @property
    def nb_presents(self):
        return self._count_results(Result.STATUSES.P)
    
    @property
    def nb_absents(self):
        return self._count_results(Result.STATUSES.A)
    
    @property
    def somme_en_jeu(self):
        return sum([result.buyin for result in self.results if result.statut == Result.STATUSES.P])
    
    @property
    def future(self):
        return datetime.date.today() <= self.date_tournoi
    
    @property
    def ordered_results(self):
        return dict([(result.user, result) for result in self.results])

mapper(Tournament, tournaments_table, properties={
    "results": relationship(Result, backref="tournament", order_by=[desc(results_table.c.statut), results_table.c.rank, results_table.c.user_id], cascade="save-update, merge, delete"), #@UndefinedVariable
    "comments": relationship(TournamentComment, backref="tournament", order_by=TournamentComment.comment_dt, cascade="save-update, merge, delete") #@UndefinedVariable
})
web.debug("[MODEL] Successfully mapped Tournament class")

