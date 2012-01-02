# -*- coding: utf-8 -*-

""" Messaging logic to build & send email notifications """

from email.mime.text import MIMEText
import smtplib

class EMailNotification(object):
    """ Simple class for representing an email notification """
    
    def __init__(self, recipients=None, subject=None, body=None):
        self.recipients = recipients or []
        self.subject = subject
        self.body = body
        
    def __repr__(self) :
        # UTF-8 encoding to allow messages to be dumped on most consoles
        return ("Recipients: %s \nSubject: %s \nBody: %s" % (self.recipients, self.subject, self.body)).encode("utf-8")

    def split(self):
        """ Returns a list of similar notifications including only one recipient per instance """
        return [EMailNotification([recipient], self.subject, self.body) for recipient in self.recipients]

def send_email(server_name, user_name, password, email_notification):
    """ Actually sends an email notification with the provided settings """
    
    # Creates a MIME message
    msg = MIMEText(email_notification.body, _charset="utf-8")
    msg["From"] = user_name
    msg["Subject"] = email_notification.subject
    msg["To"] = ", ".join(recipient for recipient in email_notification.recipients)
    
    # Creates the connection
    server = smtplib.SMTP(server_name)
    
    # Sends the message & BCCs the sender for tracking
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user_name, password)
        server.sendmail(user_name, email_notification.recipients + [user_name], msg.as_string())
    finally:
        server.quit()
