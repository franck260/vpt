# -*- coding: utf-8 -*-

'''
Created on 17 nov. 2010

@author: fperez
'''

from app.models import Season, Tournament
from app.utils import session
from config import views
from sqlalchemy.sql.expression import desc

class View_Season :
    
    @session.configure_session(login_required = True)
    def GET(self, id):
        
        user = session.get_manager().user       
        season = Season.get(id)
        all_seasons = Season.all(order_by_clause = desc(Season.start_year)) #@UndefinedVariable
        
        return views.layout(views.season(season,
                                         views.results(season)),
                            user,
                            all_seasons,
                            season.id)




class Index :
    
    @session.configure_session(login_required = True)
    def GET(self):
        
        user = session.get_manager().user
        next_tournament = Tournament.next_tournament()
        all_seasons = Season.all(order_by_clause = desc(Season.start_year)) #@UndefinedVariable

        
        return views.layout(views.index(user, next_tournament),
                            user,
                            all_seasons)
    
