# app/routes/translation_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
# from your translation helper (Hugging Face NLLB-200)
translation_bp = Blueprint('translation', __name__)

@translation_bp.route('/translate', methods=['POST'])
@jwt_required()
def translate_text():
    try:
        data = request.get_json()
        text = data.get("text")
        target_lang = data.get("language")

        if not text or not target_lang:
            return jsonify({"error": "Text and language required"}), 400

        # Call your separate translation app
        translated_text = f"Translated({target_lang}): {text}"  # Integrate with your translation app

        return jsonify({"translated_text": translated_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
