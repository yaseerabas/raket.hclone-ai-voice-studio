# app/schemas/usage_schema.py
from app import ma
from marshmallow import fields

class UsageSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    characters_used = fields.Int(dump_only=True)
    characters_remaining = fields.Int(dump_only=True)
    last_generated_at = fields.DateTime(dump_only=True)
