# -*- coding: utf-8 -*-

from app.models import Season, Tournament, News, Poll
from app.utils import session
from web import config

class Index :
    
    @session.login_required
    def GET(self):
        
        next_tournament = Tournament.next_tournament()
        all_polls = Poll.all()
        open_polls = filter(lambda poll: not poll.expired, all_polls)
        expired_polls = filter(lambda poll: poll.expired, all_polls)
        
        return config.views.layout(config.views.index(next_tournament, open_polls, expired_polls, News.all()), Season.all())

    
