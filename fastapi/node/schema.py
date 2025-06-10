# -*- coding: UTF-8 -*-
from marshmallow import fields, Schema

class NodeSchema(Schema):
    id = fields.Int(dump_only=True)
    conversation_id = fields.Int(required=True)
    prompt = fields.Str()
    content = fields.Str()
    order = fields.Int(required=True)
    create_time = fields.DateTime()
    update_time = fields.DateTime()