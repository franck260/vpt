# -*- coding: utf-8 -*-

#TODO: test login redirection

from app.forms import simple_forms
from app.models import Season
from app.utils import session
from app.utils.session import to_md5
from web import config
import web

class View:
    
    @session.configure_session(login_required=True)
    def GET(self):
        
        user_fieldset = simple_forms.UserFieldSet().bind(config.session_manager.user)
        password_fieldset = simple_forms.PasswordFieldSet().bind(config.session_manager.user)
        
        return config.views.layout(config.views.account(user_fieldset, password_fieldset), Season.all())

class Update_User:
    
    @session.configure_session(login_required=True)  
    def POST(self):
        
        user_fieldset = simple_forms.UserFieldSet().bind(config.session_manager.user, data=web.input())
        password_fieldset = simple_forms.PasswordFieldSet().bind(config.session_manager.user)
        
        if user_fieldset.validate():
            # If the form was properly filled, updates the model and redirects back to home page
            user_fieldset.sync()
            raise web.seeother("/")
        else:
            return config.views.layout(config.views.account(user_fieldset, password_fieldset), Season.all())
        
class Update_Password:
    
    @session.configure_session(login_required=True)  
    def POST(self):
        
        user_fieldset = simple_forms.UserFieldSet().bind(config.session_manager.user)
        password_fieldset = simple_forms.PasswordFieldSet().bind(config.session_manager.user, data=web.input())
        
        if password_fieldset.validate():
            # If the form was properly filled, updates the model and redirects back to home page
            password_fieldset.model.password = to_md5(password_fieldset.new_password.value)
            raise web.seeother("/")
        else:
            return config.views.layout(config.views.account(user_fieldset, password_fieldset), Season.all())

class Logout:
    
    @session.configure_session(enabled=True)
    def GET(self):
        
        #TODO: logout should be done by a POST !
        config.session_manager.logout()
        raise web.seeother("/")

class Login:
        
    @session.configure_session(enabled=False)
    def GET(self):
        return config.views.layout(config.views.login(simple_forms.login_form()))
    
    @session.configure_session(enabled=True)
    def POST(self):
        
        # Reads the form parameters & the previously requested path (if any)
        i = web.input(next="/")
        email = i.email
        password = i.password
        requested_path = i.next
    
        # Tries to log in, and redirects to the previously requested path (if any)
        if config.session_manager.login(email, password):
            raise web.seeother(requested_path)
        else:
            login_form = simple_forms.login_form(email)
            login_form.valid = False

            return config.views.layout(config.views.login(login_form))
