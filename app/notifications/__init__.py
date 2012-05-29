# -*- coding: utf-8 -*-

""" Handles the email notifications which can be fired in the application """

from app.models import User, TournamentComment, Tournament, UserToken, \
    PollComment, PasswordToken, Poll, PollVote
from app.notifications.messaging import EMailNotification
from app.utils import Enum, formatting, dates
from app.utils.mm import multimethod, NoSuchMethod
from functools import wraps
from web import config
import web

# The events which can be fired throughout the application
Events = Enum(["NEW", "MODIFIED"])

# The email templates are loaded once
templates = web.template.render("app/notifications/templates/", globals={
    "formatting": formatting,
    "sorted": sorted,
    "dates": dates
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
@templatize({Events.NEW: "tournament_comment_new"})
def build_email_notification(comment, event):
    
    recipients = [user.email for user in User.all() if user.admin or (user != comment.user and user.active)]
    return EMailNotification(recipients=recipients)

@multimethod(PollComment, unicode)
@templatize({Events.NEW: "poll_comment_new"})
def build_email_notification(comment, event):
    
    recipients = [user.email for user in User.all() if user.admin or (user != comment.user and user.active)]
    return EMailNotification(recipients=recipients)

@multimethod(PollVote, unicode)
@templatize({Events.NEW: "poll_vote_new", Events.MODIFIED: "poll_vote_modified"})
def build_email_notification(poll_vote, event):
    
    recipients = [user.email for user in User.all() if user.admin]
    return EMailNotification(recipients=recipients)

@multimethod(Poll, unicode)
@templatize({Events.NEW: "poll_new"})
def build_email_notification(poll, event):
    
    recipients = [user.email for user in User.all() if user.active]
    return EMailNotification(recipients=recipients)

@multimethod(Tournament, unicode)
@templatize({Events.NEW: "tournament_new"})
def build_email_notification(tournament, event):
    
    recipients = [user.email for user in User.all() if user.active]
    return EMailNotification(recipients=recipients)

@multimethod(UserToken, unicode)
@templatize({Events.NEW: "user_token_new"})
def build_email_notification(user_token, event):
    
    recipients = [user_token.email] + [user.email for user in User.all() if user.admin]
    return EMailNotification(recipients=recipients)

@multimethod(PasswordToken, unicode)
@templatize({Events.NEW: "password_token_new"})
def build_email_notification(password_token, event):
    
    recipients = [password_token.user.email] + [user.email for user in User.all() if user.admin and user != password_token.user]
    return EMailNotification(recipients=recipients)
