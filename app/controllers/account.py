# -*- coding: utf-8 -*-

'''
Created on 17 nov. 2010

@author: fperez
'''

from app.models import User
from app.utils import session
from config import views
import web

class Logout:
    
    @session.configure_session(enabled = True)
    def GET(self):
        
        session.get_manager().logout()
        raise web.seeother('/')
        
        

class Login:
    
        
    def __form(self, all_users, selected_user = 1):

        return web.form.Form (
                  web.form.Dropdown('user_id',[(user.id, user.pseudo) for user in all_users], description='Utilisateur : ', value = selected_user),
                  web.form.Password('password', description='Mot de passe : '),
                  web.form.Button('Se connecter', type='submit')                  
                )
    
    @session.configure_session(enabled = False)
    def GET(self):
        
        formulaire = self.__form(User.all())
        return views.login(formulaire)
    
    @session.configure_session(enabled = True)
    def POST(self):
        
        # Récupération de l'identifiant et du mot de passe
        i = web.input(password = None)
        user_id = int(i.user_id)
        password = i.password
    
        # Activation de la session
        if session.get_manager().login(user_id, password):
            raise web.seeother('/')
        else:
            formulaire = self.__form(User.all(), user_id)
            formulaire.valid = False

            return views.login(formulaire)
        
        