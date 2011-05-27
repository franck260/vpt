# -*- coding: utf-8 -*-

from app.models import Season
from app.utils import session
from sqlalchemy.sql.expression import desc
from web import config


class View:
    
    @session.configure_session(login_required = True)
    def GET(self, id):

        user = config.session_manager.user       
        season = Season.get(id)
        all_seasons = Season.all(order_by_clause = desc(Season.start_year)) #@UndefinedVariable
        
        return config.views.layout(config.views.season(season, config.views.results(season)),
                                   user,
                                   all_seasons,
                                   season.id)



    
