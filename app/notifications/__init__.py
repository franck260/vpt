# -*- coding: utf-8 -*-

""" Handles the email notifications which can be fired in the application """

from app.models import User, TournamentComment, Tournament
from app.notifications.messaging import EMailNotification
from app.utils import Enum, formatting
from app.utils.mm import multimethod, NoSuchMethod
from functools import wraps
from web import config
import web

# The events which can be fired throughout the application
Events = Enum(["NEW", "MODIFIED"])

# The email templates are loaded once
templates = web.template.render("app/notifications/templates/", globals={
    "formatting": formatting
})

class NoSuchTemplate(Exception):
    """ Fired when no suitable template was identified to handle the passed values """
    pass


def templatize(templates_dict):
    """ Wraps a notification builder and tries to inject the output notification into the selected template """
    
    def actual_decorator(func):
            
            @wraps(func)
            def wrapped_func(obj, event):
                
                # Determines the template file name corresponding to the event
                template_name = templates_dict.get(event)
                
                if template_name is None:
                    raise NoSuchTemplate("No template associated with the event %s" % event)
                
                # Reads the actual template file based on the file name
                template = getattr(templates, template_name)
                
                # Builds the notification
                notification = func(obj, event)
                
                # Applies the template & passes the output to the notification
                applied_template = template(obj)
                notification.subject = applied_template.subject
                notification.body = unicode(applied_template)
                
                # Returns the updated notification
                return notification
                
            return wrapped_func
        
    return actual_decorator

def notify_via_email(obj, event):
    """ Main method to send a notification email. Handles cases when no method/template is defined for the object/event couple. """
    
    try:
        email_notification = build_email_notification(obj, event)
        config.email_notification_handler.handle(email_notification)
    except (NoSuchMethod, NoSuchTemplate):
        # Notifications are fired throughout the application : sometimes no method/template is registered to handle it
        pass

@multimethod(TournamentComment, unicode)
@templatize({Events.NEW: "comment_new"})
def build_email_notification(comment, event):
    
    recipients = [user.email for user in User.all() if user != comment.user or user.is_admin]
    return EMailNotification(recipients=recipients)

@multimethod(Tournament, unicode)
@templatize({Events.NEW: "tournament_new"})
def build_email_notification(tournament, event):
    
    recipients = [user.email for user in User.all()]
    return EMailNotification(recipients=recipients)
