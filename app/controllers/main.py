# -*- coding: utf-8 -*-

from app.models import News, Poll
from app.models.tournaments import pending_tournaments
from app.utils import session
from web import config

class Index :
    
    @session.login_required
    def GET(self):
        
        open_polls = filter(lambda poll: not poll.expired, Poll.all())
        
        return config.views.layout(
            config.views.index(
                pending_tournaments(),
                open_polls,
                News.all()
            )
        )
