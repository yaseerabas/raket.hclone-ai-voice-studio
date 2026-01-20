import requests

audio_url = "http://127.0.0.1:5001/static/audios/audio_c931423e-ee8d-4c55-96c7-4c681ed55d35.mp3"

audio_resp = requests.get(audio_url, stream=True)

if audio_resp.status_code != 200:
    print({"error": "Failed to download audio"})

local_path = "received_audio.mp3"

with open(local_path, "wb") as f:
    for chunk in audio_resp.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)
