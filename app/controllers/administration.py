# -*- coding: utf-8 -*-

"""
Generic administration controller.
Most calls to /admin/(.*) will land here : the 'components' key must be properly registered below.
"""

from app.forms import season_forms, tournament_forms, news_forms, user_forms, \
    session_forms, poll_forms
from app.models import User
from app.notifications import Events, notify_via_email
from app.utils import session, http
from collections import namedtuple
from web import config
import web

# Named tuple to define an administration component (Python 2.6)
AdminComponent = namedtuple("AdminComponent",  ["grid_component", "fieldset_component"])

# Do not use None to indicate that a component has no grid_component or no fieldset_component, but this lambda instead
NOTHING = lambda: None

# HTTP requests to /admin/(.*) are routed through this dictionary : administration components must be declared accordingly
ADMIN_COMPONENTS = {
    "seasons"     : AdminComponent(season_forms.EditSeasonsGrid, season_forms.NewSeasonFieldSet),
    "tournaments" : AdminComponent(tournament_forms.EditTournamentsGrid, tournament_forms.NewTournamentFieldSet),
    "news" : AdminComponent(news_forms.EditNewsGrid, news_forms.NewNewsFieldSet),
    "users" : AdminComponent(user_forms.EditUsersGrid, user_forms.NewUserTokenFieldSet),
    "sessions" : AdminComponent(session_forms.EditSessionsGrid, NOTHING),
    "polls" : AdminComponent(poll_forms.EditPollsGrid, poll_forms.NewPollFieldSet)
}

class Admin:
    
    @session.login_required(User.BaseLevels.ADMIN)
    def GET(self, key):

        if not key in ADMIN_COMPONENTS:
            raise web.notfound()

        # The fieldset is not bound to any specific instance, where as the grid should automatically be populated with all instances
        grid =  ADMIN_COMPONENTS.get(key).grid_component()
        fieldset = ADMIN_COMPONENTS.get(key).fieldset_component()
        
        return config.views.layout(config.views.administration(grid, fieldset))
        
    @session.login_required(User.BaseLevels.ADMIN)
    def POST(self, key):
        
        if not key in ADMIN_COMPONENTS:
            raise web.notfound()

        http_input = web.input()
        
        # Scenario 1 : edit an existing element
        if http_input.event == Events.MODIFIED:
            
            # The grid should be bound to the form data
            component_to_sync = grid =  ADMIN_COMPONENTS.get(key).grid_component()
            grid.rebind(data=http_input)
            fieldset = ADMIN_COMPONENTS.get(key).fieldset_component()
        
        # Scenario 2 : create a new element
        elif http_input.event == Events.NEW:
            
            # The fieldset should be bound to the form data & the session
            grid =  ADMIN_COMPONENTS.get(key).grid_component()
            component_to_sync = fieldset = ADMIN_COMPONENTS.get(key).fieldset_component().bind(data=http_input, session=config.orm)
        
        # Scenario 3 : invalid action
        else:
            raise web.notfound()
        
        # Synchronizes the grid or the fieldset (depending on the action) & registers an email notification
        if component_to_sync.validate():
            component_to_sync.sync()
            http.register_hook(lambda: notify_via_email(component_to_sync.model, http_input.event))
            raise web.seeother("/")
        else:
            return config.views.layout(config.views.administration(grid, fieldset))

    
