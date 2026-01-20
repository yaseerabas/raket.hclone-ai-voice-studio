# API Testing Guide

## Quick Test Commands

### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "models": {
    "translation": true,
    "tts": true
  },
  "device": "cuda",
  "cuda_available": true
}
```

---

### 2. Get Languages
```bash
curl http://localhost:8000/languages
```

**Expected Response:**
```json
{
  "translation": {
    "model": "NLLB-200",
    "languages": [
      {"code": "eng_Latn", "name": "English"},
      {"code": "urd_Arab", "name": "Urdu"},
      ...
    ]
  },
  "tts": {
    "model": "XTTS-v2",
    "languages": [
      {"code": "en", "name": "English"},
      {"code": "es", "name": "Spanish"},
      ...
    ]
  }
}
```

---

### 3. Translate Text
```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "src_lang": "eng_Latn",
    "tgt_lang": "urd_Arab"
  }'
```

**Expected Response:**
```json
{
  "translated_text": "ہیلو، آپ کیسے ہیں؟"
}
```

---

### 4. Generate TTS (Default Voice)
```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test of the text to speech system.",
    "language": "en",
    "speaker_id": "default"
  }'
```

**Expected Response:**
```json
{
  "audio_path": "/audio/abc123def456.wav",
  "file_path": "app/storage/audio/abc123def456.wav"
}
```

---

### 5. Generate TTS (Cloned Voice)
```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is using a cloned voice.",
    "language": "en",
    "speaker_id": "user_123"
  }'
```

---

### 6. Combined Translation + TTS
```bash
curl -X POST http://localhost:8000/translate-tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "src_lang": "eng_Latn",
    "tgt_lang": "urd_Arab",
    "language": "ur",
    "speaker_id": "default"
  }'
```

**Expected Response:**
```json
{
  "audio_path": "/audio/xyz789abc123.wav",
  "file_path": "app/storage/audio/xyz789abc123.wav",
  "translated_text": "ہیلو، آپ کیسے ہیں؟",
  "original_text": "Hello, how are you?"
}
```

---

### 7. TTS Only (Without Translation)
```bash
curl -X POST http://localhost:8000/translate-tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test.",
    "language": "en",
    "speaker_id": "default"
  }'
```

**Note**: When `src_lang` and `tgt_lang` are not provided, only TTS is performed.

---

### 8. Upload Voice
```bash
curl -X POST http://localhost:8000/voice/upload \
  -F "user_id=user_123" \
  -F "voice_file=@/path/to/voice.wav"
