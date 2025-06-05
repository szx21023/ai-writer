# -*- coding: UTF-8 -*-
from marshmallow import fields, Schema

class ConversationSchema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    create_time = fields.DateTime()
    update_time = fields.DateTime()