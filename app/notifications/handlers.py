# -*- coding: utf-8 -*-

""" The different email notification handlers """

from app.notifications import messaging
from celery.task import task
import smtplib
import web

class EmailNotificationHandler(object):
    """ Parent of all email notification handlers """
    
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

class AsynchronousEmailNotificationHandler(EmailNotificationHandler):
    """ Asynchronously sends an email with Celery """

    @task(max_retries=10, default_retry_delay=180)
    def send_notification(self, email_notification):
        try:
            messaging.send_email(self.host, self.user, self.password, email_notification)
        except smtplib.SMTPException, exc:
            self.send_notification.retry(exc=exc)

    @task
    def split_notification(self, email_notification):
        [self.send_notification.delay(self, single_notification) for single_notification in email_notification.split()]
        
    def handle(self, email_notification):
        self.split_notification.delay(self, email_notification)

class ConsoleEmailNotificationHandler(EmailNotificationHandler):
    """ Outputs the email on the console """
    
    def handle(self, email_notification):
        web.debug(email_notification)

class DummyEmailNotificationHandler(EmailNotificationHandler):
    """ Does nothing with the notification (useful for testing purposes) """

    def handle(self, email_notification):
        pass

def init_email_notification_handler(**kwargs):
    """ Instanciates the notification handler """
    
    # The handler class is mandatory
    handler_cls = kwargs.get("handler_cls")
    
    # The other settings are optional
    handler_host = kwargs.get("handler_host", None)
    handler_user = kwargs.get("handler_user", None)
    handler_password = kwargs.get("handler_password", None)
    
    # Actually instanciates the handler
    handler = globals()[handler_cls](handler_host, handler_user, handler_password)
    web.debug("[NOTIFICATIONS] Successfully instanciated notification handler from the class %s" % handler_cls)
    
    return handler
