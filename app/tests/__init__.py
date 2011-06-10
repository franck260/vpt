# -*- coding: utf-8 -*-

from app.models import *
from app.models.meta import metadata
from app.utils import session
from application import app
from fixture import DataSet, SQLAlchemyFixture
from fixture.style import NamedDataStyle
from web import config
import datetime
import hashlib
import web
try:
    import unittest2 as unittest
except ImportError:
    import unittest

_md5 = lambda s : hashlib.md5(s).hexdigest()

class UserData(DataSet):
    class franck_l:
        # id = 1
        prenom = "Franck"
        nom = "Lasry"
        pseudo = "Franck L"
        email = "franck.lasry@gmail.com"
        is_admin = 0
        password = _md5("secret1")
    class franck_p:
        # id = 2
        prenom = "Franck"
        nom = "Perez"
        pseudo = "Franck P"
        email = "franck.perez@gmail.com"
        is_admin = 1
        password = _md5("secret2")
    class fx:
        # id = 3
        prenom = "Francois-Xavier"
        nom = "Clair"
        pseudo = "FX"
        email = "fxclair@gmail.com"
        is_admin = 0
        password = _md5("secret3")
    class jo:
        # id = 4
        prenom = "Jonathan"
        nom = "Levy"
        pseudo = "Jo"
        email = "jolevy23@gmail.com"
        is_admin = 0
        password = _md5("secret4")
    class nico:
        # id = 5
        prenom = "Nicolas"
        nom = "Chaves"
        pseudo = "Nico"
        email = "chavesnicolas@gmail.com"
        is_admin = 0
        password = _md5("secret5")
    class rolland:
        # id = 6
        prenom = "Rolland"
        nom = "Quillevere"
        pseudo = "Rolex"
        email = "rolland.quillevere@gmail.com"
        is_admin = 0
        password = _md5("secret6")


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
    
class TournamentCommentData(DataSet):
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
        comments = [TournamentCommentData.comment_121, TournamentCommentData.comment_122, TournamentCommentData.comment_123]
        results = [ResultData.result12_franck_p, ResultData.result12_jo, ResultData.result12_fx]
    class tournament_21:
        date_tournoi = datetime.date(2010, 9, 1)
        buyin = 10        
        season = SeasonData.season_2
        comments = [TournamentCommentData.comment_211]
        results = [ResultData.result21_jo, ResultData.result21_fx]

class WebTestCase(unittest.TestCase):
    """ Parent of all test classes based on a Web architecture (controllers, models...) """
        
    def setUp(self):
        # remove the session once per test so that 
        # objects do not leak from test to test
        config.orm.remove()

# Configuration of the application
app.configure("testing.cfg")

# Creation of the model
metadata.create_all(config.engine)
web.debug("[MODEL] Successfully created the model (engine = %s)" % config.engine)

dbfixture = SQLAlchemyFixture(
    env=globals(),
    engine=config.engine,
    style=NamedDataStyle()
)


