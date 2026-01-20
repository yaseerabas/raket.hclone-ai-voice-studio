# app/schemas/subscription_schema.py
from app import ma
from marshmallow import fields

class SubscriptionSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    plan_id = fields.Int(required=True)
    start_date = fields.DateTime(dump_only=True)
    end_date = fields.DateTime()
    status = fields.Str(validate=lambda x: x in ['active', 'cancelled', 'expired'])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)