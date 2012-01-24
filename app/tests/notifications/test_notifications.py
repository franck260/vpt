# -*- coding: utf-8 -*-

from app.models import User, Tournament, UserToken, PasswordToken
from app.notifications import build_email_notification, Events, NoSuchTemplate
from app.tests import dbfixture, TournamentData, UserTokenData, \
    PasswordTokenData
from app.tests.models import ModelTestCase
from app.utils.mm import NoSuchMethod
from web import config
import datetime

class TestNotifications(ModelTestCase):
    
    def setUp(self):
        super(TestNotifications, self).setUp()
        self.data = dbfixture.data(TournamentData, UserTokenData, PasswordTokenData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_build_email_notification_tournament_new(self):
        
        tournament_21 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 8, 1)).one() #@UndefinedVariable
        notification = build_email_notification(tournament_21, Events.NEW)
        zoe = config.orm.query(User).filter(User.first_name == "Zoe").one() 
        
        self.assertEqual(notification.subject, u"VPT : le prochain tournoi aura lieu le dimanche 01 août")
        self.assertListEqual(notification.recipients, [user.email for user in User.all() if user != zoe])
    
    def test_build_email_notification_comment_new(self):
        
        try:
            tournament_21 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 8, 1)).one() #@UndefinedVariable
            nico = config.orm.query(User).filter(User.first_name == "Nicolas").one()
            zoe = config.orm.query(User).filter(User.first_name == "Zoe").one()
            comment = tournament_21.add_comment(nico, "Salut les amis !")
            config.orm.commit()
            notification = build_email_notification(comment, Events.NEW)
            
            self.assertEqual(notification.subject, u"VPT : un nouveau commentaire a été posté (tournoi du 01 août)")
            self.assertListEqual(notification.recipients, [user.email for user in User.all() if user not in (nico, zoe)])
        
        finally:
            #TODO: should be done by the fixture
            config.orm.delete(tournament_21.comments[1])
            config.orm.commit()

    def test_build_email_notification_user_token_new(self):
        
        user_token_active = config.orm.query(UserToken).filter(UserToken.email == "dorian.gray@gmail.com").one() #@UndefinedVariable
        notification = build_email_notification(user_token_active, Events.NEW)
        
        self.assertEqual(notification.subject, u"Bienvenue sur le portail du VPT !")
        self.assertListEqual(notification.recipients, [user_token_active.email] + [user.email for user in User.all() if user.admin])
        
    def test_build_email_notification_password_token_new(self):
        
        password_token_active = config.orm.query(PasswordToken).join(PasswordToken.user).filter(User.email == "jo@gmail.com").one() #@UndefinedVariable
        notification = build_email_notification(password_token_active, Events.NEW)
        
        self.assertEqual(notification.subject, u"VPT : demande de changement de mot de passe")
        self.assertListEqual(notification.recipients, [password_token_active.user.email] + [user.email for user in User.all() if user.admin])

    def test_build_email_notification_invalid_method(self):
        self.assertRaises(NoSuchMethod, build_email_notification, object(), Events.NEW)
        
    def test_build_email_notification_invalid_template(self):
        
        tournament_21 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 8, 1)).one() #@UndefinedVariable
        self.assertRaises(NoSuchTemplate, build_email_notification, tournament_21, u"UNDEFINED_EVENT")
