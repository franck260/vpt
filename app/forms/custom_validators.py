# -*- coding: utf-8 -*-

""" Custom validators used by the FormAlchemy forms """

from app.models import Season
from app.utils.session import to_md5
from formalchemy import validators
import datetime
import re

def old_password_validator(value, field):
    
    if field.parent.model.password != to_md5(value):
        raise validators.ValidationError("Invalid value")
    
def new_password_validator(value, field):
    
    if field.parent.new_password.value != value:
        raise validators.ValidationError("Passwords do not match")

def required_for(statuses):
    
    @validators.accepts_none
    def f(value, field):
        status = field.parent.to_dict(with_prefix=False)["status"]
        if status in statuses and value is None:
            raise validators.ValidationError("Mandatory value (status=%s)" %status)
        
    return f

def forbidden_for(statuses):
    
    @validators.accepts_none
    def f(value, field):
        status = field.parent.to_dict(with_prefix=False)["status"]
        if status in statuses and value is not None:
            raise validators.ValidationError("Forbidden value (status=%s)" %status)
        
    return f

def year_validator(year_pattern):
    
    def f(value, field):
        if not re.match(year_pattern, str(value)):
            raise validators.ValidationError("Year does not match %s" %year_pattern)
        
    return f

def year_delta_validator(value, field):
    
    if value - field.parent.start_year.value != 1:
        raise validators.ValidationError("1 != end_year - start_year")
    
    
def dt_validator(dt_format):
    
    def f(value, field):
        
        # Step 1 : general format check with the standard library
        try:
            year = datetime.datetime.strptime(value, dt_format).year
        except ValueError:
            raise validators.ValidationError("Date does not match format %s" %dt_format)
        
        # Step 2 : year check
        selected_season = Season.get(field.parent.season_id.value)
        allowed_years = (selected_season.start_year, selected_season.end_year)
        if not year in allowed_years:
            raise validators.ValidationError("Year should be %s" % " or ".join(map(str,allowed_years))) 
        
    return f
 
    