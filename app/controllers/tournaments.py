# -*- coding: utf-8 -*-

from app.forms import tournament_forms
from app.models import Tournament, User
from app.notifications import notify_via_email, Events
from app.utils import session, http
from web import config
import web

class AdminResults :
    
    @session.login_required(User.BaseLevels.ADMIN)
    def GET(self):
        
        tournament_id = web.input(tournament_id=None).tournament_id
        
        if tournament_id is None:
            raise web.notfound()
        
        tournament = Tournament.get(int(tournament_id), joined_attrs=["results"])

        if tournament is None:
            raise web.notfound()
        
        results_grid = tournament_forms.EditResultsGrid().bind(tournament.results)
        
        return config.views.results_admin(tournament, results_grid)

    @session.login_required(User.BaseLevels.ADMIN)
    @http.jsonify
    def POST(self):
        
        input = web.input(tournament_id=None)
        tournament_id = input.tournament_id

        if tournament_id is None:
            raise web.notfound() 

        tournament = Tournament.get(int(tournament_id), joined_attrs=["results"])

        if tournament is None:
            raise web.notfound()
        
        results_grid = tournament_forms.EditResultsGrid().bind(tournament.results, data=input)
        
        if results_grid.validate():
            # If the form was properly filled, updates the model and returns the standard table
            # Besides, we sort the results manually since they are directly returned (commit & no load)
            results_grid.sync()
            tournament.sort_results()
            results = config.views.results(tournament)
            statistics = config.views.statistics(tournament)
        else:
            # Otherwise, returns the editing grid
            results = config.views.results_admin(tournament, results_grid)
            statistics = None
        
        # Returns the dictionary
        return dict(results=results, statistics=statistics)

class AddComment :
    
    @session.login_required
    def POST(self):
        
        # Reads the HTTP request parameters
        input = web.input()
        tournament_id = input.tournament_id
        comment = input.comment
        
        # Appends the comment
        # TODO: variables are ambiguous
        tournament = Tournament.get(int(tournament_id), joined_attrs=["comments"])
        added_comment = tournament.add_comment(config.session_manager.user, comment)
        
        # Registers an email notification
        http.register_hook(lambda: notify_via_email(added_comment, Events.NEW))

        # Returns the dictionary
        return config.views.comment(added_comment)

class UpdateStatus:
    
    @session.login_required
    @http.jsonify
    def POST(self):
        
        # Reads the HTTP request parameters
        input = web.input()
        tournament_id = input.tournament_id
        status = input.status
        
        # Updates the status
        tournament = Tournament.get(int(tournament_id), joined_attrs=["results"])
        tournament.subscribe(config.session_manager.user, status)
        
        # We sort the results manually since they are directly returned (commit & no load)
        tournament.sort_results()
        
        # Returns the dictionary
        return dict(statistics=config.views.statistics(tournament), results=config.views.results(tournament))
    
class View :
    
    @session.login_required
    def GET(self, season_id, position):
        
        tournament = Tournament.get_tournament(int(season_id), int(position))

        if tournament is None:
            raise web.notfound()

        return config.views.layout(
            config.views.tournament(
                tournament,
                config.views.statistics(tournament),
                config.views.results(tournament),
                config.views.comments(tournament, config.views.comment)
            )
        )
