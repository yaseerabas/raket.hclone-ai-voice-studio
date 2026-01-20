# app/models/usage.py
from app import db
from datetime import datetime

class Usage(db.Model):
    __tablename__ = 'usage'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    characters_used = db.Column(db.BigInteger, default=0)
    characters_remaining = db.Column(db.BigInteger, default=0)
    last_generated_at = db.Column(db.DateTime, default=None)
