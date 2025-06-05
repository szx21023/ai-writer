# -*- coding: UTF-8 -*-
from marshmallow import fields, Schema

class NodeSchema(Schema):
    id = fields.Integer()
    conversation_id = fields.Integer(required=True)
    prompt = fields.String(required=True)
    content = fields.String(required=True)
    order = fields.Integer(required=True)
    create_time = fields.DateTime(required=True)
    update_time = fields.DateTime(required=True)