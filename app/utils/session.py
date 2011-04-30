# -*- coding: utf-8 -*-

'''
Created on 17 nov. 2010

@author: fperez
'''


from app.models import orm, User, Session
from web.session import Store
import datetime
import hashlib
import web

#TODO: vérifier que le composant est multi thread

class SqlAlchemyDBStore(Store):
    """Store for saving a session in database
    Needs a table with the following columns:

        session_id CHAR(128) UNIQUE NOT NULL,
        atime DATETIME NOT NULL default current_timestamp,
        data TEXT
    """
    
    def __contains__(self, key):
        data = Session.get(key)
        return bool(data) 

    def __getitem__(self, key):
        
        now = datetime.datetime.now()
        s = Session.get(key)
        s.atime = now
        #orm.commit()
        return self.decode(s.data)
        
    
    def __setitem__(self, key, value):
        pickled = self.encode(value)
        now = datetime.datetime.now()
        s = Session.get(key)
        if s :
            s.data = pickled
            #orm.commit()
        else:
            s = Session(key, now, pickled)
            orm.add(s)
            #orm.commit()

                
    def __delitem__(self, key):
        s = Session.get(key)
        orm.delete(s)
        #orm.commit()

    def cleanup(self, timeout):
        
        timeout = datetime.timedelta(timeout/(24.0*60*60)) #timedelta takes numdays as arg
        last_allowed_time = datetime.datetime.now() - timeout
        
        orm.query(Session).filter(last_allowed_time > Session.atime).delete()
        #orm.commit()



class SessionManager:
    
    def __init__(self, session_handler):
        self.session_handler = session_handler
    
    def __repr__(self) :
        return "<SessionManager(%s)>" % self.session_handler.__dict__
    
    def login(self, user_id, password):
        """ Vérifie les identifiants et impacte la session web le cas échéant """
        
        # Remontée du user
        user = User.get(user_id)
        
        # Encodage du mot de passe passé en paramètres
        password_md5 = hashlib.md5(password).hexdigest()
        
        # On confronte le mot de passe
        if user.password != password_md5:
            web.debug("Utilisateur non reconnu : %d" %user_id)
            return False
        else :
            self.session_handler.user_id = user_id
            self.session_handler.is_logged = True
            web.debug('Session MAJ OK  : %s' %self.session_handler)
            return True
        
    def logout(self):
        """ Se déconnecter """
        self.session_handler.kill()
    
    @property
    def user(self):
        """ Renvoie l'utilisateur loggé dans la session """
        return User.get(self.session_handler.user_id)
    
    @property
    def is_logged(self):
        """ Renvoie True si l'utilisateur est loggé dans la session """
        return self.session_handler.is_logged
    
    def load(self):
        self.session_handler._cleanup()
        self.session_handler._load()
    
    def save(self):
        self.session_handler._save()

def init_manager(session_handler_cls = web.session.Session):
    """ Initialisation globale de la session (appeler avant le démarrage de l'application) """
    
    if web.config.get("_session_manager") is None:
                
        store = SqlAlchemyDBStore()
        session_handler = session_handler_cls(app = None, store = store, initializer = {'is_logged': False, 'user_id' : None})
        session_manager = SessionManager(session_handler)   
        web.config._session_manager = session_manager
        
        web.debug("[WEBSESSION] Armement OK du moteur de session avec le handler %s" %session_handler_cls)

def get_manager():
    """ Récupère la session courante """
    return web.config._session_manager


#def init_session():
#    """ Initialisation globale de la session (appeler avant le démarrage de l'application) """
#    
#    if web.config.get('_session') is None:
#                
#        #db = web.database(dbn='sqlite', db='vpt.db')
#        #store = web.session.DBStore(db, 'sessions')
#        store = SqlAlchemyDBStore()
#        session = web.session.Session(app = None, store = store, initializer = {'is_logged': False, 'user' : None})       
#        web.config._session = session



def configure_session(enabled = True, login_required = False):
    """ Wraps a controller method (GET/POST) in order to handle session management on a per-request basis """
    
    def actual_decorator(func):
        """ The actual decorator returned by configure_session (required for a decorator with arguments) """
        
        if login_required:
            
            # Scenario 1 (session control, login control) : replaces the GET/POST with a wrapped function            
            def wrapped_func(*args):
                
                #print "[SESSION WRAPPER - SCENARIO 1] [BEGIN] Inside wrapped %s method in %s" %(func.__name__, func.__module__)
                session_manager = get_manager()
                session_manager.load()
                
                try:
                    
                    if not session_manager.is_logged:
                        raise web.seeother('/login')
                    return func(*args)
                
                finally:
                    session_manager.save()
                    #print "[SESSION WRAPPER - SCENARIO 1] [END] Inside wrapped %s method in %s" %(func.__name__, func.__module__)
    
            # End of scenario 1 
            #print "[SESSION WRAPPER - SCENARIO 1] Succesfully wrapped %s method in %s" %(func.__name__, func.__module__) 
            return wrapped_func
        
        elif enabled:
            
            # Scenario 2 (session control, no login control) : replaces the GET/POST with a wrapped function
            def wrapped_func(*args):
                
                #print "[SESSION WRAPPER - SCENARIO 2] [BEGIN] Inside wrapped %s method in %s" %(func.__name__, func.__module__)
                session_manager = get_manager()
                session_manager.load()
                
                try :
                    return func(*args)
                finally:
                    session_manager.save()
                    #print "[SESSION WRAPPER - SCENARIO 2] [END] Inside wrapped %s method in %s" %(func.__name__, func.__module__)

            # End of scenario 2 
            #print "[SESSION WRAPPER - SCENARIO 2] Succesfully wrapped %s method in %s" %(func.__name__, func.__module__)
            return wrapped_func
            
        else:
            
            # Scenario 3 (no session control) : the GET/POST is unmodified (actually, it's replaced by itself)
            #print "[SESSION WRAPPER] No wrapped function generated for %s method inside %s" %(func.__name__, func.__module__)
            return func
        
    return actual_decorator


