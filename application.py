#!/home/franck260/ENV/bin/python
# -*- coding: utf-8 -*-

""" Main application class """

from app.models import meta
from app.models.results import Result
from app.utils import formatting, dates, session
from web import config
import ConfigParser
import locale
import web
import sys

# Application's URLs
urls = (
    "/",                                    "app.controllers.main.Index",
    
    "/login",                               "app.controllers.account.Login",
    "/logout",                              "app.controllers.account.Logout",
    "/admin/account",                       "app.controllers.account.View",
    "/update/user",                         "app.controllers.account.Update_User",
    "/update/password",                     "app.controllers.account.Update_Password",

    "/season/(\d+)",                        "app.controllers.seasons.View",

    "/tournament/(\d+)/(\d+)",              "app.controllers.tournaments.View",
    "/update/status",                       "app.controllers.tournaments.Update_Status",
    "/add/comment",                         "app.controllers.tournaments.Add_Comment",
    "/admin/results/(\d+)",                 "app.controllers.tournaments.Admin_Results",

    "/admin/(.*)",                          "app.controllers.administration.Admin",

    "/public/(?:img|js|css|doc)/.*",        "app.controllers.public.Public"
)


# Enforces the locale
if sys.platform == "win32":
    locale.setlocale(locale.LC_ALL, "fra")
else:
    locale.setlocale(locale.LC_ALL, "fr_FR")
    

def _sqlalchemy_processor(handler):
    """ Makes sure a commit appends at the end of each request """
    try:
        return handler()
    except web.HTTPError:
        config.orm.commit()
        raise
    except:
        config.orm.rollback()
        raise
    finally:
        config.orm.commit()
    

class WebApplication(web.application):
    """ Web application with additional features (configuration management...) """
    
    def __init__(self, mapping, fvars):
        
        # Parent constructor
        web.application.__init__(self, mapping, fvars) #@UndefinedVariable
        
        # The views are bound once for all to the configuration
        config.views = web.template.render("app/views/", globals={
            "formatting": formatting,
            "dates": dates,
            "zip": zip,
            "getattr": getattr,
            "class_name": lambda x: x.__class__.__name__,
            "config": config,
            "result_statuses": Result.STATUSES
        })
        
        # The ORM is bound once since it dynamically loads the engine from the configuration
        config.orm = meta.init_orm(lambda : config.engine)
        
        # SQL Alchemy processor
        self.add_processor(_sqlalchemy_processor)    
    
    def configure(self, config_filename):
        
        # Reads the configuration file
        config_file = ConfigParser.ConfigParser()
        config_file.read(config_filename)
        
        # Initializes the components
        config.engine = meta.init_engine(config_file.get("sqlalchemy", "dsn"), config_file.getboolean("sqlalchemy", "echo"))
        config.debug = config_file.getboolean("application", "debug")
        config.session_manager = session.init_session_manager(getattr(session, config_file.get("session", "handler_cls")))
        
        web.debug("[CONFIGURATION] Sucessfully configured the application from %s" %config_filename)

# The application is instantiated once and should be configured with the configure() method
app = WebApplication(urls, globals())


if __name__ == "__main__":
    
    # Configures the application
    app.configure("development.cfg")

    # Starts the development server
    app.run()
else:
    
    # Enable FCGI
    # TODO: this is no longer useful
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)