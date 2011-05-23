# -*- coding: utf-8 -*-

'''
Created on 12 mars 2011

@author: Franck
'''

from app.models.comments import Comment
from app.models.seasons import Season
from app.models.tournaments import Tournament
from app.tests import dbfixture, CommentData, TournamentData
from app.tests.models import ModelTestCase
from web import config
import datetime
        
class TestComment(ModelTestCase):
    
    def setUp(self):
        super(TestComment, self).setUp()
        self.data = dbfixture.data(TournamentData, CommentData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_all(self):
        
        all_comments = Comment.all()
        print all_comments
        self.assertEqual(len(all_comments), 4)
    
    def test_get(self):
        
        comments_11 = config.orm.query(Comment).join(Comment.tournament).filter(Tournament.date_tournoi == datetime.date(2009, 9, 1)).all() #@UndefinedVariable
        comments_12 = config.orm.query(Comment).join(Comment.tournament).filter(Tournament.date_tournoi == datetime.date(2010, 1, 1)).all() #@UndefinedVariable
        comments_21 = config.orm.query(Comment).join(Comment.tournament).join(Tournament.season).filter(Season.id == 2).all() #@UndefinedVariable
        
        self.assertEqual(len(comments_11), 0)
        self.assertEqual(len(comments_12), 3)
        self.assertEqual(len(comments_21), 1)

    
