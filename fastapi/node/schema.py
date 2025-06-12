# -*- coding: UTF-8 -*-
from marshmallow import fields, Schema, EXCLUDE

class NodeSchema(Schema):
    id = fields.Int(dump_only=True)
    conversation_id = fields.Int(required=True)
    prompt = fields.Str()
    content = fields.Str()
    order = fields.Float(required=True)
    create_time = fields.DateTime()
    update_time = fields.DateTime()

    class Meta:
        unknown = EXCLUDE

class CreateNodeSchema(Schema):
    conversation_id = fields.Int(required=True)
    prompt = fields.Str()
    content = fields.Str()
    last_node_id = fields.Int()
    next_node_id = fields.Int()