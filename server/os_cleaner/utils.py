from flask import request, g

from os_cleaner.db import db
from os_cleaner.models import Agent


def agent_login_required(func):
    def wrapped(*args, **kwargs):
        agent = Agent.query.filter(Agent.ip == request.remote_addr).first()
        if agent is None:
            db.session.add(Agent(ip=request.remote_addr))
            db.session.commit()
            agent = Agent.query.filter(Agent.ip == request.remote_addr).first()

        g.agent_id = agent.id
        return func(*args, **kwargs)

    return wrapped
