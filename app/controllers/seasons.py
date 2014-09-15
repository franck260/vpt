# -*- coding: utf-8 -*-

from app.models import Season
from app.utils import session, http
from itertools import groupby
from web import config

class View:

    @session.login_required
    def GET(self, season_id):
        season = Season.get(int(season_id))
        return config.views.layout(
            config.views.season(season, config.views.results(season))
        )

class Results:

    @session.login_required
    @http.jsonify
    def GET(self, season_id):
        season = Season.get(int(season_id))
        results = []
        # Groups the results by user (works because the results are ordered)
        for _, iter_raw_results_by_player in groupby(season.raw_results, lambda r: r.tournament_id):
            results.append({
                raw_result.user_id: raw_result.score 
                for raw_result in iter_raw_results_by_player
            })

        return {
            "players": {player.id: player.pseudonym for player in season.players},
            "results": results
        }
