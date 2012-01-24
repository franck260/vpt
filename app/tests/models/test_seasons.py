# -*- coding: utf-8 -*-

from app.models import Season, User
from app.tests import dbfixture, SeasonData, TournamentData
from app.tests.models import ModelTestCase
from web import config



class TestSeason(ModelTestCase):
    
    def setUp(self):
        super(TestSeason, self).setUp()
        self.data = dbfixture.data(TournamentData, SeasonData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_all(self):
        
        all_seasons = Season.all()
        print all_seasons
        self.assertEqual(len(all_seasons), 2)
        
        # Checks the order by clause
        self.assertEqual(all_seasons[0].id, 2)
        self.assertEqual(all_seasons[1].id, 1)
    
    def test_get(self):
        
        season_1 = config.orm.query(Season).filter(Season.start_year == 2009).one() #@UndefinedVariable
        season_2 = config.orm.query(Season).filter(Season.start_year == 2010).one() #@UndefinedVariable
        
        self.assertEquals(season_1.start_year, 2009)
        self.assertEquals(season_1.end_year, 2010)
        self.assertEquals(season_2.start_year, 2010)
        self.assertEquals(season_2.end_year, 2011)
        
        self.assertEqual(len(season_1.tournaments), 2)
        self.assertEqual(len(season_2.tournaments), 1)
        
    def test_results(self):

        season_1 = config.orm.query(Season).filter(Season.start_year == 2009).one() #@UndefinedVariable
        season_2 = config.orm.query(Season).filter(Season.start_year == 2010).one() #@UndefinedVariable
        
        franck_p = config.orm.query(User).filter(User.pseudonym == "Franck P").one() #@UndefinedVariable
        nico = config.orm.query(User).filter(User.first_name == "Nicolas").one() #@UndefinedVariable
        jo = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable

        results_season_1 = season_1.results
        
        self.assertEqual(len(results_season_1), 3)
        
        # TODO: Nico missing at #T2 & make sure attended is OK
        self.assertEqual(results_season_1[0].user, franck_p)
        self.assertEqual(results_season_1[0].attended, 2)
        self.assertEqual(results_season_1[0].buyin, 15)
        self.assertEqual(results_season_1[0].rank, 1)
        self.assertEqual(results_season_1[0].profit, 45)
        self.assertEqual(results_season_1[0].score, 67 + 50)
        self.assertEqual(results_season_1[0].net_profit, 45 - 15)
        
        self.assertEqual(results_season_1[1].user, jo)
        self.assertEqual(results_season_1[1].attended, 2)
        self.assertEqual(results_season_1[1].buyin, 25)
        self.assertEqual(results_season_1[1].rank, 2)
        self.assertEqual(results_season_1[1].profit, 5)
        self.assertEqual(results_season_1[1].score, 34 + 5)
        self.assertEqual(results_season_1[1].net_profit, None)
        
        self.assertEqual(results_season_1[2].user, nico)
        self.assertEqual(results_season_1[2].attended, 1)
        self.assertEqual(results_season_1[2].buyin, 10)
        self.assertEqual(results_season_1[2].rank, 3)
        self.assertEqual(results_season_1[2].profit, None)
        self.assertEqual(results_season_1[2].score, 5)
        self.assertEqual(results_season_1[2].net_profit, None)       

        results_season_2 = season_2.results
        self.assertEqual(results_season_2, [])
                
    
    
    