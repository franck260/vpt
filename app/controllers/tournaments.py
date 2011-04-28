# -*- coding: utf-8 -*-

'''
Created on 7 janv. 2011

@author: fperez
'''

#TODO: factoriser tous les ViewXXX

from app.models import Season, Tournament
from app.utils import session
from config import views
from sqlalchemy.sql.expression import desc
import urllib
import web


class Add_Comment :
    
    @session.configure_session(login_required = True)
    def POST(self):
        
        # Récupération des paramètres de la requête
        i = web.input()
        tournament_id = i.tournament_id
        comment = i.comment
        
        # Conversion ASCII
        comment = urllib.unquote(comment)
        
        if comment:     
                   
            # Prise en compte du commentaire
            tournament = Tournament.get(tournament_id)
            tournament.add_comment(session.get_manager().user, comment)

        

class Update_Status:
    
    @session.configure_session(login_required = True)
    def POST(self):
        
        # Récupération des paramètres de la requête
        i = web.input()
        tournament_id = i.tournament_id
        statut = i.statut
        
        # Prise en compte du statut
        tournament = Tournament.get(tournament_id)
        tournament.subscribe(session.get_manager().user, statut)
    
    
    
class View :
    
    @session.configure_session(login_required = True)
    def GET(self, season_id, position):
        
        tournament_id, previous_tournament_id, next_tournament_id = Tournament.get_tournaments(int(season_id), int(position))

        if tournament_id is None:
            raise web.notfound()

        tournament = Tournament.get(tournament_id)
        user = session.get_manager().user       
        all_seasons = Season.all(order_by_clause = desc(Season.start_year)) #@UndefinedVariable

        return views.layout(views.tournament(tournament,
                                             views.paging(season_id, previous_tournament_id, next_tournament_id),
                                             views.stats(tournament),
                                             views.results(tournament),
                                             views.comments(tournament)),
                            user,
                            all_seasons,
                            tournament.season.id)
        

class View_Part:

    @session.configure_session(login_required = True)
    def GET(self, context, tournament_id):
        
        tournament = Tournament.get(tournament_id)
        return views.__getattr__(context)(tournament)
       

#class View_Results :
#    
#    @session.configure_session(login_required = True)
#    def GET(self):
#        
#        # Remontée du tournoi
#        tournament = Tournament.get(web.input().tournament_id)
#        
#        return views.results(tournament)
#
#class View_Stats :
#
#    @session.configure_session(login_required = True)
#    def GET(self):
#        
#        # Remontée du tournoi
#        tournament = Tournament.get(web.input().tournament_id)
#        
#        return views.stats(tournament)
#
#class View_Comments:
#
#    @session.configure_session(login_required = True)
#    def GET(self):
#        
#        # Remontée du tournoi
#        tournament = Tournament.get(web.input().tournament_id)
#        
#        return views.comments(tournament)
            
