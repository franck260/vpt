# -*- coding: utf-8 -*-

from app.models import Poll
from app.notifications import notify_via_email, Events
from app.utils import session, http
from web import config
import web

class View:
    
    @session.login_required
    def GET(self, id):
        
        # Loads the poll
        poll = Poll.get(int(id), joined_attrs=["choices", "votes_by_user", "comments"])
        
        if poll is None:
            raise web.notfound()
        
        return config.views.layout(
                   config.views.poll(
                        poll,
                        config.views.poll_header(poll),
                        config.views.poll_vote_unit(poll),
                        config.views.poll_votes(poll),
                        config.views.comments(poll, config.views.comment)
                    ),
                    config.views.ui_head()
                )

class Vote:

    @session.login_required
    @http.jsonify
    def POST(self):
        
        # Reads the HTTP request parameters
        input = web.input(poll_id=None, poll_user_choices=[])
        poll_id = input.poll_id
        poll_user_choices = input.poll_user_choices

        # Loads the poll
        if poll_id is None:
            raise web.notfound() 

        poll = Poll.get(int(poll_id), joined_attrs=["choices", "votes_by_user"])

        if poll is None:
            raise web.notfound()
        
        # Passes the user's choices to the model
        try:
            
            # Parses the choice numbers & makes sure they're valid
            poll_user_choices = map(int, poll_user_choices)
            if any(i not in range(len(poll.choices)) for i in poll_user_choices):
                raise ValueError(u"Un des entiers passes a la methode /poll/vote n'est pas compris dans l'intervalle %s" % range(len(poll.choices)))
            
            # Determines if it's the first vote ever in the poll
            someone_already_voted = poll.has_votes
            
            # Determines if it's the first vote for the user
            user_already_voted = config.session_manager.user in poll.choices_by_user
            
            # Actual vote action for the user
            poll_vote = poll.vote(config.session_manager.user, [poll.choices[i] for i in poll_user_choices])

            # Registers an email notification
            http.register_hook(lambda: notify_via_email(poll_vote, Events.MODIFIED if user_already_voted else Events.NEW))

            return dict(
                data=config.views.poll_votes(poll, highlight_user=config.session_manager.user if someone_already_voted else None),
                partial=someone_already_voted
            )
            
        except ValueError as exception:
            raise web.forbidden(exception)
        
class Comment:
    
    @session.login_required
    def POST(self):
        
        # Reads the HTTP request parameters
        input = web.input()
        poll_id = input.poll_id
        comment = input.comment

        # Loads the poll
        if poll_id is None:
            raise web.notfound() 

        poll = Poll.get(int(poll_id), joined_attrs=["comments"])

        if poll is None:
            raise web.notfound()
        
        # Appends the comment
        poll_comment = poll.add_comment(config.session_manager.user, comment)
        
        # Registers an email notification
        http.register_hook(lambda: notify_via_email(poll_comment, Events.NEW))

        # Returns the dictionary
        return config.views.comment(poll_comment)
