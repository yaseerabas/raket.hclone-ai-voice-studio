# app/utils/file_utils.py
import os
from datetime import datetime, timedelta

# --------------------------
# Ensure folders exist
# --------------------------
def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

# --------------------------
# Auto-delete generated audio
# --------------------------
def delete_expired_audio(AudioFileModel, session):
    """
    Delete generated audio older than 7 days
    AudioFileModel: SQLAlchemy model for generated audio
    session: db.session
    """
    now = datetime.utcnow()
    expired_files = AudioFileModel.query.filter(AudioFileModel.expire_at <= now).all()
    for audio in expired_files:
        if os.path.exists(audio.file_path):
            os.remove(audio.file_path)
        session.delete(audio)
    session.commit()

# --------------------------
# Save uploaded file
# --------------------------
def save_file(file, folder, filename=None):
    ensure_folder(folder)
    if not filename:
        filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
    file_path = os.path.join(folder, filename)
    file.save(file_path)
    return file_path
