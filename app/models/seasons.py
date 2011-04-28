# -*- coding: utf-8 -*-

'''
Created on 17 nov. 2010

@author: fperez
'''

from app.models import metadata, Base, orm
from app.models.results import Result, SeasonResult
from app.models.tournaments import Tournament, tournaments_table
from itertools import groupby
from sqlalchemy import Table, Column, Integer
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import mapper, relationship

                 
                                   
# Définition de la table
seasons_table = Table('SEASONS', metadata,
                      Column('id', Integer, primary_key=True, nullable=False),
                      Column('start_year', Integer, nullable=False),
                      Column('end_year', Integer, nullable=False),
                      )

# Définition de l'objet Season
class Season(Base):
    
    @property
    def results(self):
        
        # Initialisation de la liste résultat
        season_results = []
        
        # On remonte tous les résultats utilisables de la saison (avec un classement)
        usable_results = orm.query(Result).join(Result.tournament).join(Tournament.season).filter(Season.id == self.id).filter(Result.rank != None).order_by(Result.user_id).all() #@UndefinedVariable
        
        # On regroupe les résultats par utilisateur
        for user, iter_user_results in groupby(usable_results, lambda r: r.user):
            
            user_results = list(iter_user_results)
            
            attended = len(user_results)
            buyin = sum([result.buyin for result in user_results])
            profit = sum([result.profit for result in user_results if result.profit]) or None
            score = sum([result.score for result in user_results])
            print user, user_results, buyin, profit, score
            
            season_results.append(SeasonResult(user, attended, buyin, None, profit, score))
        
        # On trie la liste par score
        season_results.sort(key = lambda r: r.score, reverse = True)
        
        # On affecte un classement
        for rank, result in enumerate(season_results, start = 1):
            result.rank = rank            
                    
        return season_results
    
    def __repr__(self) : 
        return "<Season(%s,%s)>" % (self.start_year, self.end_year)

#def my_ordering_list(attr, count_from=None, **kw):
#
#    kw = _unsugar_count_from(count_from=count_from, **kw)
#    return lambda: MyOrderingList(attr, **kw)
#
#class MyOrderingList(OrderingList):
#            
#    def append(self, entity):
#        print "Entrée dans le append customisé"
#        super(OrderingList, self).append(entity)
#        self.sort(key = lambda tournament: tournament.date_tournoi)
#        print self
#        self._order_entity(len(self) - 1, entity, self.reorder_on_append)


# Définition du mapping : les tournois sont remontés dynamiquement
mapper(Season, seasons_table, properties={
    "tournaments": relationship(Tournament, backref="season", collection_class=ordering_list("position", count_from=1), order_by=[tournaments_table.c.position]) #@UndefinedVariable
})

print "[MODEL] Armement OK du mapping Season"
