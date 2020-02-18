from marshmallow import Schema
from marshmallow import fields


class QueryParamsSchema(Schema):
    limit = fields.Integer(default=20)
    offset = fields.Integer(default=0)

    class Meta:
        ordered = False


class AgentSchema(Schema):
    id = fields.Integer()
    hostname = fields.String()
    ip = fields.String()


class DisksSchema(Schema):
    id = fields.Integer()
    agent_id = fields.String()
    created_at = fields.DateTime()
    mountpoint = fields.String()
    total = fields.String()
    free = fields.String()
    used = fields.String()
    percent = fields.String()


class TasksSchema(Schema):
    id = fields.String()
    agent_id = fields.String()
    created_at = fields.DateTime()
    code = fields.Int()
    output = fields.String()
    errors = fields.String()
    command = fields.String()

class AllSchema(AgentSchema):
    disks = fields.List(fields.Nested(DisksSchema()))
    tasks = fields.List(fields.Nested(TasksSchema()))
