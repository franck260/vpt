# -*- coding: utf-8 -*-

'''
Created on 17 nov. 2010

@author: fperez
'''

from app import models
from app.models import orm
from app.utils import session
import config
import locale
import web

# Paramétrage des URLS
urls = (
    '/',                               'app.controllers.main.Index',
    '/season/(\d+)',                   'app.controllers.main.View_Season',
    
    '/tournament/(\d+)/(\d+)',         'app.controllers.tournaments.View',
    '/(stats|results|comments)/(\d+)', 'app.controllers.tournaments.View_Part',   
#    '/tournament_stats',              'app.controllers.tournaments.View_Stats',
#    '/tournament_results',            'app.controllers.tournaments.View_Results',
#    '/tournament_comments',           'app.controllers.tournaments.View_Comments',
    '/updateStatus',                   'app.controllers.tournaments.Update_Status',
    '/addComment',                     'app.controllers.tournaments.Add_Comment',
    
    '/login',                          'app.controllers.account.Login',
    '/logout',                         'app.controllers.account.Logout',
    '/account',                        'app.controllers.account.View',
    
     '/(?:img|js|css)/.*',             'app.controllers.public.Public'
)


# buyin en place d'un processor pour effectuer un commit par requête
def sqlalchemy_processor(handler):
    try:
        return handler()
    except web.HTTPError:
        orm.commit()
        raise
    except:
        orm.rollback()
        raise
    finally:
        orm.commit()

# Définition de la locale
locale.setlocale(locale.LC_ALL, '')

# Init de l'application
app = web.application(urls, globals())
app.add_processor(sqlalchemy_processor)


if __name__ == "__main__" :

    #TODO: améliorer nommages
    # Initialisation de la session web
    session.init_manager()

    # Initialisation de la session SQLAlchemy
    models.init_sqlalchemy_session(config.DATABASE)

    # Démarrage du serveur
    app.run()