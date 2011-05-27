# -*- coding: utf-8 -*-

from app.models import Season, Tournament
from app.utils import session
from web import config
from sqlalchemy.sql.expression import desc


class Index :
    
    @session.configure_session(login_required = True)
    def GET(self):
        
        user = config.session_manager.user
        next_tournament = Tournament.next_tournament()
        all_seasons = Season.all(order_by_clause = desc(Season.start_year)) #@UndefinedVariable

        
        return config.views.layout(config.views.index(user, next_tournament),
                                   user,
                                   all_seasons)
    
