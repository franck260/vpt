# -*- coding: utf-8 -*-

'''
Created on 12 mars 2011

@author: Franck
'''


from app.models import orm
from app.models.results import Result
from app.models.seasons import Season
from app.models.tournaments import Tournament
from app.tests import dbfixture, ResultData, TournamentData
from app.tests.models import ModelTestCase

        
class TestResult(ModelTestCase):
    
    def setUp(self):
        super(TestResult, self).setUp()
        self.data = dbfixture.data(TournamentData, ResultData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_all(self):
        
        all_results = Result.all()
        print all_results
        self.assertEqual(len(all_results), 10)
    
    def test_get(self):
        
        results_season_1 = orm.query(Result).join(Result.tournament).join(Tournament.season).filter(Season.id == 1).all() #@UndefinedVariable
        results_season_2 = orm.query(Result).join(Result.tournament).join(Tournament.season).filter(Season.id == 2).all() #@UndefinedVariable
        
        self.assertEqual(len(results_season_1), 8)
        self.assertEqual(len(results_season_2), 2)
        
    def test_score(self):
        
        result_franck_l = orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 1).one() #@UndefinedVariable
        result_franck_p = orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 2).one() #@UndefinedVariable
        result_fx = orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 3).one() #@UndefinedVariable
        result_jo = orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 4).one() #@UndefinedVariable
        result_nico = orm.query(Result).filter(Result.tournament_id == 1).filter(Result.user_id == 5).one() #@UndefinedVariable
        
        self.assertIsNone(result_franck_l.score)
        self.assertIsNone(result_fx.score)
        self.assertEqual(result_franck_p.score, 67)
        self.assertEqual(result_jo.score, 34)
        self.assertEqual(result_nico.score, 5)
                        
        
        

