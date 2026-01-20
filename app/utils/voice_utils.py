# app/utils/voice_utils.py
import os
from app.utils.file_utils import save_file, ensure_folder

XTTS_FOLDER = "uploads/generated_audio"

# --------------------------
# Placeholder XTTS v2 TTS generator
# --------------------------
def generate_tts_audio(text, voice_model="male", language="en"):
    """
    Generates audio using XTTS v2 model
    Replace this placeholder with your XTTS v2 API call
    """
    ensure_folder(XTTS_FOLDER)
    filename = f"{voice_model}_{language}_{str(abs(hash(text)))}.mp3"
    file_path = os.path.join(XTTS_FOLDER, filename)

    # Dummy file content (replace with actual TTS audio bytes)
    with open(file_path, "wb") as f:
        f.write(b"Dummy audio content for XTTS v2")

    return file_path

# --------------------------
# Voice clone helper
# --------------------------
def clone_user_voice(file, user_id, voice_name):
    """
    Saves user voice file for cloning
    """
    CLONED_FOLDER = "uploads/cloned_voices"
    ensure_folder(CLONED_FOLDER)
    filename = f"{user_id}_{voice_name}_{str(abs(hash(file.filename)))}.wav"
    file_path = os.path.join(CLONED_FOLDER, filename)
    file.save(file_path)
    return file_path
