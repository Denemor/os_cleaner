from flask import Flask, g, request
from flask_restplus import Api, Resource

from os_cleaner.db import db
from os_cleaner.models import Disks, Tasks, Agent
from os_cleaner.schema import DisksSchema, QueryParamsSchema, TasksSchema, AgentSchema, AllSchema
from os_cleaner.utils import agent_login_required

api = Api(prefix="/api")


@api.route("/auth/login/")
class Auth(Resource):
    def post(self):
        return {"access": ""}

@api.route("/agent/")
class Host(Resource):

    def get(self):
        query_params = QueryParamsSchema().dump(request.args)

        query = Agent.query
        count = query.count()

        query = query.limit(query_params["limit"]).offset(query_params["offset"])

        schema = AgentSchema().dump(query, many=True)

        return {"count": count, "results": schema}

    def post(self):

        for item in request.json:
            db.session.add(Agent(**item['data']))
            db.session.commit()

@api.route("/disks/")
class DisksListCreate(Resource):
    def get(self):
        query_params = QueryParamsSchema().dump(request.args)

        query = Disks.query
        count = query.count()

        query = query.limit(query_params["limit"]).offset(query_params["offset"])

        schema = DisksSchema().dump(query, many=True)
        return {"count": count, "results": schema}

    @agent_login_required
    def post(self):
        agent_id = g.agent_id

        for item in request.json[0]['data']:
            db.session.add(Disks(agent_id=agent_id, **item))
            db.session.commit()


@api.route("/tasks/")
class TasksResult(Resource):

    def get(self):
        query_params = QueryParamsSchema().dump(request.args)

        query = Tasks.query
        count = query.count()

        query = query.limit(query_params["limit"]).offset(query_params["offset"])

        schema = TasksSchema().dump(query, many=True)
        return {"count": count, "results": schema}

    @agent_login_required
    def post(self):
        agent_id = g.agent_id

        for item in request.json:
            db.session.add(Tasks(agent_id = agent_id, **item['data']))
            db.session.commit()


@api.route("/all/")
class All(Resource):

    def get(self):
        query_params = QueryParamsSchema().dump(request.args)

        query = Agent.query
        count = query.count()

        query = query.limit(query_params["limit"]).offset(query_params["offset"])

        schema = AllSchema().dump(query, many=True)
        return {"count": count, "results": schema}


def init_api(app: Flask):
    api.init_app(app)
