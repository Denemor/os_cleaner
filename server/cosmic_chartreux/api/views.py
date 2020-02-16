from flask import Flask, g, request
from flask_restplus import Api, Resource

from cosmic_chartreux.db import db
from cosmic_chartreux.models import Disk
from cosmic_chartreux.schema import DiskSchema, QueryParamsSchema
from cosmic_chartreux.utils import agent_login_required

api = Api(prefix="/api")


@api.route("/auth/login/")
class Auth(Resource):
    def post(self):
        return {"access": ""}


@api.route("/disk-statictics/")
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


@api.route("/disk-statictics/")
class DisksRetrieve(Resource):
    def get(self):
        pass


def init_api(app: Flask):
    api.init_app(app)
