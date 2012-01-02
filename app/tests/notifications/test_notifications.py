# -*- coding: utf-8 -*-

from app.models import User, Tournament
from app.notifications import build_email_notification, Events, NoSuchTemplate
from app.tests import dbfixture, TournamentData
from app.tests.models import ModelTestCase
from app.utils.mm import NoSuchMethod
from web import config
import datetime

class TestNotifications(ModelTestCase):
    
    def setUp(self):
        super(TestNotifications, self).setUp()
        self.data = dbfixture.data(TournamentData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_build_email_notification_tournament_new(self):
        
        tournament_21 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 8, 1)).one() #@UndefinedVariable
        notification = build_email_notification(tournament_21, Events.NEW)
        
        self.assertEqual(notification.subject, u"VPT : le prochain tournoi aura lieu le dimanche 01 août")
        self.assertListEqual(notification.recipients, [user.email for user in User.all()])
    
    def test_build_email_notification_comment_new(self):
        
        try:
            tournament_21 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 8, 1)).one() #@UndefinedVariable
            nico = config.orm.query(User).filter(User.first_name == "Nicolas").one() #@UndefinedVariable
            comment = tournament_21.add_comment(nico, "Salut les amis !")
            config.orm.commit()
            notification = build_email_notification(comment, Events.NEW)
            
            self.assertEqual(notification.subject, u"VPT : un nouveau commentaire a été posté (tournoi du 01 août)")
            self.assertListEqual(notification.recipients, [user.email for user in User.all() if user != nico])
        
        finally:
            #TODO: should be done by the fixture
            config.orm.delete(tournament_21.comments[1])
            config.orm.commit()
    
    def test_build_email_notification_invalid_method(self):
        self.assertRaises(NoSuchMethod, build_email_notification, object(), Events.NEW)
        
    def test_build_email_notification_invalid_template(self):
        
        tournament_21 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 8, 1)).one() #@UndefinedVariable
        self.assertRaises(NoSuchTemplate, build_email_notification, tournament_21, u"UNDEFINED_EVENT")
