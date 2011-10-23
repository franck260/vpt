# -*- coding: utf-8 -*-

from app.utils import formatting
from formalchemy import FieldSet
from formalchemy.fields import Field
from formalchemy.tables import Grid
import datetime

def create_date_field(name, model_date_attribute, dt_format):
    """ Instanciates a standard date field associated with the format passed as a parameter """
    
    def value(model):
        """ Returns the model date or today's date """
        dt = model and getattr(model, model_date_attribute) or datetime.date.today()
        return formatting.format_date(dt, dt_format)
    
    return Field(name=name, value=value)

class CustomGrid(Grid):
    """ Used when simple FormAlchemy grids are not sufficient
    (i.e. when the synchronization process should be customized)
    
    A 'post_sync' method, responsible for non-standard synchronization & persistence,
    should be defined when inheriting of this class.
    """
    
    def __init__(self, cls, instances):
        Grid.__init__(self, cls, instances)
    
    def sync_one(self, row):

        self._set_active(row)

        # Standard synchronization of the fields
        for field in self.render_fields.itervalues():
            field.sync()

        # Customized synchronization & persistence (defined by the child class)
        self.post_sync()
        
class CustomFieldSet(FieldSet):
    """ Used when simple FormAlchemy fieldsets are not sufficient
    (i.e. when the synchronization process should be customized)
    
    A 'post_sync' method, responsible for non-standard synchronization & persistence,
    should be defined when inheriting of this class.
    """

    def __init__(self, model):
        FieldSet.__init__(self, model)

    def sync(self):
        
        # Standard synchronization of the fields
        for field in self.render_fields.itervalues():
            field.sync()
        
        # Customized synchronization & persistence (defined by the child class)
        self.post_sync()