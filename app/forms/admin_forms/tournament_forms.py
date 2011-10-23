# -*- coding: utf-8 -*-

""" Administration forms used to edit news """

from app.forms import custom_validators
from app.forms.admin_forms import CustomGrid, CustomFieldSet, create_date_field
from app.models import Season, Tournament
import datetime

# Patterns & formats used by the validators
DT_FORMAT = "%d/%m/%Y"

# Lambda methods used to enrich the fields with labels & validators
SEASON = lambda field, season_options: field.label(u"Saison").dropdown(options=season_options) 
SEASON_READONLY = lambda field: field.label(u"Saison").readonly()
POSITION_READONLY = lambda field: field.label(u"Position").readonly()
FORMATTED_DT = lambda field: field.label(u"Date").validate(custom_validators.tournament_dt_validator(DT_FORMAT))
BUYIN = lambda field: field.label(u"Buyin")

class TournamentsGrid(CustomGrid):
    """ FormAlchemy grid used to edit tournaments """
    
    def __init__(self):

        # Grid initialization
        CustomGrid.__init__(self, Tournament, Tournament.all(order_by_clause=Tournament.tournament_dt)) #@UndefinedVariable
        
        # Creation of a customized date field to edit the tournaments' date
        self.append(create_date_field("formatted_tournament_dt", "tournament_dt", DT_FORMAT))
        
        # Grid configuration
        inc = [SEASON_READONLY(self.season_id), POSITION_READONLY(self.position), FORMATTED_DT(self.formatted_tournament_dt), BUYIN(self.buyin)] 
        self.configure(include=inc)
        
    def post_sync(self):
        
        # Parses the entered date and updates the model
        self.model.tournament_dt = datetime.datetime.strptime(self.formatted_tournament_dt.value, DT_FORMAT).date()
        
        # Reshuffles the tournaments so that they are still ordered by date
        Season.get(self.model.season_id).reorder_tournaments()
        
class TournamentFieldSet(CustomFieldSet):
    """ FormAlchemy form used to edit tournaments """

    def __init__(self):
        
        # FieldSet initialization
        CustomFieldSet.__init__(self, Tournament)
        
        # Creation of a customized date field to edit the tournament's date
        self.append(create_date_field("formatted_tournament_dt", "tournament_dt", DT_FORMAT))
        
        # FieldSet configuration
        season_options = [("Saison %s (%s - %s)" %(season.id, season.start_year, season.end_year), season.id) for season in Season.all()]
        inc = [SEASON(self.season, season_options), FORMATTED_DT(self.formatted_tournament_dt), BUYIN(self.buyin)]
        self.configure(include=inc)

    def post_sync(self):
        
        # Parses the entered date and updates the model
        self.model.tournament_dt = datetime.datetime.strptime(self.formatted_tournament_dt.value, DT_FORMAT).date() 
        
        # Appends the tournament in the end of the collection (i.e. in last position)
        # The tournament should be appended to the season and not just be added to the session :
        # see the collection_class used at the Season level to store tournaments
        season = Season.get(self.model.season_id)
        season.tournaments.append(self.model)
        
        # Reshuffles the tournaments so that they are still ordered by date
        season.reorder_tournaments()
