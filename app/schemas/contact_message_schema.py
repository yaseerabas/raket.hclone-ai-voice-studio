# app/schemas/contact_message_schema.py
from app import ma
from marshmallow import fields, validate

class ContactMessageSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    subject = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    message = fields.Str(required=True, validate=validate.Length(min=1))
    created_at = fields.DateTime(dump_only=True)
    is_read = fields.Bool(dump_only=True)