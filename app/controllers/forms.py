# -*- coding: utf-8 -*-

""" All the input forms used by the controllers """

from app.models import User
from app.utils.session import to_md5
from formalchemy import FieldSet, validators
from formalchemy.fields import Field
import web

def login_form(email = None):
    """ Web.py form used for the login screen """

    if email is None:
        email = ""

    return web.form.Form (
              web.form.Textbox("email", description="Adresse email : ", value=email),
              web.form.Password("password", description="Mot de passe : "),
              web.form.Button("Se connecter", type="submit")                  
            )
    

class UserFieldSet(FieldSet):
    """ FormAlchemy form used to edit users """
    
    def __init__(self):
        
        FieldSet.__init__(self, User)

        inc = [self.pseudonym.label(u"Pseudo"),
               self.first_name.label(u"Prénom"),
               self.last_name.label(u"Nom"),
               self.email.label(u"Adresse email").validate(validators.email)
               ]
        
        self.configure(include=inc)

class PasswordFieldSet(FieldSet):
    """ FormAlchemy form used to edit passwords """

    @staticmethod
    def old_password_validator(value, field):
        
        if field.parent.model.password != to_md5(value):
            raise validators.ValidationError("Invalid value")
        
    @staticmethod
    def new_password_validator(value, field):
        
        if field.parent.new_password.value != value:
            raise validators.ValidationError("Passwords do not match")
    
    def __init__(self):
        
        FieldSet.__init__(self, User)

        self.add(Field("old_password"))
        self.add(Field("new_password"))
        self.add(Field("new_password_confirm"))
        
        inc = [self.old_password.password().label(u"Ancien mot de passe").required().validate(self.old_password_validator),
               self.new_password.password().label(u"Nouveau mot de passe").required().validate(validators.minlength(4)),
               self.new_password_confirm.password().label(u"Nouveau mot de passe (confirmation)").required().validate(validators.minlength(4)).validate(self.new_password_validator),
               ]
        
        self.configure(include=inc)

