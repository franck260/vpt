# -*- coding: utf-8 -*-

'''
Created on 17 nov. 2010

@author: fperez
'''

from app.models import orm, metadata, Base
from app.models.comments import Comment
from app.models.results import Result, results_table
from sqlalchemy import Table, Column, Integer, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.expression import desc
import datetime
import web

                       
# Définition de la table
tournaments_table = Table('TOURNAMENTS', metadata,
                          Column('id', Integer, primary_key=True, nullable=False),
                          Column('date_tournoi', Date, nullable=False),
                          Column('buyin', Integer, nullable=False),
                          Column('season_id', Integer, ForeignKey('SEASONS.id'), nullable=False),
                          Column('position', Integer, nullable=True)
                          )



# Les différents statuts possibles de participation à un tournoi
# TODO: basculer dans la classe

# Définition de l'objet Tournament
class Tournament(Base):
    
    @staticmethod
    def get_tournaments(season_id, position):
        """ Retourne un tuple du type (tournament_id, previous_tournament_id, next_tournament_id) """
        
        # Si position = 2, tuples est du type [(9, 1), (10, 2), (11, 3)]
        tuples = orm.query(Tournament.id, Tournament.position)                          \
                    .filter(Tournament.season_id == season_id)                          \
                    .filter(Tournament.position.between(position - 1, position + 1))    \
                    .all()
                    
        ids, positions = zip(*tuples) if tuples else ((), ())
        # Hack : Python < 2.7 => tuple n'est pas itérable
        _id = lambda position: ids[list(positions).index(position)] if position in positions else None
                   
        return (_id(position), _id(position - 1), _id(position + 1))
        
    
    @staticmethod
    def next_tournament():
        """ Renvoie le prochain tournoi, en terme de date absolue """
        
        return orm.query(Tournament)                                              \
                  .filter(Tournament.date_tournoi >= datetime.date.today())       \
                  .order_by(Tournament.date_tournoi)                              \
                  .first()                                                 
        
#    def __init__(self, date_tournoi, season, results) :
#        
#        self.date_tournoi = date_tournoi
#        self.season = season
#        self.results = results
        
    def __repr__(self) : 
        return "<Tournament(#%s-%s, %s, %d)>" % (self.season.id, self.position, self.date_tournoi, self.buyin)
    
    def subscribe(self, user, statut):
        """ Inscrit ou modifie l'inscription (INSERT OR UPDATE) de l'utilisateur passé en paramètre pour le tournoi courant """
        
        # Calcul de la mise courante
        buyin = self.buyin if statut == Result.STATUSES.P else None
            
        # Remontée de l'éventuel résultat déjà présent en base
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
        """ Ajoute le commentaire passé en paramètre au tournoi courant """
        
        self.comments.append(Comment(user, comment))
    
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

# Définition du mapping
mapper(Tournament, tournaments_table, properties={
    "results": relationship(Result, backref="tournament", order_by=[desc(results_table.c.statut), results_table.c.rank, results_table.c.user_id], cascade="save-update, merge, delete"), #@UndefinedVariable
    "comments": relationship(Comment, backref="tournament", order_by=Comment.comment_dt, cascade="save-update, merge, delete") #@UndefinedVariable
})

web.debug("[MODEL] Armement OK du mapping Tournament")

