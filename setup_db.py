# -*- coding: utf-8 -*-

'''
Created on 15 mars 2011

@author: Franck
'''

from app.models import *
from fixture import DataSet, SQLAlchemyFixture
from fixture.style import NamedDataStyle
import config
import datetime
import hashlib

_md5 = lambda s : hashlib.md5(s).hexdigest()

class UserData(DataSet):
    class franck:
        prenom = u"Franck"
        nom = u"Perez"
        pseudo = u"Franck P"
        email = u"franck.perez@gmail.com"
        is_admin = 1
        password = _md5("vpt")
    class jo:
        prenom = u"Jonathan"
        nom = u"Levy"
        pseudo = u"Jo"
        email = u"jolevy23@gmail.com"
        is_admin = 0
        password = _md5("vpt")
    class fx:
        prenom = u"François-Xavier"
        nom = u"Clair"
        pseudo = u"FX"
        email = u"fxclair@gmail.com"
        is_admin = 0
        password = _md5("vpt")
    class nico:
        prenom = u"Nicolas"
        nom = u"Chaves"
        pseudo = u"Nico"
        email = u"chavesnicolas@gmail.com"
        is_admin = 0
        password = _md5("vpt")
    class rolland:
        prenom = u"Rolland"
        nom = u"Quillévéré"
        pseudo = u"Rolex"
        email = u"rolland.quillevere@gmail.com"
        is_admin = 0
        password = _md5("vpt")
    class franck_l:
        prenom = u"Franck"
        nom = u"Lasry"
        pseudo = u"Franck L"
        email = u"franck.lasry@gmail.com"
        is_admin = 0
        password = _md5("vpt")
    class fred:
        prenom = u"Frédéric"
        nom = u"Lambillotte"
        pseudo = u"Fred"
        email = u"frederic.lambillotte@orange.fr"
        is_admin = 0
        password = _md5("vpt")
        
        

class SeasonData(DataSet):
    class season_1:
        start_year = 2006
        end_year = 2007
    class season_2:
        start_year = 2007
        end_year = 2008
    class season_3:
        start_year = 2008
        end_year = 2009
    class season_4:
        start_year = 2009
        end_year = 2010
    class season_5:
        start_year = 2010
        end_year = 2011

class ResultData(DataSet):
    class result52_franck_p:
        user = UserData.franck
        statut = Result.STATUSES.P
        buyin = 10
        rank = 1
        profit = 40
    class result52_jo:
        user = UserData.jo
        statut = Result.STATUSES.P
        buyin = 10
        rank = 2
        profit = 20
    class result52_nico:
        user = UserData.nico
        statut = Result.STATUSES.P
        buyin = 10
        rank = 3
    class result52_rolland:
        user = UserData.rolland
        statut = Result.STATUSES.P
        buyin = 10
        rank = 4
    class result52_fx:
        user = UserData.fx
        statut = Result.STATUSES.P
        buyin = 10
        rank = 5
    class result52_franck_l:
        user = UserData.franck_l
        statut = Result.STATUSES.P
        buyin = 10
        rank = 6
    class result53_franck_p:
        user = UserData.franck
        statut = Result.STATUSES.P
        buyin = 10
        rank = 3
    class result53_jo:
        user = UserData.jo
        statut = Result.STATUSES.P
        buyin = 20
        rank = 6
    class result53_nico:
        user = UserData.nico
        statut = Result.STATUSES.P
        buyin = 10
        rank = 5
    class result53_fx:
        user = UserData.fx
        statut = Result.STATUSES.A
        buyin = None
        rank = None
    class result53_franck_l:
        user = UserData.franck_l
        statut = Result.STATUSES.P
        buyin = 20
        rank = 4
    class result53_rolland:
        user = UserData.rolland
        statut = Result.STATUSES.P
        buyin = 10
        rank = 2
        profit = 20
    class result53_fred:
        user = UserData.fred
        statut = Result.STATUSES.P
        buyin = 10
        rank = 1
        profit = 60

class TournamentData(DataSet):
    class tournament_51:
        date_tournoi = datetime.date(2010, 9, 24)
        buyin = 10        
        season = SeasonData.season_5
    class tournament_52:
        date_tournoi = datetime.date(2010, 11, 6)
        buyin = 10
        season = SeasonData.season_5
        results = [ResultData.result52_franck_p, ResultData.result52_franck_l, ResultData.result52_jo, ResultData.result52_rolland, ResultData.result52_fx, ResultData.result52_nico]
    class tournament_53:
        date_tournoi = datetime.date(2011, 3, 18)
        buyin = 10
        season = SeasonData.season_5
        results = [ResultData.result53_franck_p, ResultData.result53_franck_l, ResultData.result53_fred, ResultData.result53_jo, ResultData.result53_rolland, ResultData.result53_fx, ResultData.result53_nico]
    class tournament_54:
        date_tournoi = datetime.date(2011, 5, 27)
        buyin = 10        
        season = SeasonData.season_5
        
engine = init_sqlalchemy_session(config.DATABASE)

dbfixture = SQLAlchemyFixture(
    env=globals(),
    engine=engine,
    style=NamedDataStyle()
)

if __name__ == "__main__" :
    
    metadata.drop_all(engine)
    metadata.create_all(engine)
    dbfixture.data(UserData, TournamentData).setup()
    


