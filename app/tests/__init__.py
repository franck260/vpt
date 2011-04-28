# -*- coding: utf-8 -*-

'''
Created on 12 mars 2011

@author: Franck
'''

from app.models import *
from app.utils import session
from fixture import DataSet, SQLAlchemyFixture
from fixture.style import NamedDataStyle
from unittest import TestCase
import datetime
import hashlib

class MemorySessionHandler:
    """ Implémentation très simple d'un gestionnaire de session """
    
    def __init__(self, app, store, initializer=None):
        self.is_logged = False
        self.user_id = None
    
    def _cleanup(self):
        pass
    
    def _load(self):
        pass
    
    def _save(self):
        pass
    
    def kill(self):
        self.is_logged = False
        self.user_id = None


_md5 = lambda s : hashlib.md5(s).hexdigest()

class UserData(DataSet):
    class franck_l:
        # id = 1
        prenom = "Franck"
        nom = "Lasry"
        pseudo = "Franck"
        email = "franck.lasry@gmail.com"
        is_admin = 0
        password = _md5("secret")
    class franck_p:
        # id = 2
        prenom = "Franck"
        nom = "Perez"
        pseudo = "Franck"
        email = "franck.perez@gmail.com"
        is_admin = 1
        password = _md5("secret")
    class fx:
        # id = 3
        prenom = "Francois-Xavier"
        nom = "Clair"
        pseudo = "FX"
        email = "fxclair@gmail.com"
        is_admin = 0
        password = _md5("secret")
    class jo:
        # id = 4
        prenom = "Jonathan"
        nom = "Levy"
        pseudo = "Jo"
        email = "jolevy23@gmail.com"
        is_admin = 0
        password = _md5("secret")
    class nico:
        # id = 5
        prenom = "Nicolas"
        nom = "Chaves"
        pseudo = "Nico"
        email = "chavesnicolas@gmail.com"
        is_admin = 0
        password = _md5("secret")
    class rolland:
        # id = 6
        prenom = "Rolland"
        nom = "Quillevere"
        pseudo = "Rolex"
        email = "rolland.quillevere@gmail.com"
        is_admin = 0
        password = _md5("secret")


class SeasonData(DataSet):
    class season_1:
        start_year = 2009
        end_year = 2010
    class season_2:
        start_year = 2010
        end_year = 2011

class ResultData(DataSet):
    class result11_franck_p:
        user = UserData.franck_p
        statut = Result.STATUSES.P
        buyin = 10
        rank = 1
        profit = 35
    class result11_jo:
        user = UserData.jo
        statut = Result.STATUSES.P
        buyin = 20
        rank = 2
        profit = 5
    class result11_nico:
        user = UserData.nico
        statut = Result.STATUSES.P
        buyin = 10
        rank = 3
    class result11_fx:
        user = UserData.fx
        statut = Result.STATUSES.M
    class result11_franck_l:
        user = UserData.franck_l
        statut = Result.STATUSES.A
    class result12_franck_p:
        user = UserData.franck_p
        statut = Result.STATUSES.P
        buyin = 5
        rank = 1
        profit = 10
    class result12_jo:
        user = UserData.jo
        statut = Result.STATUSES.P
        buyin = 5
        rank = 2
    class result12_fx:
        user = UserData.fx
        statut = Result.STATUSES.A
    class result21_jo:
        user = UserData.jo
        statut = Result.STATUSES.P
        buyin = 10
    class result21_fx:
        user = UserData.fx
        statut = Result.STATUSES.P
        buyin = 10
    
class CommentData(DataSet):
    class comment_121:
        user = UserData.franck_p
        comment = "Hello"
    class comment_122:
        user = UserData.rolland
        comment = "Salut Franck"
    class comment_123:
        user = UserData.fx
        comment = "Salut Rolland et Franck"
    class comment_211:
        user = UserData.franck_p
        comment = "Salut les amis !\nJe suis Franck"
    
class TournamentData(DataSet):
    class tournament_11:
        date_tournoi = datetime.date(2009, 9, 1)
        buyin = 10
        season = SeasonData.season_1
        results = [ResultData.result11_franck_p, ResultData.result11_jo, ResultData.result11_nico, ResultData.result11_fx, ResultData.result11_franck_l]
    class tournament_12:
        date_tournoi = datetime.date(2010, 1, 1)
        buyin = 10
        season = SeasonData.season_1
        comments = [CommentData.comment_121, CommentData.comment_122, CommentData.comment_123]
        results = [ResultData.result12_franck_p, ResultData.result12_jo, ResultData.result12_fx]
    class tournament_21:
        date_tournoi = datetime.date(2010, 9, 1)
        buyin = 10        
        season = SeasonData.season_2
        comments = [CommentData.comment_211]
        results = [ResultData.result21_jo, ResultData.result21_fx]

class WebTestCase(TestCase):
    """ Superclasse des tests s'appuyant sur l'architecture Web (contrôleurs, modèles...) """
        
    def setUp(self):
        # remove the session once per test so that 
        # objects do not leak from test to test
        orm.remove()

# Initialisation de la session web
session.init_manager(MemorySessionHandler)
    
# Initialisation de la session SQLAlchemy
engine = init_sqlalchemy_session("sqlite:///:memory:", echo = False)
metadata.create_all(engine)

dbfixture = SQLAlchemyFixture(
    env=globals(),
    engine=engine,
    style=NamedDataStyle()
)


