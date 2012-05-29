# -*- coding: utf-8 -*-

""" Administration forms used to edit polls """

from app import utils
from app.forms import custom_validators, CustomFieldSet, create_date_field, \
    CustomGrid, create_generic_date_field
from app.models import Poll
from app.utils import formatting
from formalchemy.fields import Field
from web import config
import datetime

# Patterns & formats used by the validators
DT_FORMAT = "%d/%m/%Y"

# Lambda methods used to enrich the fields with labels & validators
TITLE = lambda field: field.label(u"Titre")
FORMATTED_START_DT = lambda field: field.label(u"Date de début").required().validate(custom_validators.dt_validator(DT_FORMAT))
FORMATTED_END_DT = lambda field: field.label(u"Date de fin").validate(custom_validators.dt_validator(DT_FORMAT)).validate(custom_validators.poll_dt_range_validator(DT_FORMAT))
FORMATTED_POSSIBLE_DATES_READONLY = lambda field: field.label(u"Choix").readonly()
FORMATTED_POSSIBLE_DT = lambda field, i: (field.required() if i<=2 else field).label(u"Choix %s" % i)                                                   \
                                                                              .validate(custom_validators.dt_validator(DT_FORMAT))                      \
                                                                              .validate(custom_validators.poll_choice_dt_uniqueness_validator)          \
                                                                              .validate(custom_validators.poll_dt_range_validator(DT_FORMAT))

class EditPollsGrid(CustomGrid):
    """ Administration grid used to edit polls """
    
    def __init__(self):
        
        # Grid initialization
        super(EditPollsGrid, self).__init__(Poll, Poll.all(joined_attrs=["choices"])) #@UndefinedVariable

        # Creation of customized date fields to edit the poll dates
        self.append(create_date_field("formatted_start_dt", "start_dt", DT_FORMAT, today_by_default=True))
        self.append(create_date_field("formatted_end_dt", "end_dt", DT_FORMAT, today_by_default=False))
        self.append(
            Field(
                name="formatted_possible_dates",
                value=lambda model: "[%s]" % ",".join([formatting.format_date(dt, DT_FORMAT) for dt in model.possible_dates])
            )
        )
        
        # Grid configuration
        inc = [
            TITLE(self.title),
            FORMATTED_START_DT(self.formatted_start_dt),
            FORMATTED_END_DT(self.formatted_end_dt),
            FORMATTED_POSSIBLE_DATES_READONLY(self.formatted_possible_dates)
        ]
        self.configure(include=inc)
        
    def post_sync(self):
        
        # Parses the entered dates and updates the model
        self.model.start_dt = datetime.datetime.strptime(self.formatted_start_dt.value, DT_FORMAT).date()
        self.model.end_dt = self.formatted_end_dt.value and datetime.datetime.strptime(self.formatted_end_dt.value, DT_FORMAT).date()

class NewPollFieldSet(CustomFieldSet):
    """ Administration form used to create polls """
    
    @property    
    def possible_date_fields_names(self):
        return ["formatted_%s_possible_dt" % index for index in ("first", "second", "third", "fourth")]
    
    @property
    def possible_date_fields(self):
        return [getattr(self, name) for name in self.possible_date_fields_names]
    
    def __init__(self):

        # FieldSet initialization
        super(NewPollFieldSet, self).__init__(Poll)
        
        # Creation of customized date fields to edit the poll dates
        self.append(create_date_field("formatted_start_dt", "start_dt", DT_FORMAT, today_by_default=True))
        self.append(create_date_field("formatted_end_dt", "end_dt", DT_FORMAT, today_by_default=False))
        [self.append(
            create_generic_date_field(
                name,
                lambda model: utils.safeget(model.possible_dates, i),
                DT_FORMAT,
                today_by_default=False
            )) for i, name in enumerate(self.possible_date_fields_names)]
        
        # FieldSet configuration
        inc = [
            TITLE(self.title),
            FORMATTED_START_DT(self.formatted_start_dt),
            FORMATTED_END_DT(self.formatted_end_dt),
        ] + [FORMATTED_POSSIBLE_DT(field, i) for i, field in enumerate(self.possible_date_fields, start=1)]
            
        self.configure(include=inc)
        
    def post_sync(self):
        
        # Parses the entered dates and updates the model
        self.model.start_dt = datetime.datetime.strptime(self.formatted_start_dt.value, DT_FORMAT).date()
        self.model.end_dt = self.formatted_end_dt.value and datetime.datetime.strptime(self.formatted_end_dt.value, DT_FORMAT).date()
        self.model.possible_dates = [datetime.datetime.strptime(field.value, DT_FORMAT).date() for field in self.possible_date_fields if field.value is not None]
        
        # Appends the poll to the session
        config.orm.add(self.model)