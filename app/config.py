# app/config.py

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MySQL database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://raket_user:StrongPass_123!@localhost:3306/raket_ai'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT config
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET') or 'supersecretkey123'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # File paths
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    CLONED_VOICE_FOLDER = os.path.join(UPLOAD_FOLDER, 'cloned_voices')
    GENERATED_AUDIO_FOLDER = os.path.join(UPLOAD_FOLDER, 'generated_audio')

    # Other configs
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # Max 50 MB uploads
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}