# -*- coding: utf-8 -*-

from app.utils import session
from web import config
import web


class Logout:
    
    @session.configure_session(enabled = True)
    def GET(self):
        
        config.session_manager.logout()
        raise web.seeother("/")

class Login:
        
    def _login_form(self, email = None):

        if email is None:
            email = ""

        return web.form.Form (
                  web.form.Textbox("email", description="Adresse email : ", value = email),
                  web.form.Password("password", description="Mot de passe : "),
                  web.form.Button("Se connecter", type="submit")                  
                )
    
    @session.configure_session(enabled = False)
    def GET(self):
        
        login_form = self._login_form()
        return config.views.layout(config.views.login(login_form))
    
    @session.configure_session(enabled = True)
    def POST(self):
        
        # Reads the form parameters
        i = web.input()
        email = i.email
        password = i.password
    
        # Tries to log in
        if config.session_manager.login(email, password):
            raise web.seeother("/")
        else:
            login_form = self._login_form(email)
            login_form.valid = False

            return config.views.layout(config.views.login(login_form))
        
        