# app/schemas/cloned_voice_schema.py
from app import ma
from marshmallow import fields

class ClonedVoiceSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    voice_file_path = fields.Str(required=True)
    voice_name = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
