# -*- coding: utf-8 -*-

""" Simple forms used by the controllers (except the generic administration one) """

from app.forms import custom_validators
from app.models import User, Result
from app.utils import formatting
from formalchemy import FieldSet, validators
from formalchemy.fields import Field
from formalchemy.tables import Grid
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
    
    def __init__(self):
        
        FieldSet.__init__(self, User)

        self.append(Field("old_password"))
        self.append(Field("new_password"))
        self.append(Field("new_password_confirm"))
        
        inc = [self.old_password.label(u"Ancien mot de passe").password().required().validate(custom_validators.old_password_validator),
               self.new_password.label(u"Nouveau mot de passe").password().required().validate(validators.minlength(4)),
               self.new_password_confirm.label(u"Nouveau mot de passe (confirmation)").password().required().validate(validators.minlength(4)).validate(custom_validators.new_password_validator),
               ]
        
        self.configure(include=inc)

class ResultsGrid(Grid):
    """ FormAlchemy grid used to edit tournament results """
        
    def __init__(self):
        
        Grid.__init__(self, Result)
        
        STATUS_OPTIONS = [(u"Présent", Result.STATUSES.P), (u"Absent", Result.STATUSES.A), (u"Peut-être", Result.STATUSES.M)]
        RANK_OPTIONS = [(u"", None)] + [(formatting.append(i, formatting.to_rank), i) for i in range(1, len(User.all()))]

        self.append(Field("pseudonym", value=lambda result: result.user.pseudonym))
        
        inc = [self.pseudonym.label(u"Joueur").readonly(),
               self.status.label(u"Statut").dropdown(options=STATUS_OPTIONS),
               self.buyin.label(u"Mise").validate(custom_validators.required_for([Result.STATUSES.P])).validate(custom_validators.forbidden_for([Result.STATUSES.M, Result.STATUSES.A])),
               self.rank.label(u"Classement").dropdown(options=RANK_OPTIONS).validate(custom_validators.forbidden_for([Result.STATUSES.M, Result.STATUSES.A])),
               self.profit.label(u"Gain").validate(custom_validators.forbidden_for([Result.STATUSES.M, Result.STATUSES.A])),
               ]
        
        self.configure(include=inc)
        
