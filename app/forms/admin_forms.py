# -*- coding: utf-8 -*-

""" Forms used by the generic administration controller """

from app.forms import custom_validators
from app.models import Season, Tournament
from app.utils import formatting
from formalchemy import FieldSet
from formalchemy.fields import Field
from formalchemy.tables import Grid
import datetime

# Patterns & formats used by the validators
YEAR_PATTERN = r"^20\d{2}$"
DT_FORMAT = "%d/%m/%Y"
# DT_PATTERN = r"^\d{2}/\d{2}/\d{4}$"


def formatted_tournament_dt_field():
    """ Instanciates a formatted date field used by the tournaments """
    
    def value(model):
        tournament_dt = model and model.tournament_dt or datetime.date.today()
        return formatting.format_date(tournament_dt, DT_FORMAT)
    
    return Field("formatted_tournament_dt", value=value)

# Lambda methods to enrich the fields used by the fieldsets & the grids
ID_READONLY = lambda id: id.label(u"ID").readonly()
SEASON_START_YEAR = lambda start_year: start_year.label(u"Année de début").validate(custom_validators.year_validator(YEAR_PATTERN))
SEASON_END_YEAR = lambda end_year: end_year.label(u"Année de fin").validate(custom_validators.year_validator(YEAR_PATTERN)).validate(custom_validators.year_delta_validator)
TOURNAMENT_SEASON = lambda season_id, season_options: season_id.label(u"Saison").dropdown(options=season_options) 
TOURNAMENT_SEASON_READONLY = lambda season_id: season_id.label(u"Saison").readonly()
TOURNAMENT_POSITION_READONLY = lambda position: position.label(u"Position").readonly()
TOURNAMENT_FORMATTED_DT = lambda formatted_tournament_dt: formatted_tournament_dt.label(u"Date").validate(custom_validators.dt_validator(DT_FORMAT))
TOURNAMENT_FORMATTED_DT_READONLY = lambda formatted_tournament_dt: TOURNAMENT_FORMATTED_DT(formatted_tournament_dt).readonly()
TOURNAMENT_BUYIN = lambda buyin: buyin.label(u"Buyin")

class SeasonsGrid(Grid):
    """ FormAlchemy grid used to edit seasons """
    
    def __init__(self):
        
        Grid.__init__(self, Season, Season.all(order_by_clause=Season.start_year)) #@UndefinedVariable
        inc = [ID_READONLY(self.id), SEASON_START_YEAR(self.start_year), SEASON_END_YEAR(self.end_year)]
        self.configure(include=inc)

class SeasonFieldSet(FieldSet):
    """ FormAlchemy form used to edit seasons """

    def __init__(self):
        
        FieldSet.__init__(self, Season)
        inc = [SEASON_START_YEAR(self.start_year), SEASON_END_YEAR(self.end_year)]
        self.configure(include=inc)

class TournamentsGrid(Grid):
    """ FormAlchemy grid used to edit tournaments """
    
    def __init__(self):
        
        Grid.__init__(self, Tournament, Tournament.all(order_by_clause=Tournament.tournament_dt)) #@UndefinedVariable
        self.append(formatted_tournament_dt_field())
        inc = [TOURNAMENT_SEASON_READONLY(self.season_id), TOURNAMENT_POSITION_READONLY(self.position), TOURNAMENT_FORMATTED_DT_READONLY(self.formatted_tournament_dt), TOURNAMENT_BUYIN(self.buyin)] 
        self.configure(include=inc)
        
class TournamentFieldSet(FieldSet):
    """ FormAlchemy form used to edit tournaments """

    def sync(self):
        
        # Manual update of the model since the tournament should be appended to the season and not just be added to the session
        # See the collection_class used at the Season level to store tournaments
        for field in self.render_fields.itervalues():
            field.sync()
        
        # Parses the entered date and updates the model
        self.model.tournament_dt = datetime.datetime.strptime(self.formatted_tournament_dt.value, DT_FORMAT).date() 
        
        # Appends the tournament in the end of the collection (i.e. in last position)
        season = Season.get(self.model.season_id)
        season.tournaments.append(self.model)
        
        # Reshuffles the tournaments so that they are still ordered by date
        season.reorder_tournaments()

    def __init__(self):
        
        FieldSet.__init__(self, Tournament)
        self.append(formatted_tournament_dt_field())
        season_options = [("Saison %s (%s - %s)" %(season.id, season.start_year, season.end_year), season.id) for season in Season.all()]
        inc = [TOURNAMENT_SEASON(self.season, season_options), TOURNAMENT_FORMATTED_DT(self.formatted_tournament_dt), TOURNAMENT_BUYIN(self.buyin)]
        self.configure(include=inc)
        

