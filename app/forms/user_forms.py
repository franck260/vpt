# -*- coding: utf-8 -*-

""" Administration & user-facing forms used to edit users """

from app.forms import custom_validators, CustomFieldSet
from app.models import User, UserToken
from app.utils.session import to_md5
from formalchemy import validators, FieldSet
from formalchemy.fields import Field
from formalchemy.tables import Grid
from web import config
import web

# Lambda methods used to enrich the fields with labels & validators
ID_READONLY = lambda field: field.label(u"ID").readonly()
EMAIL = lambda field: field.label(u"Adresse email").validate(validators.email)
EMAIL_REQUIRED = lambda field: EMAIL(field).required()
EMAIL_READONLY = lambda field: field.label(u"User").readonly()
LEVEL = lambda field, level_options: field.label(u"Level").dropdown(options=level_options)
FIRST_NAME = lambda field: field.label(u"Prénom")
LAST_NAME = lambda field: field.label(u"Nom")
PSEUDONYM = lambda field: field.label(u"Pseudo")
OLD_PASSWORD = lambda field: field.label(u"Ancien mot de passe").password().required().validate(custom_validators.old_password_validator)
NEW_PASSWORD = lambda field: field.label(u"Nouveau mot de passe").password().required().validate(validators.minlength(4))
NEW_PASSWORD_CONFIRM = lambda field: field.label(u"Nouveau mot de passe (confirmation)").password().required().validate(validators.minlength(4)).validate(custom_validators.new_password_validator)

def login_form(email=None, persistent=False):
    """ Simple form used to log in users """

    email = email or ""

    return web.form.Form(
              web.form.Textbox("email", description="Adresse email : ", value=email),
              web.form.Password("password", description="Mot de passe : "),
              web.form.Checkbox(u"Rester connecté", value="True", checked=persistent),
              web.form.Button("Se connecter", type="submit")                  
           )
    
def recover_password_form():
    """ Simple form used to recover passwords """

    return web.form.Form(
              web.form.Textbox("recover_password_email", description="Adresse email : "),
              web.form.Button("Envoyer", type="submit")                  
           )

class EditUsersGrid(Grid):
    """ Administration grid used to edit users """
    
    def __init__(self):
        
        # Grid initialization
        super(EditUsersGrid, self).__init__(User, User.all(order_by_clause=User.level))
        
        # Grid configuration
        level_options = sorted(User.Levels.values(), key=lambda level_component: level_component.value)
        
        inc = [
            ID_READONLY(self.id),
            EMAIL_READONLY(self.email),
            LEVEL(self.level, level_options)
        ]
        
        self.configure(include=inc)
        
class NewUserTokenFieldSet(CustomFieldSet):
    """ Administration form used to create user tokens """

    def __init__(self):
        
        # FieldSet initialization
        super(NewUserTokenFieldSet, self).__init__(UserToken)
        
        # FieldSet configuration
        level_options = sorted(
            [level_component for level, level_component in User.Levels.items() if level != User.BaseLevels.DISABLED],
            key=lambda level_component: level_component.value
        )
        
        inc = [
            LEVEL(self.level, level_options),
            EMAIL(self.email)
        ]
        
        self.configure(include=inc)

    def post_sync(self):
        
        # Creates the random token
        self.model.token = UserToken.generate_random_token(16)
        
        # Appends the token to the session
        config.orm.add(self.model)

class NewUserFieldSet(CustomFieldSet):
    """ User-facing form used to create users """
    
    def __init__(self, user_token):

        # FieldSet initialization
        super(NewUserFieldSet, self).__init__(User)
        self.user_token = user_token

        # FieldSet configuration
        self.append(Field("new_email", value=user_token.email))
        self.append(Field("new_password"))
        self.append(Field("new_password_confirm"))

        inc = [
            EMAIL_REQUIRED(self.new_email),
            FIRST_NAME(self.first_name),
            LAST_NAME(self.last_name),
            PSEUDONYM(self.pseudonym),
            NEW_PASSWORD(self.new_password),
            NEW_PASSWORD_CONFIRM(self.new_password_confirm)
        ]
        
        self.configure(include=inc)
        
    def post_sync(self):
        
        # Encodes & stores the password (entered by the user)
        self.model.password =  to_md5(self.new_password.value)
        
        # Stores the level (enclosed in the token, not visible by the user)
        self.model.level = self.user_token.level
        
        # Stores the email (enclosed in the token as well, but potentially overriden by the user)
        self.model.email = self.new_email.value
        
        # Appends the user to the session
        config.orm.add(self.model)
        
        # Expires the token since it should only be used once
        self.user_token.expire()
        
class EditUserFieldSet(FieldSet):
    """ User-facing form used to edit users """
    
    def __init__(self):
        
        # FieldSet initialization
        super(EditUserFieldSet, self).__init__(User)

        # FieldSet configuration
        inc = [
            PSEUDONYM(self.pseudonym),
            FIRST_NAME(self.first_name),
            LAST_NAME(self.last_name),
            EMAIL(self.email)
        ]
        
        self.configure(include=inc)

class EditPasswordFieldSet(CustomFieldSet):
    """ User-facing form used to edit passwords """
    
    def __init__(self):
        
        # FieldSet initialization
        super(EditPasswordFieldSet, self).__init__(User)

        # FieldSet configuration
        self.append(Field("old_password"))
        self.append(Field("new_password"))
        self.append(Field("new_password_confirm"))
        
        inc = [
            OLD_PASSWORD(self.old_password),
            NEW_PASSWORD(self.new_password),
            NEW_PASSWORD_CONFIRM(self.new_password_confirm)
        ]
        
        self.configure(include=inc)
        
    def post_sync(self):
        
        # Encodes & stores the password (entered by the user)
        self.model.password =  to_md5(self.new_password.value)
        
class NewPasswordFieldSet(CustomFieldSet):
    """ User-facing form used to create passwords """
    
    def __init__(self, password_token=None):

        # FieldSet initialization
        super(NewPasswordFieldSet, self).__init__(User)
        self.password_token = password_token

        # FieldSet configuration
        self.append(Field("new_password"))
        self.append(Field("new_password_confirm"))

        inc = [
            NEW_PASSWORD(self.new_password),
            NEW_PASSWORD_CONFIRM(self.new_password_confirm)
        ]
        
        self.configure(include=inc)
        
    def post_sync(self):
        
        # Encodes & stores the password (entered by the user)
        self.model.password =  to_md5(self.new_password.value)

        # Expires the token since it should only be used once
        self.password_token.expire()
