# -*- coding: utf-8 -*-

from app.models import Result, Season, Tournament, User
from app.tests import dbfixture, TournamentData, UserData
from app.tests.models import ModelTestCase
from sqlalchemy.ext.orderinglist import OrderingList
from web import config
import datetime

#TODO: test_position should commit and remove the tournament (cascade bug)

class TestTournament(ModelTestCase):
    
    def setUp(self):
        super(TestTournament, self).setUp()
        self.data = dbfixture.data(TournamentData, UserData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_all(self):
        
        all_tournaments = Tournament.all()
        self.assertEqual(len(all_tournaments), 3)
    
    def test_get(self):

        tournaments_season_1 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 1).all() #@UndefinedVariable
        tournament_season_2 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable
        tournament_21 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 8, 1)).one() #@UndefinedVariable
        
        self.assertEqual(len(tournaments_season_1), 2)
        self.assertEquals(tournament_season_2.season.id, 2)
        self.assertTrue(tournament_season_2 is tournament_21)
    
    def test_get_tournament(self):
        
        # These tests work because a TournamentData has a similar structure to a Tournament
        # When Tournament.__eq__ is called, it compares the fields without caring of the parameters' actual types
            
        self.assertEquals(Tournament.get_tournament(1, 1), TournamentData.tournament_11)
        self.assertEquals(Tournament.get_tournament(1, 2), TournamentData.tournament_12)
        self.assertEquals(Tournament.get_tournament(1, 3), None)
        self.assertEquals(Tournament.get_tournament(1, 4), None)
        
        self.assertEquals(Tournament.get_tournament(2, 1), TournamentData.tournament_21)
        self.assertEquals(Tournament.get_tournament(2, 2), None)
        self.assertEquals(Tournament.get_tournament(2, 3), None)
        
        self.assertEquals(Tournament.get_tournament(42, 1), None)
        self.assertEquals(Tournament.get_tournament(42, 9), None)

    def test_sum_in_play(self):
        
        tournament_11 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        tournament_12 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 1, 1)).one() #@UndefinedVariable
        tournament_21 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable
        
        self.assertEquals(tournament_11.sum_in_play, 40)
        self.assertEquals(tournament_12.sum_in_play, 10)
        self.assertEquals(tournament_21.sum_in_play, 20)
    
    def test_results_by_status(self):
        
        def _check_results(results, expected_length, expected_status):
            self.assertEquals(len(results), expected_length)
            for result in results:
                self.assertEquals(result.status, expected_status)
        
        tournament_11 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        tournament_12 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 1, 1)).one() #@UndefinedVariable
        tournament_21 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable 
        
        _check_results(tournament_11.results_by_status(Result.STATUSES.P), 3, Result.STATUSES.P)  
        _check_results(tournament_11.results_by_status(Result.STATUSES.M), 1, Result.STATUSES.M)
        _check_results(tournament_11.results_by_status(Result.STATUSES.A), 1, Result.STATUSES.A)
        
        _check_results(tournament_12.results_by_status(Result.STATUSES.P), 2, Result.STATUSES.P)  
        _check_results(tournament_12.results_by_status(Result.STATUSES.M), 0, Result.STATUSES.M)
        _check_results(tournament_12.results_by_status(Result.STATUSES.A), 1, Result.STATUSES.A)
        
        _check_results(tournament_21.results_by_status(Result.STATUSES.P), 2, Result.STATUSES.P)  
        _check_results(tournament_21.results_by_status(Result.STATUSES.M), 0, Result.STATUSES.M)
        _check_results(tournament_21.results_by_status(Result.STATUSES.A), 0, Result.STATUSES.A)
    
    def test_comment(self):
        
        franck_l = config.orm.query(User).filter(User.pseudonym == "Franck L").one() #@UndefinedVariable
        nico = config.orm.query(User).filter(User.first_name == "Nicolas").one() #@UndefinedVariable
        
        tournament_11 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        tournament_12 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 1, 1)).one() #@UndefinedVariable
        tournament_21 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable

        self.assertEqual(len(tournament_11.comments), 0)
        self.assertEqual(len(tournament_12.comments), 3)
        self.assertEqual(len(tournament_21.comments), 1)

        tournament_11.add_comment(franck_l, "Salut Nicolas !")
        tournament_11.add_comment(nico, "Salut Franck !")
        config.orm.commit()
        
        self.assertEqual(len(tournament_11.comments), 2)
        self.assertEqual(len(tournament_12.comments), 3)
        self.assertEqual(len(tournament_21.comments), 1)

    def test_nb_attending_players(self):
        
        tournament_11 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        tournament_12 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 1, 1)).one() #@UndefinedVariable
        tournament_21 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable
        
        self.assertEqual(tournament_11.nb_attending_players, 3)
        self.assertEqual(tournament_12.nb_attending_players, 2)
        self.assertEqual(tournament_21.nb_attending_players, 2)

        
    def test_subscribe(self):
        
        franck_l = config.orm.query(User).filter(User.pseudonym == "Franck L").one() #@UndefinedVariable
        nico = config.orm.query(User).filter(User.first_name == "Nicolas").one() #@UndefinedVariable
        jo = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable
        fx = config.orm.query(User).filter(User.pseudonym == "FX").one() #@UndefinedVariable
        tournament_21 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable
        
        self.assertEqual(len(tournament_21.results), 2)

        # Checks if the results are properly ordered
        self.assertListEqual(
            [result.user for result in tournament_21.results],
            [jo, fx]
        )
        
        tournament_21.subscribe(franck_l, Result.STATUSES.P)
        tournament_21.subscribe(nico, Result.STATUSES.P)
        tournament_21.subscribe(jo, Result.STATUSES.M)

        self.assertEqual(len(tournament_21.results), 4)

        # Checks if the results are properly ordered
        self.assertListEqual(
            [result.user for result in tournament_21.results],
            [jo, fx, franck_l, nico]  
        )
                
        self.assertEqual(tournament_21.results_by_user.get(franck_l).status, Result.STATUSES.P)
        self.assertEqual(tournament_21.results_by_user.get(nico).status, Result.STATUSES.P)
        self.assertEqual(tournament_21.results_by_user.get(jo).status, Result.STATUSES.M)
        self.assertEqual(tournament_21.results_by_user.get(fx).status, Result.STATUSES.P)
        
        tournament_21.subscribe(nico, Result.STATUSES.M)
        tournament_21.subscribe(franck_l, Result.STATUSES.A)
        tournament_21.subscribe(jo, Result.STATUSES.M)
        
        self.assertEqual(len(tournament_21.results), 4)
        
        # Checks if the results are properly ordered
        self.assertListEqual(
            [result.user for result in tournament_21.results],
            [franck_l, nico, jo, fx]  
        )        
        
        self.assertEqual(tournament_21.results_by_user.get(franck_l).status, Result.STATUSES.A)
        self.assertEqual(tournament_21.results_by_user.get(nico).status, Result.STATUSES.M)
        self.assertEqual(tournament_21.results_by_user.get(jo).status, Result.STATUSES.M)
        self.assertEqual(tournament_21.results_by_user.get(fx).status, Result.STATUSES.P)
    
    def test_future(self):

        tournament_11 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        tournament_12 = config.orm.query(Tournament).filter(Tournament.tournament_dt == datetime.date(2010, 1, 1)).one() #@UndefinedVariable
        tournament_21 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable
        
        self.assertFalse(tournament_11.future)
        self.assertFalse(tournament_12.future)
        self.assertFalse(tournament_21.future)
        
    def test_position(self):
        
        season_1 = config.orm.query(Season).filter(Season.id == 1).one() #@UndefinedVariable
        season_2 = config.orm.query(Season).filter(Season.id == 2).one() #@UndefinedVariable
        
        self.assertIsInstance(season_1.tournaments, OrderingList)
        self.assertIsInstance(season_2.tournaments, OrderingList)
        
        self.assertEqual(len(season_1.tournaments), 2)
        self.assertEqual(len(season_2.tournaments), 1)
    
        self.assertEqual(season_1.tournaments[0].position, 1)
        self.assertEqual(season_1.tournaments[1].position, 2)
        self.assertEqual(season_2.tournaments[0].position, 1)
    
        self.assertEqual(season_1.tournaments[0].tournament_dt, datetime.date(2009, 9, 1))
        self.assertEqual(season_1.tournaments[1].tournament_dt, datetime.date(2010, 1, 1))
        self.assertEqual(season_2.tournaments[0].tournament_dt, datetime.date(2010, 8, 1))
        
        tournament_13 = Tournament()
        tournament_13.tournament_dt = datetime.date(2010, 2, 1)
        tournament_13.buyin = 10
        tournament_13.season_id = 1
        
        season_1.tournaments.append(tournament_13)
        season_1.reorder_tournaments()
        
        self.assertEqual(len(season_1.tournaments), 3)
        self.assertEqual(len(season_2.tournaments), 1)
        
        self.assertEqual(season_1.tournaments[0].position, 1)
        self.assertEqual(season_1.tournaments[1].position, 2)
        self.assertEqual(season_1.tournaments[2].position, 3)
        self.assertEqual(season_2.tournaments[0].position, 1)
        
        self.assertEqual(season_1.tournaments[0].tournament_dt, datetime.date(2009, 9, 1))
        self.assertEqual(season_1.tournaments[1].tournament_dt, datetime.date(2010, 1, 1))
        self.assertEqual(season_1.tournaments[2].tournament_dt, datetime.date(2010, 2, 1))
        self.assertEqual(season_2.tournaments[0].tournament_dt, datetime.date(2010, 8, 1))

        tournament_10 = Tournament()
        tournament_10.tournament_dt = datetime.date(2009, 8, 31)
        tournament_10.buyin = 10
        tournament_10.season_id = 1
        
        season_1.tournaments.append(tournament_10)
        season_1.reorder_tournaments()
        
        self.assertEqual(len(season_1.tournaments), 4)
        self.assertEqual(len(season_2.tournaments), 1)
        
        self.assertEqual(season_1.tournaments[0].position, 1)
        self.assertEqual(season_1.tournaments[1].position, 2)
        self.assertEqual(season_1.tournaments[2].position, 3)
        self.assertEqual(season_1.tournaments[3].position, 4)
        self.assertEqual(season_2.tournaments[0].position, 1)
        
        self.assertEqual(season_1.tournaments[0].tournament_dt, datetime.date(2009, 8, 31))
        self.assertEqual(season_1.tournaments[1].tournament_dt, datetime.date(2009, 9, 1))
        self.assertEqual(season_1.tournaments[2].tournament_dt, datetime.date(2010, 1, 1))
        self.assertEqual(season_1.tournaments[3].tournament_dt, datetime.date(2010, 2, 1))
        self.assertEqual(season_2.tournaments[0].tournament_dt, datetime.date(2010, 8, 1))



        

