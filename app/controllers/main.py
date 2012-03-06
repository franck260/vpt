# -*- coding: utf-8 -*-

from app.models import Season, Tournament, News
from app.utils import session
from web import config

class Index :
    
    @session.login_required
    def GET(self):
        
        next_tournament = Tournament.next_tournament()
        
        return config.views.layout(config.views.index(next_tournament, News.all()), Season.all())

    
