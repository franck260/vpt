# -*- coding: utf-8 -*-

""" Administration forms used to edit sessions """

from app.forms import create_date_field
from app.models import Session
from formalchemy.fields import Field
from formalchemy.tables import Grid
from web import config

# Patterns & formats used by the validators
DT_FORMAT = "%d/%m/%Y"

# Lambda methods used to enrich the fields with labels & validators
SESSION_ID_READONLY = lambda field: field.label(u"Session ID").readonly()
FORMATTED_ATIME_READONLY = lambda field: field.label(u"Atime").readonly()
FORMATTED_DATA_READONLY = lambda field: field.label(u"Data").readonly()

class EditSessionsGrid(Grid):
    """ Administration grid used to edit sessions """
    
    def __init__(self):
        
        # Grid initialization
        super(EditSessionsGrid, self).__init__(Session, Session.all())
        
        # Creation of a customized date field to view the session's date
        self.append(create_date_field("formatted_atime", "atime", DT_FORMAT))
        
        # Creation of a customized field to view the session's data
        self.append(
            Field(
                name="formatted_data",
                value=lambda model: "{%s}" % ",".join(["%s:%s" % (k, v) for k, v in config.session_manager.session_handler.store.decode(model.data).items() if k != "session_id"])
            )
        )
        
        # Grid configuration
        inc = [
            FORMATTED_ATIME_READONLY(self.formatted_atime),
            FORMATTED_DATA_READONLY(self.formatted_data),
            SESSION_ID_READONLY(self.session_id)
        ]
        
        self.configure(include=inc)
