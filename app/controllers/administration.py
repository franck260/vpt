# -*- coding: utf-8 -*-

"""
Generic administration controller.
Most calls to /admin/components will land here : the 'components' key must be properly registered below.
"""

from app.forms import admin_forms
from app.models import Season
from app.utils import session
from collections import namedtuple
from web import config
import web

# Named tuple to define an administration component (Python 2.6)
AdminComponent = namedtuple("AdminComponent",  ["grid", "fieldset"])

ADMIN_COMPONENTS = {"seasons"     : AdminComponent(admin_forms.SeasonsGrid, admin_forms.SeasonFieldSet),
                    "tournaments" : AdminComponent(admin_forms.TournamentsGrid, admin_forms.TournamentFieldSet)
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
        if i.action == "edit":
            
            # The grid should be bound to the form data
            component_to_sync = grid =  ADMIN_COMPONENTS.get(key).grid()
            grid.rebind(data=web.input())
            fieldset = ADMIN_COMPONENTS.get(key).fieldset()
        
        # Scenario 2 : create a new element
        elif i.action == "new":
            
            # The fieldset should be bound to the form data & the session
            grid =  ADMIN_COMPONENTS.get(key).grid()
            component_to_sync = fieldset = ADMIN_COMPONENTS.get(key).fieldset().bind(data=web.input(), session=config.orm)
        
        # Scenario 3 : invalid action
        else:
            raise web.notfound()
        
        # Synchronizes the grid or the fieldset (depending on the action)
        if component_to_sync.validate():
            component_to_sync.sync()
            raise web.seeother("/")
        else:
            return config.views.layout(config.views.administration(grid, fieldset), Season.all())

    
