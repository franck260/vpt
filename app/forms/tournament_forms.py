# -*- coding: utf-8 -*-

""" Administration forms used to edit tournaments """

from app.forms import custom_validators, CustomGrid, CustomFieldSet, \
    create_date_field
from app.models import Season, Tournament, Result, User
from app.utils import formatting
from formalchemy.fields import Field
from formalchemy.tables import Grid
import datetime

# Patterns & formats used by the validators
DT_FORMAT = "%d/%m/%Y"

# Lambda methods used to enrich the fields with labels & validators
SEASON = lambda field, season_options: field.label(u"Saison").dropdown(options=season_options) 
SEASON_READONLY = lambda field: field.label(u"Saison").readonly()
POSITION_READONLY = lambda field: field.label(u"Position").readonly()
FORMATTED_DT = lambda field: field.label(u"Date").validate(custom_validators.tournament_dt_validator(DT_FORMAT))
BUYIN = lambda field: field.label(u"Buyin")

class EditTournamentsGrid(CustomGrid):
    """ Administration grid used to edit tournaments """
    
    def __init__(self):

        # Grid initialization
        super(EditTournamentsGrid, self).__init__(Tournament, Tournament.all(order_by_clause=Tournament.tournament_dt)) #@UndefinedVariable
        
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
        
class NewTournamentFieldSet(CustomFieldSet):
    """ Administration form used to create tournaments """

    def __init__(self):
        
        # FieldSet initialization
        super(NewTournamentFieldSet, self).__init__(Tournament)
        
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

class EditResultsGrid(Grid):
    """ Administration grid used to edit tournament results """
        
    def __init__(self):
        
        super(EditResultsGrid, self).__init__(Result)
        
        STATUS_OPTIONS = [(u"Présent", Result.STATUSES.P), (u"Absent", Result.STATUSES.A), (u"Peut-être", Result.STATUSES.M)]
        RANK_OPTIONS = [(u"", None)] + [(formatting.append(i, formatting.to_rank), i) for i in range(1, len(User.all()))]

        self.append(Field("pseudonym", value=lambda result: result.user.pseudonym))
        
        inc = [
            self.pseudonym.label(u"Joueur").readonly(),
            self.status.label(u"Statut").dropdown(options=STATUS_OPTIONS),
            self.buyin.label(u"Mise").validate(custom_validators.required_for([Result.STATUSES.P])).validate(custom_validators.forbidden_for([Result.STATUSES.M, Result.STATUSES.A])),
            self.rank.label(u"Classement").dropdown(options=RANK_OPTIONS).validate(custom_validators.forbidden_for([Result.STATUSES.M, Result.STATUSES.A])),
            self.profit.label(u"Gain").validate(custom_validators.forbidden_for([Result.STATUSES.M, Result.STATUSES.A])),
        ]
        
        self.configure(include=inc)