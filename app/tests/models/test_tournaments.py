# -*- coding: utf-8 -*-

'''
Created on 12 mars 2011

@author: Franck
'''

from app.models.results import Result
from app.models.seasons import Season
from app.models.tournaments import Tournament
from app.models.users import User
from app.tests import dbfixture, TournamentData, UserData
from app.tests.models import ModelTestCase
from sqlalchemy.ext.orderinglist import OrderingList
from web import config
import datetime



        
#TODO: tester inscription et vérifier le basculement des paramètres
#TODO: sortir l'enum
#TODO: renommer anglais / français
#TODO: tester next_tournament
#TODO: test_position doit commit, supprimer le tournoi (bug sur la cascade)

class TestTournament(ModelTestCase):
    
    def setUp(self):
        super(TestTournament, self).setUp()
        self.data = dbfixture.data(TournamentData, UserData)
        self.data.setup()
    
    def tearDown(self):
        self.data.teardown()
        
    def test_all(self):
        
        all_tournaments = Tournament.all()
        print all_tournaments
        self.assertEqual(len(all_tournaments), 3)
    
    def test_get(self):

        tournaments_season_1 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 1).all() #@UndefinedVariable
        tournament_season_2 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable
        tournament_21 = config.orm.query(Tournament).filter(Tournament.date_tournoi == datetime.date(2010, 9, 1)).one() #@UndefinedVariable
        
        self.assertEqual(len(tournaments_season_1), 2)
        self.assertEquals(tournament_season_2.season.id, 2)
        self.assertTrue(tournament_season_2 is tournament_21)
    
    def test_get_tournaments(self):
        
        self.assertEquals(Tournament.get_tournaments(1, 1), (1, None, 2))
        self.assertEquals(Tournament.get_tournaments(1, 2), (2, 1, None))
        self.assertEquals(Tournament.get_tournaments(1, 3), (None, 2, None))
        self.assertEquals(Tournament.get_tournaments(1, 4), (None, None, None))
        
        self.assertEquals(Tournament.get_tournaments(2, 1), (3, None, None))
        self.assertEquals(Tournament.get_tournaments(2, 2), (None, 3, None))
        self.assertEquals(Tournament.get_tournaments(2, 3), (None, None, None))
        
        self.assertEquals(Tournament.get_tournaments(42, 1), (None, None, None))
        self.assertEquals(Tournament.get_tournaments(42, 9), (None, None, None))

    
    def test_comment(self):
        
        franck_l = config.orm.query(User).filter(User.nom == "Lasry").one() #@UndefinedVariable
        nico = config.orm.query(User).filter(User.prenom == "Nicolas").one() #@UndefinedVariable
        
        tournament_11 = config.orm.query(Tournament).filter(Tournament.date_tournoi == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        tournament_12 = config.orm.query(Tournament).filter(Tournament.date_tournoi == datetime.date(2010, 1, 1)).one() #@UndefinedVariable
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
        
    def test_nb_presents(self):
        
        tournament_11 = config.orm.query(Tournament).filter(Tournament.date_tournoi == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        tournament_12 = config.orm.query(Tournament).filter(Tournament.date_tournoi == datetime.date(2010, 1, 1)).one() #@UndefinedVariable
        tournament_21 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable
        
        self.assertEqual(tournament_11.nb_presents, 3)
        self.assertEqual(tournament_12.nb_presents, 2)
        self.assertEqual(tournament_21.nb_presents, 2)
    
    def test_nb_absents(self):
        
        tournament_11 = config.orm.query(Tournament).filter(Tournament.date_tournoi == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        tournament_12 = config.orm.query(Tournament).filter(Tournament.date_tournoi == datetime.date(2010, 1, 1)).one() #@UndefinedVariable
        tournament_21 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable
         
        self.assertEqual(tournament_11.nb_absents, 1)
        self.assertEqual(tournament_12.nb_absents, 1)
        self.assertEqual(tournament_21.nb_absents, 0)
        
    def test_subscribe(self):
        
        franck_l = config.orm.query(User).filter(User.nom == "Lasry").one() #@UndefinedVariable
        nico = config.orm.query(User).filter(User.prenom == "Nicolas").one() #@UndefinedVariable
        jo = config.orm.query(User).filter(User.prenom == "Jonathan").one() #@UndefinedVariable
        fx = config.orm.query(User).filter(User.pseudo == "FX").one() #@UndefinedVariable
        tournament_21 = config.orm.query(Tournament).join(Tournament.season).filter(Season.id == 2).one() #@UndefinedVariable
        
        self.assertEqual(len(tournament_21.results), 2)
        
        tournament_21.subscribe(franck_l, Result.STATUSES.P)
        tournament_21.subscribe(nico, Result.STATUSES.P)
        tournament_21.subscribe(jo, Result.STATUSES.M) 
           
        self.assertEqual(len(tournament_21.results), 4)
        self.assertEqual(tournament_21.ordered_results.get(franck_l).statut, Result.STATUSES.P)
        self.assertEqual(tournament_21.ordered_results.get(nico).statut, Result.STATUSES.P)
        self.assertEqual(tournament_21.ordered_results.get(jo).statut, Result.STATUSES.M)
        self.assertEqual(tournament_21.ordered_results.get(fx).statut, Result.STATUSES.P)
        
        tournament_21.subscribe(franck_l, Result.STATUSES.A)
        tournament_21.subscribe(nico, Result.STATUSES.M)
        tournament_21.subscribe(jo, Result.STATUSES.M)
        
        self.assertEqual(len(tournament_21.results), 4)
        self.assertEqual(tournament_21.ordered_results.get(franck_l).statut, Result.STATUSES.A)
        self.assertEqual(tournament_21.ordered_results.get(nico).statut, Result.STATUSES.M)
        self.assertEqual(tournament_21.ordered_results.get(jo).statut, Result.STATUSES.M)
        self.assertEqual(tournament_21.ordered_results.get(fx).statut, Result.STATUSES.P)
    
    def test_future(self):

        tournament_11 = config.orm.query(Tournament).filter(Tournament.date_tournoi == datetime.date(2009, 9, 1)).one() #@UndefinedVariable
        tournament_12 = config.orm.query(Tournament).filter(Tournament.date_tournoi == datetime.date(2010, 1, 1)).one() #@UndefinedVariable
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
    
        self.assertEqual(season_1.tournaments[0].date_tournoi, datetime.date(2009, 9, 1))
        self.assertEqual(season_1.tournaments[1].date_tournoi, datetime.date(2010, 1, 1))
        self.assertEqual(season_2.tournaments[0].date_tournoi, datetime.date(2010, 9, 1))
        
        tournament_13 = Tournament()
        tournament_13.date_tournoi = datetime.date(2010, 2, 1)
        tournament_13.buyin = 10
        tournament_13.season_id = 1
        
        season_1.tournaments.append(tournament_13)
        season_1.tournaments.sort(key = lambda tournament: tournament.date_tournoi)
        season_1.tournaments.reorder()
        
        self.assertEqual(len(season_1.tournaments), 3)
        self.assertEqual(len(season_2.tournaments), 1)
        
        self.assertEqual(season_1.tournaments[0].position, 1)
        self.assertEqual(season_1.tournaments[1].position, 2)
        self.assertEqual(season_1.tournaments[2].position, 3)
        self.assertEqual(season_2.tournaments[0].position, 1)
        
        self.assertEqual(season_1.tournaments[0].date_tournoi, datetime.date(2009, 9, 1))
        self.assertEqual(season_1.tournaments[1].date_tournoi, datetime.date(2010, 1, 1))
        self.assertEqual(season_1.tournaments[2].date_tournoi, datetime.date(2010, 2, 1))
        self.assertEqual(season_2.tournaments[0].date_tournoi, datetime.date(2010, 9, 1))

        tournament_10 = Tournament()
        tournament_10.date_tournoi = datetime.date(2009, 8, 31)
        tournament_10.buyin = 10
        tournament_10.season_id = 1
        
        season_1.tournaments.append(tournament_10)
        season_1.tournaments.sort(key = lambda tournament: tournament.date_tournoi)
        season_1.tournaments.reorder()
        
        self.assertEqual(len(season_1.tournaments), 4)
        self.assertEqual(len(season_2.tournaments), 1)
        
        self.assertEqual(season_1.tournaments[0].position, 1)
        self.assertEqual(season_1.tournaments[1].position, 2)
        self.assertEqual(season_1.tournaments[2].position, 3)
        self.assertEqual(season_1.tournaments[3].position, 4)
        self.assertEqual(season_2.tournaments[0].position, 1)
        
        self.assertEqual(season_1.tournaments[0].date_tournoi, datetime.date(2009, 8, 31))
        self.assertEqual(season_1.tournaments[1].date_tournoi, datetime.date(2009, 9, 1))
        self.assertEqual(season_1.tournaments[2].date_tournoi, datetime.date(2010, 1, 1))
        self.assertEqual(season_1.tournaments[3].date_tournoi, datetime.date(2010, 2, 1))
        self.assertEqual(season_2.tournaments[0].date_tournoi, datetime.date(2010, 9, 1))

        # config.orm.commit()


        

