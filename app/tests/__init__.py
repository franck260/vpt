# -*- coding: utf-8 -*-

from app.models import *
from app.models.meta import metadata
from app.utils import session
from app.utils.session import to_md5
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

class UserData(DataSet):
    class franck_l:
        # id = 1
        first_name = "Franck"
        last_name = "L"
        pseudonym = "Franck L"
        email = "franck.l@gmail.com"
        password = to_md5("secret1")
        level = 2
    class franck_p:
        # id = 2
        first_name = "Franck"
        last_name = "P"
        pseudonym = "Franck P"
        email = "franck.p@gmail.com"
        password = to_md5("secret2")
        level = 3
    class fx:
        # id = 3
        first_name = "Francois-Xavier"
        last_name = "C"
        pseudonym = "FX"
        email = "fx@gmail.com"
        password = to_md5("secret3")
        level = 2
    class jo:
        # id = 4
        first_name = "Jonathan"
        last_name = "L"
        pseudonym = "Jo"
        email = "jo@gmail.com"
        password = to_md5("secret4")
        level = 2
    class nico:
        # id = 5
        first_name = "Nicolas"
        last_name = "C"
        pseudonym = "Nico"
        email = "nico@gmail.com"
        password = to_md5("secret5")
        level = 2
    class rolland:
        # id = 6
        first_name = "Rolland"
        last_name = "Q"
        pseudonym = "Rolex"
        email = "rolland@gmail.com"
        password = to_md5("secret6")
        level = 2
    class zoe:
        # id = 7
        first_name = "Zoe"
        last_name = "Jones"
        pseudonym = "Zoe"
        email = "zoe@gmail.com"
        password = to_md5("secret7")
        level = 0


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
        status = Result.STATUSES.P
        buyin = 10
        rank = 1
        profit = 35
    class result11_jo:
        user = UserData.jo
        status = Result.STATUSES.P
        buyin = 20
        rank = 2
        profit = 5
    class result11_nico:
        user = UserData.nico
        status = Result.STATUSES.P
        buyin = 10
        rank = 3
    class result11_fx:
        user = UserData.fx
        status = Result.STATUSES.M
    class result11_franck_l:
        user = UserData.franck_l
        status = Result.STATUSES.A
    class result12_franck_p:
        user = UserData.franck_p
        status = Result.STATUSES.P
        buyin = 5
        rank = 1
        profit = 10
    class result12_jo:
        user = UserData.jo
        status = Result.STATUSES.P
        buyin = 5
        rank = 2
    class result12_fx:
        user = UserData.fx
        status = Result.STATUSES.A
    class result21_jo:
        user = UserData.jo
        status = Result.STATUSES.P
        buyin = 10
        rank = None
        profit = None
    class result21_fx:
        user = UserData.fx
        status = Result.STATUSES.P
        buyin = 10
        rank = None
        profit = None
    
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
        tournament_dt = datetime.date(2009, 9, 1)
        buyin = 10
        season = SeasonData.season_1
        results = [ResultData.result11_franck_p, ResultData.result11_jo, ResultData.result11_nico, ResultData.result11_fx, ResultData.result11_franck_l]
    class tournament_12:
        tournament_dt = datetime.date(2010, 1, 1)
        buyin = 10
        season = SeasonData.season_1
        comments = [TournamentCommentData.comment_121, TournamentCommentData.comment_122, TournamentCommentData.comment_123]
        results = [ResultData.result12_franck_p, ResultData.result12_jo, ResultData.result12_fx]
    class tournament_21:
        tournament_dt = datetime.date(2010, 8, 1)
        buyin = 10        
        season = SeasonData.season_2
        comments = [TournamentCommentData.comment_211]
        results = [ResultData.result21_jo, ResultData.result21_fx]
        
class NewsData(DataSet):
    class news_1:
        news = u"Lancement du site"
        news_dt = datetime.date(2011, 5, 27)
    class news_2:
        news = u"Nouveau design, corrections de bugs & publication des derniers résultats"
        news_dt = datetime.date(2011, 6, 10)
    class news_3:
        news = u"Fonctionnalité d'édition de profil & publication des derniers résultats"
        news_dt = datetime.date(2011, 7, 13)
    class news_4:
        news = u"Publication des derniers résultats"
        news_dt = datetime.date(2011, 8, 15)

class UserTokenData(DataSet):
    class user_token_expired:
        token = "znc9TNqpajeN2nEH"
        creation_dt = datetime.datetime(2011, 1, 1, 0, 0)
        expiration_dt = datetime.datetime(2011, 1, 31, 0, 0)
        email = "oscar.wilde@gmail.com"
        level = 1
    class user_token_active:
        token = "xjRp67wh3HdjEI6I"
        creation_dt = datetime.datetime(2011, 1, 1, 0, 0)
        expiration_dt = datetime.datetime(2020, 1, 31, 0, 0)
        email = "dorian.gray@gmail.com"
        level = 1
        
class PasswordTokenData(DataSet):
    class password_token_expired:
        token = "goB9Z7fhsUrjXHDi"
        creation_dt = datetime.datetime(2010, 1, 1, 0, 0)
        expiration_dt = datetime.datetime(2010, 1, 31, 0, 0)
        user = UserData.nico
    class password_token_active:
        token = "xYCPayfPCPEPCPaL"
        creation_dt = datetime.datetime(2012, 1, 1, 0, 0)
        expiration_dt = datetime.datetime(2022, 1, 31, 0, 0)
        user = UserData.jo

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