```

**Expected Response:**
```json
{
  "message": "Voice uploaded successfully",
  "user_id": "user_123",
  "path": "app/storage/voices/user_123/voice.wav"
}
```

---

### 9. List Voices
```bash
curl http://localhost:8000/voice/list
```

**Expected Response:**
```json
{
  "voices": [
    {
      "user_id": "user_123",
      "path": "app/storage/voices/user_123/voice.wav",
      "available": true
    },
    {
      "user_id": "user_456",
      "path": "app/storage/voices/user_456/voice.wav",
      "available": true
    }
  ]
}
```

---

### 10. Get Voices (Alternative Endpoint)
```bash
curl http://localhost:8000/voices
```

**Expected Response:**
```json
{
  "count": 2,
  "voices": [
    {
      "user_id": "user_123",
      "path": "app/storage/voices/user_123/voice.wav",
      "available": true
    }
  ]
}
```

---

## Testing from Dashboard

### Test Sequence:

1. **Open Dashboard**
   ```
   Open: http://localhost:5000/dashboard-enhanced.html
   (or wherever you host the frontend)
   ```

2. **Check Health Status**
   - Green indicator = System healthy
   - Red indicator = System offline

3. **Test Translation**
   - Go to "Translation" tab
   - Enter: "Hello, how are you?"
   - Source: English (eng_Latn)
   - Target: Urdu (urd_Arab)
   - Click "Translate"
   - Should see: "ہیلو، آپ کیسے ہیں؟"

4. **Test TTS**
   - Go to "Text-to-Speech" tab
   - Enter: "This is a test"
   - Language: English (en)
   - Speaker: Default Voice
   - Click "Generate Voice"
   - Should hear audio in preview player

5. **Test Combined**
   - Go to "Translate & TTS" tab
   - Enter: "Good morning"
   - Source: English
   - Target: Spanish
   - TTS Language: Spanish
   - Click "Translate & Generate Voice"
   - Should see translation and hear Spanish audio

6. **Test Voice Upload**
   - Go to "Voice Cloning" tab
   - Drag/drop or select WAV file
   - Enter user ID: "test_user_1"
   - Click "Upload Voice"
   - Should see success message
   - Voice should appear in list

---

## Common Test Scenarios

### Scenario 1: English to Urdu Translation + TTS
```json
{
  "text": "Welcome to our application",
  "src_lang": "eng_Latn",
  "tgt_lang": "urd_Arab",
  "language": "ur",
  "speaker_id": "default"
}
```

### Scenario 2: Spanish to English Translation + TTS
```json
{
  "text": "Hola, ¿cómo estás?",
  "src_lang": "spa_Latn",
  "tgt_lang": "eng_Latn",
  "language": "en",
  "speaker_id": "default"
}
```

### Scenario 3: Long Text TTS
```json
{
  "text": "Time is the most valuable resource we have...",
  "language": "en",
  "speaker_id": "user_123"
}
```

---

## Verification Checklist

### Backend Server (Port 8000)
- [ ] Server is running
- [ ] `/health` endpoint returns 200
- [ ] Translation model is loaded
- [ ] TTS model is loaded
- [ ] Storage directories exist

### Frontend Dashboard
- [ ] Health status indicator is green
- [ ] All language dropdowns are populated
- [ ] All tabs are clickable
- [ ] Forms accept input
- [ ] Buttons are enabled

### Translation Feature
- [ ] Text input works
- [ ] Language selection works
- [ ] Swap button swaps languages
- [ ] Translation result displays
- [ ] Translation is accurate

### TTS Feature
- [ ] Text input works
- [ ] Language dropdown populated
- [ ] Speaker dropdown populated
- [ ] Generate button works
- [ ] Audio preview plays
- [ ] Download button works

### Combined Feature
- [ ] All inputs work
- [ ] Translation displays
- [ ] Audio generates
- [ ] Both results shown together
- [ ] Download works

### Voice Cloning
- [ ] File upload works
- [ ] Drag & drop works
- [ ] User ID input works
- [ ] Upload button works
- [ ] Voice list updates
- [ ] New voices appear in dropdowns

---

## Error Testing

### Test Invalid Input
```bash
# Empty text
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "", "src_lang": "eng_Latn", "tgt_lang": "urd_Arab"}'

# Invalid language code
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "src_lang": "invalid", "tgt_lang": "urd_Arab"}'
```

### Test File Upload Errors
```bash
# File too large (>10MB)
curl -X POST http://localhost:8000/voice/upload \
  -F "user_id=test" \
  -F "voice_file=@large_file.wav"

# Invalid file type
curl -X POST http://localhost:8000/voice/upload \
  -F "user_id=test" \
  -F "voice_file=@document.pdf"
```

---

## Performance Testing

### Test Response Times
```bash
# Measure translation time
time curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "src_lang": "eng_Latn", "tgt_lang": "urd_Arab"}'

# Measure TTS generation time
time curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "language": "en", "speaker_id": "default"}'
```

---

## Debugging Tips

### Check Logs
```bash
# Backend server logs
tail -f server.log

# Check for errors
grep -i error server.log
```

### Browser Console
1. Open Developer Tools (F12)
2. Go to Console tab
3. Look for:
   - Network errors
   - JavaScript errors
   - API response errors

### Network Tab
1. Open Developer Tools (F12)
2. Go to Network tab
3. Check:
   - Request headers
   - Response status codes
   - Response payloads
   - Request timing

---

## Expected Behavior

### Successful Translation
- Status: 200 OK
- Response contains `translated_text`
- Text is different from input (unless same language)

### Successful TTS
- Status: 200 OK
- Response contains `audio_path`
- Audio file exists in storage
- Audio duration > 0

### Successful Voice Upload
- Status: 200 OK
- File saved in storage
- Voice appears in list
- Voice available for TTS

### Health Check
- Status: 200 OK
- Models show `true`
- Device shows GPU or CPU

---

## Troubleshooting Guide

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| 404 Not Found | Wrong URL | Check API base URL |
| 500 Server Error | Model not loaded | Restart server |
| CORS Error | Missing headers | Add CORS middleware |
| Audio not playing | Wrong format | Check audio codec |
| Upload fails | File too large | Reduce file size |
| Translation empty | Invalid language | Check language code |
| Slow response | CPU mode | Use GPU if available |

---

**Last Updated**: 2025-01-16
**Server Version**: 1.0
**API Version**: 1.0
