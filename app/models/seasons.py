# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from app.models.results import Result, SeasonResult
from app.models.tournaments import Tournament, tournaments_table
from itertools import groupby
from sqlalchemy import Table, Column, Integer
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import mapper, relationship
import web
from web import config

                                   
seasons_table = Table("SEASONS", metadata,
                      Column("id", Integer, primary_key=True, nullable=False),
                      Column("start_year", Integer, nullable=False),
                      Column("end_year", Integer, nullable=False),
                      )

class Season(Base):
    
    @property
    def results(self):
        
        # Initializes the resulting list
        season_results = []
        
        # Fetches all usable results of the season (with a rank)
        usable_results = config.orm.query(Result).join(Result.tournament).join(Tournament.season).filter(Season.id == self.id).filter(Result.rank != None).order_by(Result.user_id).all() #@UndefinedVariable
        
        # Groups the results by user (works because the results are ordered)
        for user, iter_user_results in groupby(usable_results, lambda r: r.user):
            
            user_results = list(iter_user_results)
            
            attended = len(user_results)
            buyin = sum([result.buyin for result in user_results])
            profit = sum([result.profit for result in user_results if result.profit]) or None
            score = sum([result.score for result in user_results])
            
            season_results.append(SeasonResult(user, attended, buyin, None, profit, score))
        
        # Sorts the list by score
        season_results.sort(key = lambda r: r.score, reverse = True)
        
        # Calculates the rank
        # Hack : Python < 2.7 => for rank, result in enumerate(season_results, start = 1)
        for rank, result in enumerate(season_results):
            result.rank = rank + 1           
                    
        return season_results
    
    def __repr__(self) : 
        return "<Season(%s,%s)>" % (self.start_year, self.end_year)


mapper(Season, seasons_table, properties={
    "tournaments": relationship(Tournament, backref="season", collection_class=ordering_list("position", count_from=1), order_by=[tournaments_table.c.position]) #@UndefinedVariable
})

web.debug("[MODEL] Successfully mapped Season class")
