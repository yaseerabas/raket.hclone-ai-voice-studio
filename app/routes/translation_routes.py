# app/routes/translation_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import requests
from dotenv import load_dotenv

load_dotenv()

translation_bp = Blueprint('translation', __name__)

TTS_BASE_URL = os.getenv("TTS_BASE_URL")

# -------------------
# Translate Text
# -------------------
@translation_bp.route('/translate', methods=['POST'])
@jwt_required()
def translate_text():
    """
    Translate text between languages using the external NLLB-200 API.
    """
    try:
        identity = get_jwt_identity()
        if not identity:
            return jsonify({"error": "Invalid token"}), 401
            
        data = request.get_json()
        
        text = data.get('text')
        src_lang = data.get('src_lang')
        tgt_lang = data.get('tgt_lang')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        if not src_lang:
            return jsonify({"error": "Source language (src_lang) is required"}), 400
        if not tgt_lang:
            return jsonify({"error": "Target language (tgt_lang) is required"}), 400
        
        # Call external translation API
        translate_api_url = f"{TTS_BASE_URL}/translate"
        
        payload = {
            "text": text,
            "src_lang": src_lang,
            "tgt_lang": tgt_lang
        }
        
        try:
            response = requests.post(translate_api_url, json=payload, timeout=60)
            response.raise_for_status()
            translation_response = response.json()
            
            return jsonify({
                "translated_text": translation_response.get('translated_text'),
                "original_text": text,
                "src_lang": src_lang,
                "tgt_lang": tgt_lang
            }), 200
            
        except requests.exceptions.RequestException as e:
            print(f"Translation API Error: {str(e)}")
            return jsonify({"error": f"Translation API error: {str(e)}"}), 500
            
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# -------------------
# Get Supported Languages
# -------------------
@translation_bp.route('/languages', methods=['GET'])
@jwt_required()
def get_languages():
    """
    Get list of supported languages for translation from the external API.
    """
    try:
        # Call external languages API
        languages_api_url = f"{TTS_BASE_URL}/languages"
        
        try:
            response = requests.get(languages_api_url, timeout=30)
            response.raise_for_status()
            languages_data = response.json()
            
            # Return translation languages
            return jsonify(languages_data.get('translation', {})), 200
            
        except requests.exceptions.RequestException as e:
            print(f"Languages API Error: {str(e)}")
            # Return fallback list of common languages
            return jsonify({
                "model": "NLLB-200",
                "languages": [
                    {"code": "eng_Latn", "name": "English"},
                    {"code": "urd_Arab", "name": "Urdu"},
                    {"code": "hin_Deva", "name": "Hindi"},
                    {"code": "spa_Latn", "name": "Spanish"},
                    {"code": "fra_Latn", "name": "French"},
                    {"code": "deu_Latn", "name": "German"},
                    {"code": "ara_Arab", "name": "Arabic"},
                    {"code": "zho_Hans", "name": "Chinese (Simplified)"},
                    {"code": "jpn_Jpan", "name": "Japanese"},
                    {"code": "kor_Hang", "name": "Korean"}
                ]
            }), 200
            
    except Exception as e:
        print(f"Get languages error: {str(e)}")
        return jsonify({"error": str(e)}), 500
