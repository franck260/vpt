# -*- coding: utf-8 -*-

from app.models import User, Tournament, UserToken, PasswordToken, Poll
from app.notifications import build_email_notification, Events, NoSuchTemplate
from app.tests import dbfixture, TournamentData, UserTokenData, \
    PasswordTokenData, PollData
from app.tests.models import ModelTestCase
from app.utils.mm import NoSuchMethod
from web import config
import datetime

class TestNotifications(ModelTestCase):
    
    def setUp(self):
        super(TestNotifications, self).setUp()
        self.data = dbfixture.data(TournamentData, UserTokenData, PasswordTokenData, PollData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_build_email_notification_tournament_new(self):
        
        tournament_21 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 8, 1)).one() #@UndefinedVariable
        notification = build_email_notification(tournament_21, Events.NEW)
        zoe = config.orm.query(User).filter(User.first_name == "Zoe").one() 
        
        self.assertEqual(notification.subject, u"VPT : le prochain tournoi aura lieu le dimanche 01 août")
        self.assertListEqual(notification.recipients, [user.email for user in User.all() if user != zoe])

    def test_build_email_notification_poll_new(self):
        
        poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable
        notification = build_email_notification(poll_3, Events.NEW)
        zoe = config.orm.query(User).filter(User.first_name == "Zoe").one()
        
        self.assertEqual(notification.subject, u"Date du VPT de juillet 2020 : votez !")
        self.assertListEqual(notification.recipients, [user.email for user in User.all() if user != zoe])

    def test_build_email_notification_tournament_comment_new(self):
        
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

    def test_build_email_notification_poll_comment_new(self):
        
        try:
            poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable
            nico = config.orm.query(User).filter(User.first_name == "Nicolas").one()
            zoe = config.orm.query(User).filter(User.first_name == "Zoe").one()
            comment = poll_3.add_comment(nico, "Salut Franck !")
            config.orm.commit()
            notification = build_email_notification(comment, Events.NEW)
            
            self.assertEqual(notification.subject, u"VPT : un nouveau commentaire a été posté (sondage : date du VPT de juillet 2020)")
            self.assertListEqual(notification.recipients, [user.email for user in User.all() if user not in (nico, zoe)])

        finally:
            #TODO: should be done by the fixture
            config.orm.delete(poll_3.comments[0])
            config.orm.commit()

    def test_build_email_notification_poll_vote(self):
        
        poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable
        jo = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable
        franck_p = config.orm.query(User).filter(User.email == "franck.p@gmail.com").one() #@UndefinedVariable
        
        try:
            # Scenario 1 : first vote on a poll, non-empty list of choices
            poll_vote = poll_3.vote(jo, poll_3.choices)
            config.orm.commit()
            notification = build_email_notification(poll_vote, Events.NEW)

            self.assertEqual(notification.subject, u"VPT : le participant Jo a enregistré son vote (sondage : date du VPT de juillet 2020)")
            self.assertListEqual(notification.recipients, [franck_p.email])
            self.assertIn("[20/07/2020, 27/07/2020]", notification.body)

            # Scenario 2 : second vote on a poll, same user, empty list of choices
            poll_vote = poll_3.vote(jo, [])
            config.orm.commit()
            notification = build_email_notification(poll_vote, Events.MODIFIED)
            
            self.assertEqual(notification.subject, u"VPT : le participant Jo a modifié son vote (sondage : date du VPT de juillet 2020)")
            self.assertListEqual(notification.recipients, [franck_p.email])
            self.assertIn("[]", notification.body)
        
        finally:
            #TODO: should be done by the fixture
            config.orm.delete(poll_3.votes_by_user[jo])
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
