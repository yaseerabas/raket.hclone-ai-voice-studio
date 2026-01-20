# app/routes/tokens_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.usage import Usage
from app.schemas.usage_schema import UsageSchema
from app import db

tokens_bp = Blueprint('tokens', __name__)
usage_schema = UsageSchema()

# Get Usage for User
@tokens_bp.route('/usage/<int:user_id>', methods=['GET'])
@jwt_required()
def get_usage(user_id):
    try:
        current_user_id = get_jwt_identity()
        if int(current_user_id) != user_id:
            return jsonify({"error": "Access denied"}), 403

        usage = Usage.query.filter_by(user_id=user_id).first()
        if not usage:
            return jsonify({"error": "Usage not found"}), 404
        return usage_schema.jsonify(usage), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Consume Tokens (deduct characters)
@tokens_bp.route('/consume', methods=['POST'])
@jwt_required()
def consume_tokens():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        characters = data.get('characters', 0)

        usage = Usage.query.filter_by(user_id=int(user_id)).first()
        if not usage or characters > usage.characters_remaining:
            return jsonify({"error": "Not enough tokens"}), 400

        usage.characters_used += characters
        usage.characters_remaining -= characters
        db.session.commit()
        return jsonify({"message": "Tokens consumed", "remaining": usage.characters_remaining}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500