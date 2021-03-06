# -*- coding: utf-8 -*-

from app.utils import formatting
from formalchemy import FieldSet
from formalchemy.fields import Field
from formalchemy.tables import Grid
import datetime
import operator

def create_generic_date_field(name, attr_getter, dt_format, today_by_default=True):
    """ Instanciates a generic date field associated with the format passed as a parameter """
    
    def value(model):
        """ Returns the model date or today's date """
        default_date = datetime.date.today() if today_by_default else None
        dt = model and attr_getter(model) or default_date
        return dt and formatting.format_date(dt, dt_format)
    
    return Field(name=name, value=value)

def create_date_field(name, model_date_attribute, dt_format, today_by_default=True):
    """ Instanciates a standard date field associated with the format passed as a parameter """
    return create_generic_date_field(name, operator.attrgetter(model_date_attribute), dt_format, today_by_default)

class CustomGrid(Grid):
    """ Used when simple FormAlchemy grids are not sufficient
    (i.e. when the synchronization process should be customized)
    
    A 'post_sync' method, responsible for non-standard synchronization & persistence,
    should be defined when inheriting of this class.
    """
    
    def __init__(self, cls, instances):
        super(CustomGrid, self).__init__(cls, instances)
    
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
        super(CustomFieldSet, self).__init__(model)

    def sync(self):
        
        # Standard synchronization of the fields
        for field in self.render_fields.itervalues():
            field.sync()
        
        # Customized synchronization & persistence (defined by the child class)
        self.post_sync()