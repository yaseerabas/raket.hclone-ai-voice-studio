# app/schemas/plan_schema.py
from app import ma
from marshmallow import fields

class PlanSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    character_limit = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
