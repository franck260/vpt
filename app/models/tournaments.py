# -*- coding: utf-8 -*-

from app.models.comments import TournamentComment
from app.models.meta import metadata, Base
from app.models.results import Result, result_sort_keys
from sqlalchemy import Table, Column, Integer, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship, joinedload
from sqlalchemy.orm.exc import NoResultFound
from web import config
import datetime
import web
                       
tournaments_table = Table("TOURNAMENTS", metadata,
                          Column("id", Integer, primary_key=True, nullable=False),
                          Column("tournament_dt", Date, nullable=False),
                          Column("buyin", Integer, nullable=False),
                          Column("season_id", Integer, ForeignKey("SEASONS.id"), nullable=False),
                          Column("position", Integer, nullable=True)
                          )

class Tournament(Base):
    
    @staticmethod
    def get_tournament(season_id, position):
        """ Returns the tournament matching the parameters, or None if it could not be found """
        
        try:
            tournament = config.orm.query(Tournament)                          \
                                   .options(joinedload(Tournament.results))    \
                                   .filter(Tournament.season_id == season_id)  \
                                   .filter(Tournament.position == position)    \
                                   .one()
        except NoResultFound:
            tournament = None
        
        return tournament
        
    
    @staticmethod
    def next_tournament():
        """ Returns the next scheduled tournament, based on the system date """
        
        return config.orm.query(Tournament)                                              \
                         .filter(Tournament.tournament_dt >= datetime.date.today())       \
                         .order_by(Tournament.tournament_dt)                              \
                         .first()                                                 
        
    def __repr__(self) : 
        return "<Tournament(#%s-%s, %s, %d)>" % (self.season.id, self.position, self.tournament_dt, self.buyin)
    
    def __eq__(self, other):
        
        # Horrible hack to bypass FormAlchemy controls (!?)
        if isinstance(other, type):
            return False
        
        return self.tournament_dt == other.tournament_dt and self.buyin == other.buyin
    
    def subscribe(self, user, status):
        """ Subscribes or modifies the subscription (INSERT OR UPDATE) of the user for this tournament instance """
        
        # Calculates the buyin
        buyin = self.buyin if status == Result.STATUSES.P else None
            
        # Fetches the result already in the database (if any)
        current_result = self.results_by_user.get(user)
        
        if not current_result :
            current_result = Result(user=user)
            self.results.append(current_result)

        current_result.status = status
        current_result.buyin = buyin
        current_result.rank = None
        current_result.profit = None

    
    def add_comment(self, user, comment):
        """ Adds the comment to this tournament instance """
        self.comments.append(TournamentComment(user, comment))
    
    @property
    def sum_in_play(self):
        return sum([result.buyin for result in self.results_by_status(Result.STATUSES.P)])
    
    @property
    def future(self):
        return datetime.date.today() <= self.tournament_dt
    
    @property
    def nb_attending_players(self):
        """ Handy method which returns the number of actually attending players """
        return len(self.results_by_status(Result.STATUSES.P))
    
    @property
    def results_by_user(self):
        return dict([(result.user, result) for result in self.results])

    def results_by_status(self, status):
        """ Returns the tournament results, ordered and filtered by status """
        return filter(lambda result: result.status == status, self.results)
    
    def sort_results(self):
        """ Sorts the tournament results by the same keys used by the ORM """
        self.results.sort(key=result_sort_keys)

# TODO: sort results by pseudonym instead
mapper(Tournament, tournaments_table, properties={
    "results": relationship(Result, backref="tournament", order_by=lambda: result_sort_keys(Result), cascade="save-update, merge, delete"), #@UndefinedVariable
    "comments": relationship(TournamentComment, backref="tournament", order_by=TournamentComment.comment_dt, cascade="save-update, merge, delete") #@UndefinedVariable
})
web.debug("[MODEL] Successfully mapped Tournament class")

