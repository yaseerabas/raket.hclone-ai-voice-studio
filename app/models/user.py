# app/models/user.py
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.Enum('admin', 'user'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    plan = db.relationship('Plan', backref='users', lazy=True)
    usage = db.relationship('Usage', backref='user', uselist=False)
    cloned_voices = db.relationship('ClonedVoice', backref='user', lazy=True)
    audio_files = db.relationship('AudioFile', backref='user', lazy=True)
