# -*- coding: utf-8 -*-

from app.models import Season, Tournament, User, Poll, PollVote, PollUserChoice
from app.tests import dbfixture, TournamentData, PollData, PollVoteData
from app.tests.models import ModelTestCase
from web import config
import datetime

class TestPoll(ModelTestCase):
    
    def setUp(self):
        super(TestPoll, self).setUp()
        self.data = dbfixture.data(PollData, PollVoteData, TournamentData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_all(self):
        
        all_polls = Poll.all()
        self.assertEqual(len(all_polls), 3)
        
        # Checks the order by clause
        self.assertEqual(all_polls[0].start_dt, datetime.date(2011, 5, 28))
        self.assertEqual(all_polls[1].start_dt, datetime.date(2012, 4, 5))
        self.assertEqual(all_polls[2].start_dt, datetime.date(2020, 7, 1))

    def test_expired(self):

        poll_1 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2012, 4, 5)).one() #@UndefinedVariable
        poll_2 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2011, 5, 28)).one() #@UndefinedVariable
        poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable
        
        self.assertFalse(poll_1.expired)
        self.assertTrue(poll_2.expired)
        self.assertFalse(poll_3.expired)

    def test_has_votes(self):

        poll_1 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2012, 4, 5)).one() #@UndefinedVariable
        poll_2 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2011, 5, 28)).one() #@UndefinedVariable
        poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable
        
        self.assertTrue(poll_1.has_votes)
        self.assertTrue(poll_2.has_votes)
        self.assertFalse(poll_3.has_votes)
        
    def test_comment(self):
        
        franck_l = config.orm.query(User).filter(User.pseudonym == "Franck L").one() #@UndefinedVariable
        nico = config.orm.query(User).filter(User.first_name == "Nicolas").one() #@UndefinedVariable
        jo = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable
        
        poll_1 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2012, 4, 5)).one() #@UndefinedVariable
        poll_2 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2011, 5, 28)).one() #@UndefinedVariable
        poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable

        tournament_11 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        tournament_12 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 1, 1)).one() #@UndefinedVariable
        tournament_21 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable

        self.assertEqual(len(poll_1.comments), 2)
        self.assertEqual(len(poll_2.comments), 1)
        self.assertEqual(len(poll_3.comments), 0)
        
        self.assertEqual(len(tournament_11.comments), 0)
        self.assertEqual(len(tournament_12.comments), 3)
        self.assertEqual(len(tournament_21.comments), 1)

        poll_3.add_comment(franck_l, "Salut Nicolas !")
        poll_3.add_comment(nico, "Salut Franck !")
        poll_3.add_comment(jo, "Salut tout le monde !")
        config.orm.commit()
        
        self.assertEqual(len(poll_1.comments), 2)
        self.assertEqual(len(poll_2.comments), 1)
        self.assertEqual(len(poll_3.comments), 3)
        
        # Checks nothing happened to tournaments' comments
        self.assertEqual(len(tournament_11.comments), 0)
        self.assertEqual(len(tournament_12.comments), 3)
        self.assertEqual(len(tournament_21.comments), 1)
        
    def test_vote(self):
        
        jo = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable
        rolland = config.orm.query(User).filter(User.first_name == "Rolland").one() #@UndefinedVariable
        
        poll_1 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2012, 4, 5)).one() #@UndefinedVariable
        poll_2 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2011, 5, 28)).one() #@UndefinedVariable
        poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable
        
        self.assertEqual(config.orm.query(PollVote).count(), 5)
        self.assertEqual(config.orm.query(PollUserChoice).count(), 7)
        self.assertEqual(len(poll_1.choices_by_user), 3)
        self.assertEqual(len(poll_2.choices_by_user), 2)
        self.assertEqual(len(poll_3.choices_by_user), 0)
        
        try:
            # Scenario 1 : first vote on a poll, non-empty list of choices
            poll_3.vote(jo, poll_3.choices)
            config.orm.commit()
            self.assertEqual(len(poll_3.choices_by_user[jo]), 2)
            self.assertEqual(poll_3.votes_by_user[jo].first_vote_dt, poll_3.votes_by_user[jo].last_vote_dt)
            self.assertEqual(config.orm.query(PollVote).count(), 6)
            self.assertEqual(config.orm.query(PollUserChoice).count(), 9)
            self.assertEqual(len(poll_1.choices_by_user), 3)
            self.assertEqual(len(poll_2.choices_by_user), 2)
            self.assertEqual(len(poll_3.choices_by_user), 1)

            # Scenario 2 : second vote on a poll, same user, non-empty list of choices
            poll_3.vote(jo, [poll_3.choices[0]])
            config.orm.commit()
            self.assertEqual(len(poll_3.choices_by_user[jo]), 1)
            self.assertGreater(poll_3.votes_by_user[jo].last_vote_dt, poll_3.votes_by_user[jo].first_vote_dt)
            self.assertEqual(config.orm.query(PollVote).count(), 6)
            self.assertEqual(config.orm.query(PollUserChoice).count(), 8)
            self.assertEqual(len(poll_1.choices_by_user), 3)
            self.assertEqual(len(poll_2.choices_by_user), 2)
            self.assertEqual(len(poll_3.choices_by_user), 1)
            
            # Scenario 3 : third vote on a poll, same user, empty list of choices
            poll_3.vote(jo, [])
            config.orm.commit()
            self.assertEqual(len(poll_3.choices_by_user[jo]), 0)
            self.assertGreater(poll_3.votes_by_user[jo].last_vote_dt, poll_3.votes_by_user[jo].first_vote_dt)
            self.assertEqual(config.orm.query(PollVote).count(), 6)
            self.assertEqual(config.orm.query(PollUserChoice).count(), 7)
            self.assertEqual(len(poll_1.choices_by_user), 3)
            self.assertEqual(len(poll_2.choices_by_user), 2)
            self.assertEqual(len(poll_3.choices_by_user), 1)

            # Scenario 4 : fourth vote on a poll, different user, non-empty list of choices
            poll_3.vote(rolland, [poll_3.choices[1]])
            config.orm.commit()
            self.assertEqual(len(poll_3.choices_by_user[jo]), 0)
            self.assertEqual(len(poll_3.choices_by_user[rolland]), 1)
            self.assertGreater(poll_3.votes_by_user[jo].last_vote_dt, poll_3.votes_by_user[jo].first_vote_dt)
            self.assertEqual(poll_3.votes_by_user[rolland].first_vote_dt, poll_3.votes_by_user[rolland].last_vote_dt)
            self.assertEqual(config.orm.query(PollVote).count(), 7)
            self.assertEqual(config.orm.query(PollUserChoice).count(), 8)
            self.assertEqual(len(poll_1.choices_by_user), 3)
            self.assertEqual(len(poll_2.choices_by_user), 2)
            self.assertEqual(len(poll_3.choices_by_user), 2)
            
            # Scenario 5 : fifth vote on a poll, different user, same non-empty list of choices
            poll_3.vote(rolland, [poll_3.choices[1]])
            config.orm.commit()
            self.assertEqual(len(poll_3.choices_by_user[jo]), 0)
            self.assertEqual(len(poll_3.choices_by_user[rolland]), 1)
            self.assertGreater(poll_3.votes_by_user[jo].last_vote_dt, poll_3.votes_by_user[jo].first_vote_dt)
            self.assertGreater(poll_3.votes_by_user[rolland].last_vote_dt, poll_3.votes_by_user[rolland].first_vote_dt)
            self.assertEqual(config.orm.query(PollVote).count(), 7)
            self.assertEqual(config.orm.query(PollUserChoice).count(), 8)
            self.assertEqual(len(poll_1.choices_by_user), 3)
            self.assertEqual(len(poll_2.choices_by_user), 2)
            self.assertEqual(len(poll_3.choices_by_user), 2)

            # Scenario 6 : sixth vote on a poll, different user, empty list of choices
            poll_3.vote(rolland, [])
            config.orm.commit()
            self.assertEqual(len(poll_3.choices_by_user[jo]), 0)
            self.assertEqual(len(poll_3.choices_by_user[rolland]), 0)
            self.assertGreater(poll_3.votes_by_user[jo].last_vote_dt, poll_3.votes_by_user[jo].first_vote_dt)
            self.assertGreater(poll_3.votes_by_user[rolland].last_vote_dt, poll_3.votes_by_user[rolland].first_vote_dt)
            self.assertEqual(config.orm.query(PollVote).count(), 7)
            self.assertEqual(config.orm.query(PollUserChoice).count(), 7)
            self.assertEqual(len(poll_1.choices_by_user), 3)
            self.assertEqual(len(poll_2.choices_by_user), 2)
            self.assertEqual(len(poll_3.choices_by_user), 2)
            
        
        finally:
            #TODO: should be done by the fixture
            config.orm.delete(poll_3.votes_by_user[jo])
            config.orm.delete(poll_3.votes_by_user[rolland])
            config.orm.commit()
        
    def test_vote_expired(self):
        
        jo = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable
        rolland = config.orm.query(User).filter(User.first_name == "Rolland").one() #@UndefinedVariable
        
        poll_1 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2012, 4, 5)).one() #@UndefinedVariable
        poll_2 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2011, 5, 28)).one() #@UndefinedVariable
        poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable
        
        self.assertEqual(config.orm.query(PollVote).count(), 5)
        self.assertEqual(config.orm.query(PollUserChoice).count(), 7)
        self.assertEqual(len(poll_1.choices_by_user), 3)
        self.assertEqual(len(poll_2.choices_by_user), 2)
        self.assertEqual(len(poll_3.choices_by_user), 0)
        
        self.assertRaises(ValueError, lambda: poll_2.vote(jo, poll_2.choices))
        self.assertRaises(ValueError, lambda: poll_2.vote(rolland, poll_2.choices))
        config.orm.commit()
        
        self.assertEqual(config.orm.query(PollVote).count(), 5)
        self.assertEqual(config.orm.query(PollUserChoice).count(), 7)
        self.assertEqual(len(poll_1.choices_by_user), 3)
        self.assertEqual(len(poll_2.choices_by_user), 2)
        self.assertEqual(len(poll_3.choices_by_user), 0)
        
    def test_vote_invalid_choices(self):
        
        jo = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable
        rolland = config.orm.query(User).filter(User.first_name == "Rolland").one() #@UndefinedVariable
        
        poll_1 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2012, 4, 5)).one() #@UndefinedVariable
        poll_2 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2011, 5, 28)).one() #@UndefinedVariable
        poll_3 = config.orm.query(Poll).filter(Poll.start_dt == datetime.date(2020, 7, 1)).one() #@UndefinedVariable
        
        self.assertEqual(config.orm.query(PollVote).count(), 5)
        self.assertEqual(config.orm.query(PollUserChoice).count(), 7)
        self.assertEqual(len(poll_1.choices_by_user), 3)
        self.assertEqual(len(poll_2.choices_by_user), 2)
        self.assertEqual(len(poll_3.choices_by_user), 0)

        self.assertRaises(ValueError, lambda: poll_1.vote(jo, poll_3.choices))
        self.assertEqual(poll_1.choices[2].choice_dt, poll_2.choices[0].choice_dt)
        self.assertRaises(ValueError, lambda: poll_1.vote(rolland, [poll_1.choices[0], poll_1.choices[1], poll_2.choices[0]]))
        config.orm.commit()

        self.assertEqual(config.orm.query(PollVote).count(), 5)
        self.assertEqual(config.orm.query(PollUserChoice).count(), 7)
        self.assertEqual(len(poll_1.choices_by_user), 3)
        self.assertEqual(len(poll_2.choices_by_user), 2)
        self.assertEqual(len(poll_3.choices_by_user), 0)
