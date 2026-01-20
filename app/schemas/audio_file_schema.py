# app/schemas/audio_file_schema.py
from app import ma
from marshmallow import fields

class AudioFileSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    file_path = fields.Str(required=True)
    characters_used = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    expire_at = fields.DateTime(dump_only=True)
