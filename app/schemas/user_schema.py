# app/schemas/user_schema.py
from app import ma
from marshmallow import fields, validate

class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    user_type = fields.Str(required=True, validate=validate.OneOf(["admin", "user"]))
    plan_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
