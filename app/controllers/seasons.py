# -*- coding: utf-8 -*-

from app.models import Season
from app.utils import session
from web import config


class View:
    
    @session.login_required
    def GET(self, id):

        season = Season.get(int(id))
        
        return config.views.layout(config.views.season(season, config.views.results(season)), Season.all())



    
