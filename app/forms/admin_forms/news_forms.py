# -*- coding: utf-8 -*-

""" Administration forms used to edit news """

from app.forms import custom_validators
from app.forms.admin_forms import CustomGrid, CustomFieldSet, create_date_field
from app.models import News
from web import config
import datetime

# Patterns & formats used by the validators
DT_FORMAT = "%d/%m/%Y"

# Lambda methods used to enrich the fields with labels & validators
FORMATTED_DT = lambda field: field.label(u"Date").validate(custom_validators.dt_validator(DT_FORMAT))
NEWS = lambda field: field.label(u"News")

class NewsGrid(CustomGrid):
    """ FormAlchemy grid used to edit news """
    
    def __init__(self):

        # Grid initialization
        CustomGrid.__init__(self, News, News.all()) #@UndefinedVariable
        
        # Creation of a customized date field to edit the news' date
        self.append(create_date_field("formatted_news_dt", "news_dt", DT_FORMAT))
        
        # Grid configuration
        inc = [FORMATTED_DT(self.formatted_news_dt), NEWS(self.news)] 
        self.configure(include=inc)
        
    def post_sync(self):
        
        # Parses the entered date and updates the model
        self.model.news_dt = datetime.datetime.strptime(self.formatted_news_dt.value, DT_FORMAT).date()
        
class NewsFieldSet(CustomFieldSet):
    """ FormAlchemy form used to edit tournaments """

    def __init__(self):
        
        # FieldSet initialization
        CustomFieldSet.__init__(self, News)
        
        # Creation of a customized date field to edit the news' date
        self.append(create_date_field("formatted_news_dt", "news_dt", DT_FORMAT))
        
        # FieldSet configuration
        inc = [FORMATTED_DT(self.formatted_news_dt), NEWS(self.news)] 
        self.configure(include=inc)

    def post_sync(self):
        
        # Parses the entered date and updates the model
        self.model.news_dt = datetime.datetime.strptime(self.formatted_news_dt.value, DT_FORMAT).date()
        
        # Appends the news to the session
        config.orm.add(self.model)
        
