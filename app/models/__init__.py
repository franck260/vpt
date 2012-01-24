# -*- coding: utf-8 -*-

# All models are imported here in order to be accessed through the root package
from app.models.users import User
from app.models.tokens import UserToken, PasswordToken
from app.models.comments import TournamentComment
from app.models.results import Result
from app.models.tournaments import Tournament
from app.models.seasons import Season
from app.models.sessions import Session
from app.models.news import News


