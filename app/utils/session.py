# -*- coding: utf-8 -*-

""" Session management built on top of web.py's session component """

from app.models import User, Session
from app.utils import http
from app.utils.mm import multimethod
from functools import wraps
from web import config
from web.session import Store
import datetime
import hashlib
import time
import types
import web

def to_md5(s):
    return hashlib.md5(s).hexdigest()

class SqlAlchemyDBStore(Store):
    """
    Store for saving a session in database
    Needs a table with the following columns:

        session_id CHAR(128) UNIQUE NOT NULL,
        atime DATETIME NOT NULL default current_timestamp,
        data TEXT
    """
    
    def __contains__(self, key):
        s = Session.get(key)
        return s and not s in config.orm.deleted
    
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

class SessionManager(object):
    """
    The session manager should be instantiated once & bound to the application's config.
    
    Essentially, it's a wrapper around the session component built into the framework (the "handler"), including some new features
    (login/logout methods, persistent cookies...) and a different cookie mechanism (the cookie is only sent at login time).
    
    This manager depends on SqlAlchemy to manage the users but this link could be easily broken.
    """
    
    # Duration of persistent cookies
    PERSISTENT_SESSION_DURATION = 30 * 24 * 3600 # 30 days
    
    def __init__(self, session_handler):
        self.session_handler = session_handler
    
    def __repr__(self) :
        return "<SessionManager(%s)>" % self.session_handler.__dict__
    
    def maybe_login(self, email, password, persistent):
        """ Tries to log in and returns the status """
        
        # Fetches the user
        user = User.get_user(email)
        
        # Checks if the user exists
        if user is None:
            web.debug("Unknown user : %s" % email)
            return False
        
        # Checks if the user is active
        if not user.active:
            web.debug("Inactive user : %s" % email)
            return False
        
        # Encodes the password
        password_md5 = to_md5(password)
        
        # Checks the password
        if user.password != password_md5:
            web.debug("Incorrect password for user : %s" % email)
            return False
        else :
            self.login(user, persistent)
            return True
       
    def login(self, user, persistent):
        """
        Actually logs in the user and sets the client-side cookie.
        The cookie is valid for 30 days if persistent is True, until the browser is closed otherwise (session cookie).
        """
        
        if persistent:
            session_duration = self.PERSISTENT_SESSION_DURATION
            expires = int(time.time() + session_duration)
        else:
            session_duration = expires = None

        self.update(user_id=user.id, expires=expires)
        self.session_handler.setcookie(session_duration)
        
        web.debug("Successfully logged in user : %s" % user.email)
    
    def logout(self):
        """ Logs out the currently logged user """
        
        self.lazy_load()
        self.session_handler.kill()
        self.session_handler.setcookie(-1)
        
    def __getattr__(self, name):
        """ Lazily loads the session if needed, and returns the selected attribute """
        
        self.lazy_load()
        return getattr(self.session_handler, name)
    
    @property
    def user(self):
        """ Returns the user logged in the session, or None """
        return self.user_id and User.get(self.user_id)
    
    def lazy_load(self):
        """ Lazily loads the session """
        
        if not self.session_handler.loaded:
            self.session_handler.load()
            
            # If the user passed a cookie which should already have expired, loads a new session_id from the store
            if self.expires and self.expires < time.time():
                self.logout()
                self.session_handler.load()
    
    def update(self, **kwargs):
        """ Wraps the session update process : lazily loads the session if needed, and updates it via the handler """
        
        self.lazy_load()
        
        for key, value in kwargs.items():
            setattr(self.session_handler, key, value)
        
        self.session_handler.save()

class DefaultSessionHandler(web.session.Session):
    """ Session handler inherited from the framework, with a slightly different structure to provide more flexibility """

    def load(self):
        super(DefaultSessionHandler, self)._load()

    @property
    def loaded(self):
        return hasattr(self, "session_id")

    def save(self):
        self.store[self.session_id] = dict(self._data)

    def setcookie(self, session_duration):
        super(DefaultSessionHandler, self)._setcookie(self.session_id, session_duration or "")

    def kill(self):
        super(DefaultSessionHandler, self).kill()
        
class MemorySessionHandler(object):
    """ Simple implementation of a session handler for testing purposes """

    def __init__(self, app, store, initializer=None):
        self.store = store
        self._clear()

    def load(self):
        self.loaded = True

    def save(self):
        pass

    def setcookie(self, session_duration):
        pass
    
    def kill(self):
        self._clear()
    
    def _clear(self):
        self.user_id = None
        self.expires = None
        self.loaded = False
    
def init_session_manager(session_handler_cls):
    """ Instanciates the session manager : should be called at initialization time """
    
    session_handler = globals()[session_handler_cls](app=None, store=SqlAlchemyDBStore(), initializer={"user_id" : None, "expires" : None})
    web.debug("[WEBSESSION] Successfully instanciated session manager with the handler %s" %session_handler_cls)
    return SessionManager(session_handler) 

@multimethod(unicode)
def login_required(base_level):
    """
    Wraps a controller method (GET/POST) in order to handle session management on a per-request basis.
    
    When executed, the wrapped_controller check if the user is logged, if he has sufficient privileges
    (as defined by the base_level attribute) and then only executes the controller.
    """
    
    def actual_decorator(controller):
        """ The actual decorator returned by login_required """
        
        @wraps(controller)      
        def wrapped_controller(*args):
            """ The method which replaces the actual controller """
            
            # Loads the session (if it exists) & reads the user stored in the session backend
            user = config.session_manager.user
    
            if user is None:
                # If the requested path is not the site's index, keep 
                # track of it to redirect the user after successful login
                path = web.ctx.path
                requested_path_parameter = "?next=%s" % path if path != "/" else ""
                raise web.seeother("/login%s" % requested_path_parameter)
            
            elif not user.check_level(base_level):
                # Checks if the user has sufficient access : use cases include administration pages, and scenarios where the user was disabled
                # In this case, the user will get 403 errors as long as its session is valid
                raise web.forbidden()
            
            # Everything is fine, the controller method can be executed
            return controller(*args)            
            
        return wrapped_controller
        
    return actual_decorator

@multimethod(types.FunctionType)
def login_required(controller):
    """ By default, controller methods are reserved to 'guests'. This convenient method allows to decorate controller methods with @login_required instead of @login_required() """
    return login_required(User.BaseLevels.GUEST)(controller)

def login_workflow(user):
    """ Hackish method to perform the login workflow outside of a the regular HTTP request flow """
    http.sqlalchemy_processor(lambda: config.session_manager.login(user, False))
