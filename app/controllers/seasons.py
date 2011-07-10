# -*- coding: utf-8 -*-

from app.models import Season
from app.utils import session
from web import config


class View:
    
    @session.configure_session(login_required = True)
    def GET(self, id):

        season = Season.get(id)
        
        return config.views.layout(config.views.season(season, config.views.results(season)), Season.all())



    
