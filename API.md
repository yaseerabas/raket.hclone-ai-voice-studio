# Translation & TTS API Documentation

A production-ready FastAPI service for multilingual text translation, text-to-speech (TTS), and lightweight voice cloning.

- Base URL: http://localhost:8000
- OpenAPI UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json
- Default audio mount: /audio (serves generated .wav files)

## Conventions

- Content type: application/json unless noted (file uploads use multipart/form-data)
- Responses: JSON bodies with appropriate HTTP status codes
- Errors: 4xx for client errors (e.g., bad file type), 5xx for server/model errors

---

## Root

GET /

Returns a simple service banner and a link to docs.

Example response 200:
```json
{
  "message": "Translation & TTS API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

## Metadata

GET /health

Returns health and model status.

Response 200:
```json
{
  "status": "healthy",
  "models": { "translation": true, "tts": true },
  "models_enabled": { "translation": true, "tts": true },
  "device": "cuda",
  "cuda_available": true
}
```

Notes:
- status is "healthy" when enabled models are loaded; otherwise "degraded".

GET /languages

Lists supported languages for translation and TTS.

Response 200 (excerpt):
```json
{
  "translation": {
    "model": "NLLB-200",
    "languages": [
      { "code": "eng_Latn", "name": "English" },
      { "code": "urd_Arab", "name": "Urdu" }
      // ... more NLLB codes
    ]
  },
  "tts": {
    "model": "Qwen3-TTS-0.6B-Base",
    "languages": [
      { "code": "en", "name": "English" },
      { "code": "zh", "name": "Chinese" }
      // ...
    ]
  }
}
```

GET /voices

Lists available cloned voices (quick overview).

Response 200:
```json
{
  "count": 2,
  "voices": [
    { "user_id": "user_804", "path": "app/storage/voices/user_804/voice.wav", "available": true }
  ]
}
```

---

## Translation

POST /translate

Translate text between languages using NLLB-200.

Request body:
```json
{
  "text": "Hello, how are you?",
  "src_lang": "eng_Latn",
  "tgt_lang": "urd_Arab"
}
```

Response 200:
```json
{ "translated_text": "سلام، آپ کیسے ہیں؟" }
```

Error responses:
- 500 Translation failed: <reason>

Curl example:
```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "src_lang": "eng_Latn",
    "tgt_lang": "urd_Arab"
  }'
```

---

## Text-to-Speech (TTS)

POST /tts

Synthesize speech from text using Qwen3-TTS. Supports cloned voices via `speaker_id` if a voice has been uploaded for that user.

Request body:
```json
{
  "text": "Hello, this is a test",
  "language": "en",
  "speaker_id": "default"
}
```

Response 200:
```json
{
  "audio_path": "/audio/2e5c4e2f9a9a4f5a9c70cbe0a7f1b123.wav",
  "file_path": "app/storage/audio/2e5c4e2f9a9a4f5a9c70cbe0a7f1b123.wav"
}
```

Notes:
- `language` accepts: en, zh, ja, ko, de, fr, ru, pt, es, it. Others (e.g., ar, hi, ur) fall back to Auto.
- Download the audio with: `curl -o out.wav http://localhost:8000/audio/<filename>.wav`

Errors:
- 500 TTS synthesis failed: <reason>

Curl example:
```bash
curl -X POST "http://localhost:8000/tts" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test",
    "language": "en",
    "speaker_id": "default"
  }'
```

---

## Text-to-Speech Streaming (TTS)

POST /tts/stream

Synthesize speech from text using Qwen3-TTS with **streaming response**. This endpoint is optimized for long audio generation to prevent HTTP timeouts.

The response is a streaming WAV audio file that begins playing as soon as the first chunk is generated. Uses Qwen3-TTS streaming generation mode for minimal latency (~97ms to first audio).

Request body:
```json
{
  "text": "This is a very long text that would normally cause a timeout...",
  "language": "en",
  "speaker_id": "default"
}
```

Response: `audio/wav` stream (binary audio data)

Notes:
- Use this endpoint for long texts (> 500 characters) or when the standard `/tts` endpoint times out.
- The response streams audio chunks as they are generated, so playback can begin immediately.
- Audio is returned as WAV format (PCM 16-bit, mono).
- `language` accepts: en, zh, ja, ko, de, fr, ru, pt, es, it. Others fall back to Auto.
- Supports voice cloning via `speaker_id` if a voice has been uploaded.

