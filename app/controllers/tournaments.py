# -*- coding: utf-8 -*-

from app.controllers import forms
from app.models import Season, Tournament
from app.utils import session, http
from web import config
import web

class Admin_Results :
    
    @session.configure_session(login_required=True)
    @session.administration
    def GET(self, tournament_id):
        
        tournament = Tournament.get(int(tournament_id), joined_attrs=["results"])

        if tournament is None:
            raise web.notfound()
        
        results_fieldset = forms.ResultsFieldSet().bind(tournament.results)
        
        return config.views.results_admin(tournament, results_fieldset)

    @session.configure_session(login_required=True)
    @session.administration
    @http.jsonify
    def POST(self, tournament_id):
        
        tournament = Tournament.get(int(tournament_id), joined_attrs=["results"])

        if tournament is None:
            raise web.notfound()
        
        results_fieldset = forms.ResultsFieldSet().bind(tournament.results, data=web.input())
        
        if results_fieldset.validate():
            # If the form was properly filled, updates the model and returns the standard table
            # Besides, we sort the results manually since they are directly returned (commit & no load)
            results_fieldset.sync()
            tournament.sort_results()
            results = config.views.results(tournament)
            statistics = config.views.statistics(tournament)
        else:
            # Otherwise, returns the editing grid
            results = config.views.results_admin(tournament, results_fieldset)
            statistics = None
        
        # Returns the dictionary
        return dict(results=results, statistics=statistics)

class Add_Comment :
    
    @session.configure_session(login_required=True)
    @http.jsonify
    def POST(self):
        
        # Reads the HTTP request parameters
        i = web.input()
        tournament_id = i.tournament_id
        comment = i.comment
        
        # Appends the comment
        tournament = Tournament.get(int(tournament_id), joined_attrs=["comments"])
        tournament.add_comment(config.session_manager.user, comment)

        # Returns the dictionary
        return dict(comments=config.views.comments(tournament))

class Update_Status:
    
    @session.configure_session(login_required=True)
    @http.jsonify
    def POST(self):
        
        # Reads the HTTP request parameters
        i = web.input()
        tournament_id = i.tournament_id
        status = i.status
        
        # Updates the status
        tournament = Tournament.get(int(tournament_id), joined_attrs=["results"])
        tournament.subscribe(config.session_manager.user, status)
        
        # We sort the results manually since they are directly returned (commit & no load)
        tournament.sort_results()
        
        # Returns the dictionary
        return dict(statistics=config.views.statistics(tournament), results=config.views.results(tournament))
    
class View :
    
    @session.configure_session(login_required=True)
    def GET(self, season_id, position):
        
        tournament = Tournament.get_tournament(int(season_id), int(position))

        if tournament is None:
            raise web.notfound()

        return config.views.layout(config.views.tournament(tournament,
                                                           config.views.statistics(tournament),
                                                           config.views.results(tournament),
                                                           config.views.comments(tournament)),
                                   Season.all())

       
