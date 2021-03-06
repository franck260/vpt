# -*- coding: utf-8 -*-

from app.models import Result, Season, Tournament
from app.tests import dbfixture, ResultData, TournamentData
from app.tests.models import ModelTestCase
from web import config


        
class TestResult(ModelTestCase):
    
    def setUp(self):
        super(TestResult, self).setUp()
        self.data = dbfixture.data(TournamentData, ResultData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_all(self):
        
        all_results = Result.all()
        self.assertEqual(len(all_results), 10)
    
    def test_get(self):
        
        results_season_1 = config.orm.query(Result).join(Result.tournament).join(Tournament.season).filter(Season.id == 1).all() #@UndefinedVariable
        results_season_2 = config.orm.query(Result).join(Result.tournament).join(Tournament.season).filter(Season.id == 2).all() #@UndefinedVariable
        
        self.assertEqual(len(results_season_1), 8)
        self.assertEqual(len(results_season_2), 2)
        
    def test_score(self):
        
        result_franck_l = config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 1).one() #@UndefinedVariable
        result_franck_p = config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 2).one() #@UndefinedVariable
        result_fx = config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 3).one() #@UndefinedVariable
        result_jo = config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 4).one() #@UndefinedVariable
        result_nico = config.orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 5).one() #@UndefinedVariable
        
        self.assertIsNone(result_franck_l.score)
        self.assertIsNone(result_fx.score)
        self.assertEqual(result_franck_p.score, 67)
        self.assertEqual(result_jo.score, 34)
        self.assertEqual(result_nico.score, 5)
                        
        
        

