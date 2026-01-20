# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.usage import Usage
from app.schemas.user_schema import UserSchema
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()

# Register
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        # Validate input
        errors = user_schema.validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        # Check email duplication
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 400

        hashed_pw = generate_password_hash(data['password'])
        user = User(
            email=data['email'],
            password=hashed_pw,
            user_type=data['user_type']
        )
        db.session.add(user)
        db.session.flush()  # Get user.id before commit
        
        # Create usage record with 0 characters for new user
        usage = Usage(
            user_id=user.id,
            characters_used=0,
            characters_remaining=0
        )
        db.session.add(usage)
        db.session.commit()
        
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Login
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({"error": "Invalid credentials"}), 401

        # Create JWT token
        token = create_access_token(
            identity=str(user.id),
            additional_claims={"user_type": user.user_type}
        )
        user_data = user_schema.dump(user)
        return jsonify({"token": token, "user": user_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Change Password
@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()  # str(id)
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404

        old_password = data.get('old_password')
        new_password = data.get('new_password')
        if not old_password or not new_password:
            return jsonify({"error": "Old and new password required"}), 400

        if not check_password_hash(user.password, old_password):
            return jsonify({"error": "Old password incorrect"}), 400

        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({"message": "Password changed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Logout
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # Since JWT is stateless, logout is handled client-side by deleting the token
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Verify Token
@auth_bp.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404
        user_data = user_schema.dump(user)
        return jsonify({"user": user_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Admin Login
@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']) or user.user_type != 'admin':
            return jsonify({"error": "Invalid admin credentials"}), 401

        # Create JWT token
        token = create_access_token(
            identity=str(user.id),
            additional_claims={"user_type": user.user_type}
        )
        return jsonify({"token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
