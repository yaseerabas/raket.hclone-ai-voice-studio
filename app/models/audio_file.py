# app/models/audio_file.py
from app import db
from datetime import datetime, timedelta

class AudioFile(db.Model):
    __tablename__ = 'audio_files'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    characters_used = db.Column(db.BigInteger, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expire_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=7))
