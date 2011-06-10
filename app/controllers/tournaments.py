# -*- coding: utf-8 -*-

from app.models import Season, Tournament
from app.utils import session
from sqlalchemy.sql.expression import desc
from web import config
import web

class Add_Comment :
    
    @session.configure_session(login_required=True)
    def POST(self):
        
        # Reads the HTTP request parameters
        i = web.input()
        tournament_id = i.tournament_id
        comment = i.comment
        
        if comment:     
                   
            tournament = Tournament.get(tournament_id)
            tournament.add_comment(config.session_manager.user, comment)

        

class Update_Status:
    
    @session.configure_session(login_required=True)
    def POST(self):
        
        # Reads the HTTP request parameters
        i = web.input()
        tournament_id = i.tournament_id
        statut = i.statut
        
        # Updates the status
        tournament = Tournament.get(tournament_id)
        tournament.subscribe(config.session_manager.user, statut)
    
    
    
class View :
    
    @session.configure_session(login_required=True)
    def GET(self, season_id, position):
        
        tournament = Tournament.get_tournament(int(season_id), int(position))

        if tournament is None:
            raise web.notfound()

        all_seasons = Season.all(order_by_clause=desc(Season.start_year)) #@UndefinedVariable

        return config.views.layout(config.views.tournament(tournament,
                                                           config.views.statistics(tournament),
                                                           config.views.results(tournament),
                                                           config.views.comments(tournament)),
                                   all_seasons)

class View_Part:

    @session.configure_session(login_required=True)
    def GET(self, context, tournament_id):
        
        tournament = Tournament.get(tournament_id)
        return getattr(config.views, context)(tournament)
       
