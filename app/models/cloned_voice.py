# app/models/cloned_voice.py
from app import db
from datetime import datetime

class ClonedVoice(db.Model):
    __tablename__ = 'cloned_voices'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    voice_file_path = db.Column(db.String(255), nullable=False)
    voice_name = db.Column(db.String(100), nullable=False)
    speaker_id = db.Column(db.String(100), nullable=True)  # Unique ID for external API
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
