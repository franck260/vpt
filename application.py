# -*- coding: utf-8 -*-

""" Main application class """

from app.models import meta, Result, Season, Poll
from app.notifications import Events, handlers as notification_handlers
from app.utils import formatting, dates, session, http, webparts
from web import config
import ConfigParser
import collections
import locale
import sys
import web

# Application's URLs
urls = (
    "/",                                    "app.controllers.main.Index",
    
    "/login",                               "app.controllers.account.Login",
    "/logout",                              "app.controllers.account.Logout",
    "/admin/account",                       "app.controllers.account.ViewAccount",
    "/create/account",                      "app.controllers.account.CreateAccount",
    "/update/user",                         "app.controllers.account.UpdateUser",
    "/update/password",                     "app.controllers.account.UpdatePassword",
    "/recover/password",                    "app.controllers.account.RecoverPassword",
    "/reset/password",                      "app.controllers.account.ResetPassword",

    "/season/(\d+)",                        "app.controllers.seasons.View",

    "/poll/(\d+)",                          "app.controllers.polls.View",
    "/poll/vote",                           "app.controllers.polls.Vote",
    "/poll/comment",                        "app.controllers.polls.Comment",

    "/tournament/(\d+)/(\d+)",              "app.controllers.tournaments.View",
    "/update/status",                       "app.controllers.tournaments.UpdateStatus",
    "/add/comment",                         "app.controllers.tournaments.AddComment",
    "/admin/results",                       "app.controllers.tournaments.AdminResults",

    "/admin/(.*)",                          "app.controllers.administration.Admin",

    "/public/(?:img|js|css|doc)/.*",        "app.controllers.public.Public"
)


# Enforces the locale
if sys.platform == "win32":
    locale.setlocale(locale.LC_ALL, "fra")
else:
    locale.setlocale(locale.LC_ALL, "fr_FR")
    
class WebApplication(web.application):
    """ Web application with additional features (configuration management...) """
    
    def __init__(self, mapping, fvars):
        
        # Parent constructor
        web.application.__init__(self, mapping, fvars) #@UndefinedVariable
        
        # The views are bound once for all to the configuration
        config.views = web.template.render("app/views/", globals={
            "all_seasons": lambda: Season.all(),
            "all_polls": lambda: Poll.all(),
            "webparts": webparts,
            "formatting": formatting,
            "dates": dates,
            "zip": zip,
            "getattr": getattr,
            "hasattr": hasattr,
            "class_name": lambda x: x.__class__.__name__,
            "namedtuple": collections.namedtuple,
            "config": config,
            "result_statuses": Result.STATUSES,
            "Events": Events
        })
        
        # The ORM is bound once since it dynamically loads the engine from the configuration
        config.orm = meta.init_orm(lambda : config.engine)
        
        # Binds the hooking mechanism & the SQL Alchemy processor
        self.add_processor(web.loadhook(http.init_hooks))
        self.add_processor(web.unloadhook(http.execute_hooks))        
        self.add_processor(http.sqlalchemy_processor)

        # Binds the webparts initialization mechanism
        self.add_processor(web.loadhook(webparts.init_webparts))
    
    def configure(self, config_filename):
        
        # Reads the configuration file
        config_file = ConfigParser.ConfigParser()
        config_file.read(config_filename)
        
        # Initializes the components
        config.engine = meta.init_engine(config_file.get("sqlalchemy", "dsn"), config_file.getboolean("sqlalchemy", "echo"))
        config.debug = config_file.getboolean("application", "debug")
        config.session_manager = session.init_session_manager(config_file.get("session", "handler_cls"))
        config.email_notification_handler = notification_handlers.init_email_notification_handler(**dict(config_file.items("email_notifications")))
        
        web.debug("[CONFIGURATION] Successfully configured the application from %s" %config_filename)

# The application is instantiated once and should be configured with the configure() method
app = WebApplication(urls, globals())

if __name__ == "__main__":
    
    # Configures the application
    app.configure("development.cfg")

    # Starts the development server
    app.run()