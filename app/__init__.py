# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    
    # Enhanced CORS configuration
    CORS(app, 
         origins=['*'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization'],
         supports_credentials=True)

    # Register blueprints (routes)
    from app.routes.auth_routes import auth_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.user_routes import user_bp
    from app.routes.tts_routes import tts_bp
    from app.routes.translation_routes import translation_bp
    from app.routes.subscription_routes import subscription_bp
    from app.routes.contact_routes import contact_bp
    from app.routes.tokens_routes import tokens_bp
    from app.routes.files_routes import files_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(tts_bp, url_prefix='/api/voice')
    app.register_blueprint(translation_bp, url_prefix='/api/translate')
    app.register_blueprint(subscription_bp, url_prefix='/api/subscriptions')
    app.register_blueprint(contact_bp, url_prefix='/api/contact')
    app.register_blueprint(tokens_bp, url_prefix='/api/tokens')
    app.register_blueprint(files_bp, url_prefix='/api/files')

    # Create tables if not exist
    with app.app_context():
        db.create_all()

    return app
