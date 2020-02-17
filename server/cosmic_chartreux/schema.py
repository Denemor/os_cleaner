from marshmallow import Schema
from marshmallow import fields


class QueryParamsSchema(Schema):
    limit = fields.Integer(default=20)
    offset = fields.Integer(default=0)


class AgentSchema(Schema):
    id = fields.Integer()
    hostname = fields.String()
    mac = fields.String()
    ip = fields.String()


class DiskSchema(Schema):
    id = fields.Integer()
    agent = AgentSchema()
    mountpoint = fields.String()


class StatisticSchema(Schema):
    id = fields.Integer()
    disk = DiskSchema()
    total = fields.String()
    free = fields.String()
    used = fields.String()
    percent = fields.String()
