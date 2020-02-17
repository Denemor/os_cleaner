from flask import Flask, g, request
from flask_restplus import Api, Resource

from os_cleaner.db import db
from os_cleaner.models import Disk, Tasks, Agent
from os_cleaner.schema import DiskSchema, QueryParamsSchema, TasksSchema, AgentSchema, AllSchema
from os_cleaner.utils import agent_login_required

api = Api(prefix="/api")


@api.route("/auth/login/")
class Auth(Resource):
    def post(self):
        return {"access": ""}


@api.route("/disk-statistics/")
class DisksListCreate(Resource):
    def get(self):
        query_params = QueryParamsSchema().dump(request.args)

        query = Disk.query
        count = query.count()

        query = query.limit(query_params["limit"]).offset(query_params["offset"])

        schema = DiskSchema().dump(query, many=True)
        return {"count": count, "results": schema}

    @agent_login_required
    def post(self):
        agent_id = g.agent_id

        for item in request.json:
            db.session.add(Disk(agent_id=agent_id, **item))
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
            db.session.add(Tasks(agent_id = agent_id, **item))
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
