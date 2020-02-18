from flask import request, g

from os_cleaner.db import db
from os_cleaner.models import Agent


def agent_login_required(func):
    def wrapped(*args, **kwargs):
        agent = Agent.query.filter(Agent.hostname == request.json[0]['metadata']['hostname']).first
        if agent() is None:
            data = request.json[0]['metadata']
            db.session.add(Agent(hostname=data['hostname'], ip=data['ip']))
            db.session.commit()
            agent = Agent.query.filter(Agent.hostname == request.json[0]['metadata']['hostname']).first

        g.agent_id = agent().id
        return func(*args, **kwargs)

    return wrapped
