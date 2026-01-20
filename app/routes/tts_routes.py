# app/routes/tts_routes.py
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.audio_file import AudioFile
from app.models.cloned_voice import ClonedVoice
from app.models.usage import Usage
from app import db
from datetime import datetime, timedelta
import os, glob
from werkzeug.utils import secure_filename
from app.config import Config
from pydub import AudioSegment
from pydub.generators import Sine
from dotenv import load_dotenv
import requests

load_dotenv()

tts_bp = Blueprint('tts', __name__)

GENERATED_FOLDER = Config.GENERATED_AUDIO_FOLDER
CLONED_FOLDER = Config.CLONED_VOICE_FOLDER

TTS_BASE_URL = os.getenv("TTS_BASE_URL")

# -------------------
# Generate TTS Audio
# -------------------
@tts_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_tts():
    try:
        identity = get_jwt_identity()
        print(f"Generate TTS - JWT Identity: {identity}, Type: {type(identity)}")  # Debug log
        
        if not identity:
            print("No JWT identity found in generate_tts")  # Debug log
            return jsonify({"error": "Invalid token"}), 401
            
        user_id = int(identity)
        data = request.get_json()
        print(f"Generate TTS - User ID: {user_id}, Data: {data}")  # Debug log
        
        text = data.get('text')
        if not text:
            return jsonify({"error": "Text is required"}), 400
            
        characters = len(text)

        usage = Usage.query.filter_by(user_id=user_id).first()
        if not usage or characters > usage.characters_remaining:
            print(f"Not enough characters: usage={usage}, characters={characters}")  # Debug log
            return jsonify({"error": "Not enough characters in plan"}), 400

        # Prepare API request
        language = data.get('language', 'en')  # Tone/language for TTS
        source_language = data.get('source_language')  # Optional
        target_language = data.get('target_language')  # Optional
        voice_model = data.get('voice_model', 'male')  # Voice type or speaker_id
        
        # Check if voice_model is a speaker_id (from cloned voice) or default voice type
        # Speaker IDs are in format "user-XXX-YYYY"
        if voice_model.startswith('user-'):
            speaker_id = voice_model  # Use the cloned voice speaker_id
        else:
            speaker_id = f"user_{user_id}"  # Default speaker_id for built-in voices
        
        # Prepare TTS API payload for the new endpoint
        tts_payload = {
            "text": text,
            "language": language,
            "speaker_id": speaker_id
        }
        
        # Add optional language parameters if provided
        if source_language:
            tts_payload["src_lang"] = source_language
        if target_language:
            tts_payload["tgt_lang"] = target_language
            
        print(f"TTS API Payload: {tts_payload}")  # Debug log
        
        # Call external TTS API
        tts_api_url = f"{TTS_BASE_URL}/translate-tts"
        
        try:
            response = requests.post(tts_api_url, json=tts_payload, timeout=60)
            response.raise_for_status()
            tts_response = response.json()
            print(f"TTS API Response: {tts_response}")  # Debug log
            
            # Get the audio file path from API response
            remote_audio_path = tts_response.get('file_path')
            if not remote_audio_path:
                return jsonify({"error": "No audio file path in API response"}), 500
                
            # Download the audio file from the remote server
            audio_filename = os.path.basename(remote_audio_path)
            local_filename = f"{user_id}_{datetime.utcnow().timestamp()}_{audio_filename}"
            file_path = os.path.join(GENERATED_FOLDER, local_filename)
            os.makedirs(GENERATED_FOLDER, exist_ok=True)
            
            # Download audio file
            base_url = f"{TTS_BASE_URL}"
            audio_url = tts_response.get('audio_path')
            if audio_url:
                if not audio_url.startswith('http'):
                    audio_url = f"{base_url}{audio_url}"
                    
                audio_response = requests.get(audio_url, timeout=30)
                audio_response.raise_for_status()
                
                with open(file_path, 'wb') as f:
                    f.write(audio_response.content)
                    
                print(f"Downloaded audio file to: {file_path}")  # Debug log
            else:
                return jsonify({"error": "No audio path in API response"}), 500
                
        except requests.exceptions.RequestException as e:
            print(f"TTS API Error: {str(e)}")  # Debug log
            return jsonify({"error": f"TTS API error: {str(e)}"}), 500

        # Update usage
        usage.characters_used += characters
        usage.characters_remaining -= characters
        usage.last_generated_at = datetime.utcnow()
        db.session.commit()

        # Save audio record
        audio = AudioFile(user_id=user_id, file_path=file_path, characters_used=characters)
        db.session.add(audio)
        db.session.commit()
        
        print(f"Audio generated successfully: {audio.id}")  # Debug log
        return jsonify({"message": "Audio generated", "file_path": file_path, "audio_id": audio.id}), 200
    except Exception as e:
        print(f"Generate TTS error: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()  # Print full stack trace
        return jsonify({"error": str(e)}), 500

# -------------------
# Download Audio
# -------------------
@tts_bp.route('/download/<int:audio_id>', methods=['GET'])
@jwt_required()
def download_audio(audio_id):
    try:
        identity = get_jwt_identity()
        print(f"JWT Identity: {identity}, Type: {type(identity)}")  # Debug log
        
        if not identity:
            print("No JWT identity found")  # Debug log
            return jsonify({"error": "Invalid token"}), 401
            
        user_id = int(identity)
        print(f"User ID: {user_id}, Audio ID: {audio_id}")  # Debug log
        
        audio = AudioFile.query.get(audio_id)
        if not audio:
            print(f"Audio not found: {audio_id}")  # Debug log
            return jsonify({"error": "Audio file not found"}), 404
            
        if audio.user_id != user_id:
            print(f"Access denied: audio.user_id={audio.user_id}, user_id={user_id}")  # Debug log
            return jsonify({"error": "Access denied"}), 403
            
        if not os.path.exists(audio.file_path):
            print(f"File not found on disk: {audio.file_path}")  # Debug log
            return jsonify({"error": "Audio file not found on disk"}), 404
            
        print(f"Sending file: {audio.file_path}")  # Debug log
        return send_file(audio.file_path, as_attachment=True, download_name=f"audio_{audio_id}.wav")
        
    except Exception as e:
        print(f"Download error: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()  # Print full stack trace
        return jsonify({"error": str(e)}), 500

# -------------------
# Stream Audio for Preview
# -------------------
@tts_bp.route('/stream/<int:audio_id>', methods=['GET'])
@jwt_required()
def stream_audio(audio_id):
    try:
        identity = get_jwt_identity()
        print(f"Stream JWT Identity: {identity}, Type: {type(identity)}")  # Debug log
        
        if not identity:
            print("No JWT identity found")  # Debug log
            return jsonify({"error": "Invalid token"}), 401
            
        user_id = int(identity)
        print(f"Stream User ID: {user_id}, Audio ID: {audio_id}")  # Debug log
        
        audio = AudioFile.query.get(audio_id)
        if not audio:
            print(f"Audio not found: {audio_id}")  # Debug log
            return jsonify({"error": "Audio file not found"}), 404
            
        if audio.user_id != user_id:
            print(f"Access denied: audio.user_id={audio.user_id}, user_id={user_id}")  # Debug log
            return jsonify({"error": "Access denied"}), 403
            
        if not os.path.exists(audio.file_path):
            print(f"File not found on disk: {audio.file_path}")  # Debug log
            return jsonify({"error": "Audio file not found on disk"}), 404
            
        print(f"Streaming file: {audio.file_path}")  # Debug log
        return send_file(audio.file_path, as_attachment=False)
        
    except Exception as e:
        print(f"Stream error: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()  # Print full stack trace
        return jsonify({"error": str(e)}), 500

@tts_bp.route('/download-audio/<int:audio_id>', methods=['GET'])
@jwt_required()
def download_audio_alt(audio_id):
    return download_audio(audio_id)

# -------------------
# Voice Cloning
# -------------------
@tts_bp.route('/clone-voice', methods=['POST'])
@jwt_required()
def clone_voice():
    try:
        identity = get_jwt_identity()
        user_id = int(identity)

        if 'voice_file' not in request.files or 'voice_name' not in request.form:
            return jsonify({"error": "Voice file and name required"}), 400

        file = request.files['voice_file']
        voice_name = request.form['voice_name']
        
        # Generate unique user_id for the clone
        import random
        unique_id = f"user-{random.randint(100, 999)}-{datetime.utcnow().year}"
        
        # Prepare file for external API
        files = {'voice_file': (file.filename, file.stream, file.content_type)}
        data = {'user_id': unique_id}
        
        # Call external voice cloning API
        clone_api_url = f"{TTS_BASE_URL}/voice/upload"
        
        try:
            response = requests.post(clone_api_url, files=files, data=data, timeout=60)
            response.raise_for_status()
            clone_response = response.json()
            print(f"Clone API Response: {clone_response}")  # Debug log
            
            remote_voice_path = clone_response.get('path')
            if not remote_voice_path:
                return jsonify({"error": "No voice path in API response"}), 500
                
        except requests.exceptions.RequestException as e:
            print(f"Clone API Error: {str(e)}")  # Debug log
            return jsonify({"error": f"Voice cloning API error: {str(e)}"}), 500
        
        # Save locally as well
        filename = secure_filename(f"{user_id}_{voice_name}_{datetime.utcnow().timestamp()}.wav")
        os.makedirs(CLONED_FOLDER, exist_ok=True)
        file_path = os.path.join(CLONED_FOLDER, filename)
        
        # Reset file stream and save locally
        file.stream.seek(0)
        file.save(file_path)

        # Save to DB with unique_id as speaker_id
        voice = ClonedVoice(
            user_id=user_id, 
            voice_file_path=file_path, 
            voice_name=voice_name,
            speaker_id=unique_id  # Store the unique ID for later use
        )
        db.session.add(voice)
        db.session.commit()

        return jsonify({
            "message": "Voice cloned successfully", 
            "voice_id": voice.id,
            "speaker_id": unique_id,
            "remote_path": remote_voice_path
        }), 200
    except Exception as e:
        print(f"Clone voice error: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# -------------------
# List / Search / Filter Cloned Voices
# -------------------
@tts_bp.route('/voices', methods=['GET'])
@jwt_required()
def list_voices():
    try:
        identity = get_jwt_identity()
        user_id = int(identity)
        search = request.args.get('search', '')

        voices = ClonedVoice.query.filter(
            ClonedVoice.user_id==user_id,
            ClonedVoice.voice_name.ilike(f"%{search}%")
        ).all()

        result = [{
            "id": v.id, 
            "voice_name": v.voice_name, 
            "file_path": v.voice_file_path,
            "speaker_id": v.speaker_id
        } for v in voices]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------
# Download Cloned Voice
# -------------------
@tts_bp.route('/voices/<int:voice_id>/download', methods=['GET'])
@jwt_required()
def download_voice(voice_id):
    try:
        identity = get_jwt_identity()
        user_id = int(identity)

        voice = ClonedVoice.query.filter_by(id=voice_id, user_id=user_id).first()
        if not voice:
            return jsonify({"error": "Voice not found or access denied"}), 404

        if not os.path.exists(voice.voice_file_path):
            return jsonify({"error": "Voice file not found on disk"}), 404

        return send_file(voice.voice_file_path, as_attachment=True, download_name=f"{voice.voice_name}.wav")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------
# Delete Cloned Voice
# -------------------
@tts_bp.route('/voices/<int:voice_id>', methods=['DELETE'])
@jwt_required()
def delete_voice(voice_id):
    try:
        identity = get_jwt_identity()
        user_id = int(identity)

        voice = ClonedVoice.query.filter_by(id=voice_id, user_id=user_id).first()
        if not voice:
            return jsonify({"error": "Voice not found or access denied"}), 404

        # Delete file from filesystem
        if os.path.exists(voice.voice_file_path):
            os.remove(voice.voice_file_path)

        # Delete from database
        db.session.delete(voice)
        db.session.commit()

        return jsonify({"message": "Voice deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------
# Auto-delete Generated Audio > 7 days
# -------------------
def delete_expired_audio():
    now = datetime.utcnow()
    expired_audios = AudioFile.query.filter(AudioFile.expire_at <= now).all()
    for audio in expired_audios:
        if os.path.exists(audio.file_path):
            os.remove(audio.file_path)
        db.session.delete(audio)
    db.session.commit()

# You can call delete_expired_audio() via a scheduled job (cron, APScheduler, or Celery)
# to periodically clean up old audio files.

# -------------------
# Get Supported Languages
# -------------------
@tts_bp.route('/languages', methods=['GET'])
@jwt_required()
def get_languages():
    try:
        # Placeholder: List of supported languages for TTS
        languages = [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"},
            {"code": "it", "name": "Italian"},
            {"code": "pt", "name": "Portuguese"},
            {"code": "ru", "name": "Russian"},
            {"code": "ja", "name": "Japanese"},
            {"code": "ko", "name": "Korean"},
            {"code": "zh", "name": "Chinese"}
        ]
        return jsonify(languages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------
# Get Voice Styles
# -------------------
@tts_bp.route('/styles', methods=['GET'])
@jwt_required()
def get_styles():
    try:
        # Placeholder: List of voice styles
        styles = [
            {"id": 1, "name": "Neutral", "description": "Standard neutral voice"},
            {"id": 2, "name": "Cheerful", "description": "Happy and energetic"},
            {"id": 3, "name": "Serious", "description": "Formal and professional"},
            {"id": 4, "name": "Calm", "description": "Relaxed and soothing"}
        ]
        return jsonify(styles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------
# Get User's Audio History
# -------------------
@tts_bp.route('/history', methods=['GET'])
@jwt_required()
def get_audio_history():
    try:
        identity = get_jwt_identity()
        user_id = int(identity)
        
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Query user's audio files ordered by creation date (newest first)
        audios = AudioFile.query.filter_by(user_id=user_id)\
            .order_by(AudioFile.created_at.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        result = [{
            "id": audio.id,
            "file_path": audio.file_path,
            "characters_used": audio.characters_used,
            "created_at": audio.created_at.isoformat() if audio.created_at else None,
            "expires_at": audio.expire_at.isoformat() if audio.expire_at else None
        } for audio in audios]
        
        # Get total count
        total_count = AudioFile.query.filter_by(user_id=user_id).count()
        
        return jsonify({
            "audios": result,
            "total": total_count,
            "limit": limit,
            "offset": offset
        }), 200
        
    except Exception as e:
        print(f"Audio history error: {str(e)}")
        return jsonify({"error": str(e)}), 500