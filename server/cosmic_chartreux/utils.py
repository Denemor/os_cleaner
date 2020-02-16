from flask import request, g

from cosmic_chartreux.db import db
from cosmic_chartreux.models import Agent


def agent_login_required(func):
    def wrapped(*args, **kwargs):
        agent = Agent.query.filter(Agent.ipv4 == request.remote_addr).first()
        if agent is None:
            db.session.add(Agent(ipv4=request.remote_addr))
            db.session.commit()
            agent = Agent.query.filter(Agent.ipv4 == request.remote_addr).first()

        g.agent_id = agent.id
        return func(*args, **kwargs)

    return wrapped
