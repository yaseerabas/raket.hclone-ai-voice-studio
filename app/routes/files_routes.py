# app/routes/files_routes.py
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
import os
from app.config import Config

files_bp = Blueprint('files', __name__)

# Upload File
@files_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    try:
        user_id = get_jwt_identity()
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        filename = secure_filename(f"{user_id}_{file.filename}")
        upload_folder = Config.UPLOAD_FOLDER
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Perhaps save to a File model, but for now just return path
        return jsonify({"message": "File uploaded", "file_path": file_path}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Download File
@files_bp.route('/download/<path:file_path>', methods=['GET'])
@jwt_required()
def download_file(file_path):
    try:
        user_id = get_jwt_identity()
        # Check if file belongs to user, assume filename starts with user_id
        if not file_path.startswith(str(user_id)):
            return jsonify({"error": "Access denied"}), 403

        full_path = os.path.join(Config.UPLOAD_FOLDER, os.path.basename(file_path))
        if not os.path.exists(full_path):
            return jsonify({"error": "File not found"}), 404

        return send_file(full_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500