# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from app.models.results import SeasonResult
from app.models.tournaments import Tournament
from itertools import groupby
from sqlalchemy import Table, Column, Integer
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import mapper, relationship, joinedload
from sqlalchemy.sql.expression import desc
from web import config
import web

                                   
seasons_table = Table("SEASONS", metadata,
                      Column("id", Integer, primary_key=True, nullable=False),
                      Column("start_year", Integer, nullable=False),
                      Column("end_year", Integer, nullable=False),
                      )

class Season(Base):
    
    @classmethod
    def all(cls, order_by_clause=None):
        """ Overrides the default all method to guarantee the order by """
        return Base.all.im_func(Season, order_by_clause=order_by_clause or desc(Season.start_year)) #@UndefinedVariable
    
    @property
    def results(self):
        
        # Initializes the resulting list
        season_results = []
        
        # First fetches all tournaments of the season (with joined results), then filters & orders the results
        # Theoretically it would make sense to query the usable results directly but too many queries would be issued to back-populate the tournaments later (with all results) 
        # usable_results = config.orm.query(Result).join(Result.tournament).join(Tournament.season).filter(Season.id == self.id).filter(Result.rank != None).order_by(Result.user_id).all()
        season_tournaments = config.orm.query(Tournament).options(joinedload(Tournament.results)).join(Tournament.season).filter(Season.id == self.id).all() #@UndefinedVariable
        usable_results = [result for tournament in season_tournaments for result in tournament.results if result.rank is not None]
        usable_results.sort(key = lambda r: r.user_id)
        
        # Groups the results by user (works because the results are ordered)
        for user, iter_user_results in groupby(usable_results, lambda r: r.user):
            
            user_results = list(iter_user_results)
            
            attended = len(user_results)
            buyin = sum([result.buyin for result in user_results])
            profit = sum([result.profit for result in user_results if result.profit]) or None
            score = sum([result.score for result in user_results])
            
            season_results.append(SeasonResult(user, attended, buyin, None, profit, score))
        
        # Sorts the list by score
        season_results.sort(key = lambda r: r.score, reverse=True)
        
        # Calculates the rank (Python 2.7)
        for rank, result in enumerate(season_results, start=1):
            result.rank = rank        
                    
        return season_results

    def reorder_tournaments(self):
        """ Reorders (i.e. enforce position) the tournaments by date. Useful when a tournament was appended in the end of the collection for example """
        
        self.tournaments.sort(key = lambda tournament: tournament.tournament_dt)
        self.tournaments.reorder()

    def __repr__(self) : 
        return "<Season(%s,%s)>" % (self.start_year, self.end_year)


mapper(Season, seasons_table, properties={
    "tournaments": relationship(Tournament, lazy="joined", backref="season", collection_class=ordering_list("position", count_from=1), order_by=Tournament.position) #@UndefinedVariable
})

web.debug("[MODEL] Successfully mapped Season class")
