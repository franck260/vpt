# -*- coding: utf-8 -*-

#TODO: test login redirection

from app.forms import user_forms
from app.models import Season, UserToken, PasswordToken, User
from app.notifications import notify_via_email, Events
from app.utils import session, formatting, dates, http
from web import config
import web

class ViewAccount:
    
    @session.configure_session(login_required=True)
    def GET(self):
        
        user_fieldset = user_forms.EditUserFieldSet().bind(config.session_manager.user)
        password_fieldset = user_forms.EditPasswordFieldSet().bind(config.session_manager.user)
        
        return config.views.layout(config.views.account(user_fieldset, password_fieldset), Season.all())

class UpdateUser:
    
    @session.configure_session(login_required=True)  
    def POST(self):
        
        user_fieldset = user_forms.EditUserFieldSet().bind(config.session_manager.user, data=web.input())
        password_fieldset = user_forms.EditPasswordFieldSet().bind(config.session_manager.user)
        
        # Synchronizes the fieldset
        if user_fieldset.validate():
            user_fieldset.sync()
            raise web.seeother("/")
        else:
            return config.views.layout(config.views.account(user_fieldset, password_fieldset), Season.all())
        
class UpdatePassword:
    
    @session.configure_session(login_required=True)  
    def POST(self):
        
        user_fieldset = user_forms.EditUserFieldSet().bind(config.session_manager.user)
        password_fieldset = user_forms.EditPasswordFieldSet().bind(config.session_manager.user, data=web.input())
        
        # Synchronizes the fieldset
        if password_fieldset.validate():
            password_fieldset.sync()
            raise web.seeother("/")
        else:
            return config.views.layout(config.views.account(user_fieldset, password_fieldset), Season.all())

class RecoverPassword:

    @session.configure_session(enabled=False)
    def POST(self):
        
        # Reads the email in the HTTP request parameters
        email = web.input(email=None).email
        
        # Check if the user exists and is active
        user = User.get_user(email)
              
        if user is None or not user.active:
            raise web.forbidden("Utilisateur inconnu")
        
        # Checks if there is already an active password token matching this email
        current_password_token = PasswordToken.get_password_token(email)
        
        if current_password_token is not None:
            formatted_creation_dt = formatting.format_date(dates.change_timezone(current_password_token.creation_dt), "%d/%m/%y %H:%M")
            raise web.forbidden(u"Demande similaire déjà effectuée le %s" % formatted_creation_dt)
        
        # Creates a new password token valid for 2 days
        password_token = PasswordToken(validity=2, user=user, token=PasswordToken.generate_random_token(16))
        config.orm.add(password_token)
        
        # Registers an email notification
        http.register_hook(lambda: notify_via_email(password_token, Events.NEW))
        
        return u"Instructions en cours d'envoi à %s" % email

class ResetPassword:
    
    @session.configure_session(enabled=False)
    def GET(self):
        
        # Reads the token in the HTTP request parameters
        token = web.input(token=None).token
        
        # Checks if the token is valid
        password_token = PasswordToken.get_token(token)
        
        if password_token is None or password_token.expired:
            raise web.forbidden()
        
        # The fieldset is bound to the user associated with the token
        password_fieldset = user_forms.NewPasswordFieldSet().bind(password_token.user)
        return config.views.layout(config.views.creation_form(password_fieldset))
    
    @session.configure_session(enabled=False)
    def POST(self):
        
        # Reads the token in the HTTP request parameters
        token = web.input(token=None).token
        
        # Checks if the token is valid
        password_token = PasswordToken.get_token(token)
        
        if password_token is None or password_token.expired:
            raise web.forbidden()
        
        # The fieldset is bound to the form data & the user associated with the token : the token itself is passed because it should expire when successfully used
        password_fieldset = user_forms.NewPasswordFieldSet(password_token).bind(password_token.user, data=web.input())

        # Synchronizes the fieldset & registers a delayed login of the user (we could do it now but it's better to isolate the login process)
        if password_fieldset.validate():
            password_fieldset.sync()
            http.register_hook(lambda: session.login_workflow(password_fieldset.model))
            raise web.seeother("/")
        else:
            return config.views.layout(config.views.creation_form(password_fieldset))

class CreateAccount:
    
    @session.configure_session(enabled=False)
    def GET(self):
        
        # Reads the token in the HTTP request parameters
        token = web.input(token=None).token
        
        # Checks if the token is valid
        user_token = UserToken.get_token(token)
        
        if user_token is None or user_token.expired:
            raise web.forbidden()
        
        # The fieldset is not bound to any specific instance : the token is passed because it contains the email
        user_fieldset = user_forms.NewUserFieldSet(user_token)
        return config.views.layout(config.views.creation_form(user_fieldset))
    
    @session.configure_session(enabled=False)
    def POST(self):
        
        # Reads the token in the HTTP request parameters
        token = web.input(token=None).token
        
        # Checks if the token is valid
        user_token = UserToken.get_token(token)
        
        if user_token is None or user_token.expired:
            raise web.forbidden()
        
        # The fieldset is bound to the form data & the session : the token is passed because it contains the level
        user_fieldset = user_forms.NewUserFieldSet(user_token).bind(data=web.input(), session=config.orm)
        
        # Synchronizes the fieldset & registers a delayed login of the user (because the user id is not available yet)
        if user_fieldset.validate():
            user_fieldset.sync()
            http.register_hook(lambda: session.login_workflow(user_fieldset.model))
            raise web.seeother("/")
        else:
            return config.views.layout(config.views.creation_form(user_fieldset))
    
class Logout:
    
    @session.configure_session(enabled=True)
    def GET(self):
        
        #TODO: logout should be done by a POST !
        config.session_manager.logout()
        raise web.seeother("/")

class Login:
        
    @session.configure_session(enabled=False)
    def GET(self):
        return config.views.layout(config.views.login(user_forms.login_form(), user_forms.recover_password_form()))
    
    @session.configure_session(enabled=True)
    def POST(self):
        
        # Reads the form parameters & the previously requested path (if any)
        input = web.input(next="/")
        email = input.email
        password = input.password
        requested_path = input.next
    
        # Tries to log in, and redirects to the previously requested path (if any)
        if config.session_manager.maybe_login(email, password):
            raise web.seeother(requested_path)
        else:
            login_form = user_forms.login_form(email)
            login_form.valid = False

            return config.views.layout(config.views.login(login_form, user_forms.recover_password_form()))
