# app/routes/user_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.usage import Usage
from app.models.audio_file import AudioFile
from app.schemas.user_schema import UserSchema
from app.schemas.usage_schema import UsageSchema
from app.schemas.audio_file_schema import AudioFileSchema

user_bp = Blueprint('user', __name__)
user_schema = UserSchema()
usage_schema = UsageSchema()
audio_schema = AudioFileSchema()

# Dashboard: see usage
@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    try:
        identity = get_jwt_identity()
        user = User.query.get(int(identity))
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get user's usage data
        usage = Usage.query.filter_by(user_id=user.id).first()
        
        # Get plan info
        plan = user.plan if user.plan_id else None
        total_characters = plan.character_limit if plan else 0
        
        # Prepare response with user and usage data
        response_data = {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.email.split('@')[0],  # Extract name from email
                "user_type": user.user_type,
                "plan_id": user.plan_id,
                "has_subscription": plan is not None
            },
            "usage": {
                "characters_used": usage.characters_used if usage else 0,
                "characters_remaining": usage.characters_remaining if usage else 0,
                "total_characters": total_characters,
                "last_generated_at": usage.last_generated_at.isoformat() if usage and usage.last_generated_at else None
            },
            "subscription": {
                "plan_name": plan.name if plan else None,
                "status": "active" if plan else "no_subscription"
            }
        }
        
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get User Profile
@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404
        return user_schema.jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get Voice History
@user_bp.route('/voice-history', methods=['GET'])
@jwt_required()
def get_voice_history():
    try:
        user_id = get_jwt_identity()
        audios = AudioFile.query.filter_by(user_id=int(user_id)).all()
        result = audio_schema.dump(audios, many=True)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Download Audio (log download)
@user_bp.route('/download-audio', methods=['POST'])
@jwt_required()
def download_audio():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        audio_id = data.get('audio_id')
        audio = AudioFile.query.get(audio_id)
        if not audio or audio.user_id != int(user_id):
            return jsonify({"error": "Audio not found or access denied"}), 404
        # Log download, perhaps update a counter, but for now just return success
        return jsonify({"message": "Download logged", "download_url": f"/api/voice/download/{audio_id}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
