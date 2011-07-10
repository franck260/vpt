# -*- coding: utf-8 -*-

from app.models import TournamentComment, Season, Tournament
from app.tests import dbfixture, TournamentCommentData, TournamentData
from app.tests.models import ModelTestCase
from web import config
import datetime
        
class TestTournamentComment(ModelTestCase):
    
    def setUp(self):
        super(TestTournamentComment, self).setUp()
        self.data = dbfixture.data(TournamentData, TournamentCommentData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_all(self):
        
        all_comments = TournamentComment.all()
        print all_comments
        self.assertEqual(len(all_comments), 4)
    
    def test_get(self):
        
        comments_11 = config.orm.query(TournamentComment).join(TournamentComment.tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).all() #@UndefinedVariable
        comments_12 = config.orm.query(TournamentComment).join(TournamentComment.tournament).filter(Tournament.tournament_dt == datetime.date(2010, 1, 1)).all() #@UndefinedVariable
        comments_21 = config.orm.query(TournamentComment).join(TournamentComment.tournament).join(Tournament.season).filter(Season.id == 2).all() #@UndefinedVariable
        
        self.assertEqual(len(comments_11), 0)
        self.assertEqual(len(comments_12), 3)
        self.assertEqual(len(comments_21), 1)

    