Errors:
- 500 TTS streaming failed: <reason>

Curl example (save to file):
```bash
curl -X POST "http://localhost:8000/tts/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a long text that we want to synthesize without timing out. The streaming endpoint returns audio chunks progressively.",
    "language": "en",
    "speaker_id": "default"
  }' \
  --output speech.wav
```

JavaScript fetch example (for browser playback):
```javascript
const response = await fetch('/tts/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Your long text here...',
    language: 'en',
    speaker_id: 'default'
  })
});

// Stream to audio element
const blob = await response.blob();
const audioUrl = URL.createObjectURL(blob);
const audio = new Audio(audioUrl);
audio.play();
```

---

## Translate + TTS (Combined)

POST /translate-tts

Optionally translate text first, then synthesize speech in one request.

Request body (with translation):
```json
{
  "text": "Hello, how are you?",
  "language": "ur",
  "speaker_id": "user_804",
  "src_lang": "eng_Latn",
  "tgt_lang": "urd_Arab"
}
```

Request body (TTS only, no translation):
```json
{
  "text": "مرحبا، كيف حالك؟",
  "language": "ar",
  "speaker_id": "default"
}
```

Response 200 (when translation is performed):
```json
{
  "audio_path": "/audio/1b2c3d4e.wav",
  "file_path": "app/storage/audio/1b2c3d4e.wav",
  "translated_text": "سلام، آپ کیسے ہیں؟",
  "original_text": "Hello, how are you?"
}
```

Response 200 (TTS only):
```json
{
  "audio_path": "/audio/1b2c3d4e.wav",
  "file_path": "app/storage/audio/1b2c3d4e.wav",
  "original_text": "مرحبا، كيف حالك؟"
}
```

Errors:
- 500 Translate-TTS failed: <reason>

Curl example:
```bash
curl -X POST "http://localhost:8000/translate-tts" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "language": "ur",
    "speaker_id": "user_804",
    "src_lang": "eng_Latn",
    "tgt_lang": "urd_Arab"
  }'
```

---

## Voice Cloning

POST /voice/upload

Upload a reference voice for a given `user_id`. File will be stored as `app/storage/voices/<user_id>/voice.wav`.

- Content type: multipart/form-data
- Form fields:
  - user_id: string (required)
  - voice_file: file (required) — .wav, .mp3, .flac, or .ogg

Response 200:
```json
{
  "message": "Voice uploaded successfully",
  "user_id": "user_804",
  "path": "app/storage/voices/user_804/voice.wav"
}
```

Errors:
- 400 Unsupported file type. Please upload .wav, .mp3, .flac, or .ogg
- 500 Voice upload failed: <reason>

Curl example:
```bash
curl -X POST "http://localhost:8000/voice/upload" \
  -F "user_id=user_804" \
  -F "voice_file=@voice.wav"
```

GET /voice/list

List all available cloned voices.

Response 200:
```json
{
  "voices": [
    { "user_id": "user_804", "path": "app/storage/voices/user_804/voice.wav", "available": true }
  ]
}
```

---

## Language Codes

TTS (Qwen3-TTS): en, zh, ja, ko, de, fr, ru, pt, es, it. Additional languages can be attempted with Auto detection (e.g., ar, hi, ur).

Translation (NLLB-200): uses 200+ codes. Common examples:
- eng_Latn — English
- urd_Arab — Urdu
- hin_Deva — Hindi
- spa_Latn — Spanish
- fra_Latn — French
- deu_Latn — German
- ara_Arab — Arabic
- zho_Hans — Chinese (Simplified)
- jpn_Jpan — Japanese
- kor_Hang — Korean

Use GET /languages for an up-to-date list excerpt.

---

## Static Audio Files

Generated audio files are served under `/audio`. The API returns `audio_path` you can fetch directly:

```bash
curl -o output.wav "http://localhost:8000/audio/<filename>.wav"
```

---

## Notes & Tips

- To use a cloned voice in TTS, first upload a voice for `user_id`, then pass that `speaker_id` in /tts or /translate-tts requests.
- Long texts are automatically chunked for quality and memory efficiency; the API returns a single concatenated .wav.
- **For long audio generation**, use `/tts/stream` instead of `/tts` to prevent HTTP timeouts. The streaming endpoint returns audio progressively as it is generated.
- Health endpoint helps validate model readiness and GPU availability before high-volume requests.
