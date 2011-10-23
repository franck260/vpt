# -*- coding: utf-8 -*-

""" Administration forms used to edit seasons """

from app.forms import custom_validators
from app.models import Season
from formalchemy import FieldSet
from formalchemy.tables import Grid

# Patterns & formats used by the validators
YEAR_PATTERN = r"^20\d{2}$"

# Lambda methods used to enrich the fields with labels & validators
ID_READONLY = lambda field: field.label(u"ID").readonly()
START_YEAR = lambda field: field.label(u"Année de début").validate(custom_validators.year_validator(YEAR_PATTERN))
END_YEAR = lambda field: field.label(u"Année de fin").validate(custom_validators.year_validator(YEAR_PATTERN)).validate(custom_validators.year_delta_validator)

class SeasonsGrid(Grid):
    """ FormAlchemy grid used to edit seasons """
    
    def __init__(self):
        
        # Grid initialization
        Grid.__init__(self, Season, Season.all(order_by_clause=Season.start_year)) #@UndefinedVariable
        
        # Grid configuration
        inc = [ID_READONLY(self.id), START_YEAR(self.start_year), END_YEAR(self.end_year)]
        self.configure(include=inc)

class SeasonFieldSet(FieldSet):
    """ FormAlchemy form used to edit seasons """

    def __init__(self):

        # FieldSet initialization
        FieldSet.__init__(self, Season)
        
        # FieldSet configuration
        inc = [START_YEAR(self.start_year), END_YEAR(self.end_year)]
        self.configure(include=inc)