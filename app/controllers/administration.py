# -*- coding: utf-8 -*-

"""
Generic administration controller.
Most calls to /admin/(.*) will land here : the 'components' key must be properly registered below.
"""

from app.forms.admin_forms import season_forms, tournament_forms, news_forms
from app.models import Season
from app.notifications import Events, notify_via_email
from app.utils import session
from collections import namedtuple
from web import config
import web

# Named tuple to define an administration component (Python 2.6)
AdminComponent = namedtuple("AdminComponent",  ["grid", "fieldset"])

# HTTP requests to /admin/(.*) are routed through this dictionary : administration components must be declared accordingly
ADMIN_COMPONENTS = {"seasons"     : AdminComponent(season_forms.SeasonsGrid, season_forms.SeasonFieldSet),
                    "tournaments" : AdminComponent(tournament_forms.TournamentsGrid, tournament_forms.TournamentFieldSet),
                    "news" : AdminComponent(news_forms.NewsGrid, news_forms.NewsFieldSet)
                    }

class Admin:
    
    @session.configure_session(login_required = True)
    @session.administration
    def GET(self, key):

        if not key in ADMIN_COMPONENTS:
            raise web.notfound()

        # The fieldset is not bound to any specific instance, where as the grid should automatically be populated with all instances
        grid =  ADMIN_COMPONENTS.get(key).grid()
        fieldset = ADMIN_COMPONENTS.get(key).fieldset()
        
        return config.views.layout(config.views.administration(grid, fieldset), Season.all())
        
    @session.configure_session(login_required = True)
    @session.administration
    def POST(self, key):

        if not key in ADMIN_COMPONENTS:
            raise web.notfound()

        i = web.input()
        
        # Scenario 1 : edit an existing element
        if i.event == Events.MODIFIED:
            
            # The grid should be bound to the form data
            component_to_sync = grid =  ADMIN_COMPONENTS.get(key).grid()
            grid.rebind(data=web.input())
            fieldset = ADMIN_COMPONENTS.get(key).fieldset()
        
        # Scenario 2 : create a new element
        elif i.event == Events.NEW:
            
            # The fieldset should be bound to the form data & the session
            grid =  ADMIN_COMPONENTS.get(key).grid()
            component_to_sync = fieldset = ADMIN_COMPONENTS.get(key).fieldset().bind(data=web.input(), session=config.orm)
        
        # Scenario 3 : invalid action
        else:
            raise web.notfound()
        
        # Synchronizes the grid or the fieldset (depending on the action) & tries to send an email notification (if configured)
        if component_to_sync.validate():
            component_to_sync.sync()
            notify_via_email(component_to_sync.model, i.event)
            raise web.seeother("/")
        else:
            return config.views.layout(config.views.administration(grid, fieldset), Season.all())

    
