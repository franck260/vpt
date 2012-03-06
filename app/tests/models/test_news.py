# -*- coding: utf-8 -*-

from app.models import News
from app.tests import dbfixture, NewsData
from app.tests.models import ModelTestCase
import datetime

class TestNews(ModelTestCase):
    
    def setUp(self):
        super(TestNews, self).setUp()
        self.data = dbfixture.data(NewsData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_all(self):
        
        all_news = News.all()
        self.assertEqual(len(all_news), 4)
        
        # Checks the order by clause
        self.assertEqual(all_news[0].news_dt, datetime.date(2011, 8, 15))
        self.assertEqual(all_news[1].news_dt, datetime.date(2011, 7, 13))
        self.assertEqual(all_news[2].news_dt, datetime.date(2011, 6, 10))
        self.assertEqual(all_news[3].news_dt, datetime.date(2011, 5, 27))
    
    
    