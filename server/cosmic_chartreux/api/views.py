from flask import Flask, g, request
from flask_restplus import Api, Resource

from cosmic_chartreux.db import db
from cosmic_chartreux.models import Disk, DiskStatistic
from cosmic_chartreux.schema import DiskSchema, QueryParamsSchema, StatisticSchema
from cosmic_chartreux.utils import agent_login_required
from itertools import groupby

api = Api(prefix="/api")


@api.route("/auth/login/")
class Auth(Resource):
    def post(self):
        return {"access": ""}


@api.route("/disks/")
class DisksListCreate(Resource):
    def get(self):
        query_params = QueryParamsSchema().dump(request.args)

        query = Disk.query
        count = query.count()

        query = query.limit(query_params["limit"]).offset(query_params["offset"])

        results = DiskSchema().dump(query, many=True)
        return {"count": count, "results": results}

    @agent_login_required
    def post(self):
        agent_id = g.agent_id

        group_func = lambda item: item["mountpoint"]
        request.json.sort(key=group_func)
        for mountpoint, data in groupby(request.json, group_func):
            data = list(data)
            disk = Disk.query.filter(
                Disk.mountpoint == mountpoint, Disk.agent_id == agent_id
            ).first()

            if disk is None:
                disk = Disk(agent_id=agent_id, mountpoint=mountpoint)
                db.session.add(disk)
                db.session.commit()

            statistics = []
            for item in data:
                item.pop("mountpoint", "")
                statistics.append(DiskStatistic(disk_id=disk.id, **item))

            db.session.add_all(statistics)
            db.session.commit()


@api.route("/disks/<int:disk_id>/statistics/")
class DiskStatisticResource(Resource):
    def get(self, *args, **kwargs):
        query_params = QueryParamsSchema().dump(request.args)
        query = DiskStatistic.query.filter(DiskStatistic.disk_id == kwargs["disk_id"])
        count = query.count()
        query = query.limit(query_params["limit"]).offset(query_params["offset"]).all()

        results = StatisticSchema().dump(query, many=True)
        return {"count": count, "results": results}


def init_api(app: Flask):
    api.init_app(app)
