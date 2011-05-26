# -*- coding: utf-8 -*-

""" Session management """

from app.models import User, Session
from web import config
from web.session import Store
import datetime
import hashlib
import web
from sqlalchemy.orm.exc import NoResultFound

class SqlAlchemyDBStore(Store):
    """
    Store for saving a session in database
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
        return self.decode(s.data)
        
    
    def __setitem__(self, key, value):
        pickled = self.encode(value)
        now = datetime.datetime.now()
        s = Session.get(key)
        if s :
            s.data = pickled
        else:
            s = Session(key, now, pickled)
            config.orm.add(s)
                
    def __delitem__(self, key):
        s = Session.get(key)
        config.orm.delete(s)

    def cleanup(self, timeout):
        
        timeout = datetime.timedelta(timeout/(24.0*60*60)) #timedelta takes numdays as arg
        last_allowed_time = datetime.datetime.now() - timeout
        
        config.orm.query(Session).filter(last_allowed_time > Session.atime).delete()

class SessionManager(object):
    
    def __init__(self, session_handler):
        self.session_handler = session_handler
    
    def __repr__(self) :
        return "<SessionManager(%s)>" % self.session_handler.__dict__
    
    def login(self, email, password):
        """ Tries to log in and returns the status """
        
        # Fetches the user
        try:
            user = config.orm.query(User).filter(User.email == email).one() #@UndefinedVariable
        except NoResultFound:
            web.debug("Unknown user : %s" %email)
            return False
        
        # Encodes the password
        password_md5 = hashlib.md5(password).hexdigest()
        
        # Checks the password
        if user.password != password_md5:
            web.debug("Incorrect password for user : %s" %email)
            return False
        else :
            self.session_handler.user_id = user.id
            self.session_handler.is_logged = True
            web.debug("Successfully updated session : %s" %self.session_handler)
            return True
        
    def logout(self):
        """ Logs out the currently logged user """
        self.session_handler.kill()
    
    @property
    def user(self):
        """ Returns the user logged in the session """
        return User.get(self.session_handler.user_id)
    
    @property
    def is_logged(self):
        """ Returns true if the user is authenticated """
        return self.session_handler.is_logged
    
    def load(self):
        self.session_handler._cleanup()
        self.session_handler._load()
    
    def save(self):
        self.session_handler._save()

DefaultSessionHandler = web.session.Session

class MemorySessionHandler(object):
    """ Simple implementation of a SessionHandler for testing purposes """
    
    def __init__(self, app, store, initializer=None):
        self.is_logged = False
        self.user_id = None
    
    def _cleanup(self):
        pass
    
    def _load(self):
        pass
    
    def _save(self):
        pass
    
    def kill(self):
        self.is_logged = False
        self.user_id = None

def init_session_manager(session_handler_cls):
    """ Instanciates the session manager """
    
    store = SqlAlchemyDBStore()
    session_handler = session_handler_cls(app = None, store = store, initializer = {'is_logged': False, 'user_id' : None})
    web.debug("[WEBSESSION] Sucessfully instanciated session manager with the handler %s" %session_handler_cls)
    return SessionManager(session_handler) 
    


def configure_session(enabled = True, login_required = False):
    """ Wraps a controller method (GET/POST) in order to handle session management on a per-request basis """
    
    def actual_decorator(func):
        """ The actual decorator returned by configure_session (required for a decorator with arguments) """
        
        if login_required:
            
            # Scenario 1 (session control, login control) : replaces the GET/POST with a wrapped function            
            def wrapped_func(*args):
                
                #print "[SESSION WRAPPER - SCENARIO 1] [BEGIN] Inside wrapped %s method in %s" %(func.__name__, func.__module__)
                session_manager = config.session_manager
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
                session_manager = config.session_manager
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


