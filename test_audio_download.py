#!/usr/bin/env python3
"""
Test script for audio download functionality
Run this after starting the Flask server to test the audio generation and download
"""

import requests
import json
import os

# Configuration
BASE_URL = "http://127.0.0.1:5000/api"
TEST_USER = {
    "email": "test@example.com",
    "password": "test123",
    "user_type": "user"
}

def test_audio_workflow():
    """Test the complete audio generation and download workflow"""
    
    print("🚀 Starting Audio Download Test...")
    
    # Step 1: Register user (if not exists)
    print("\n1. Registering test user...")
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=TEST_USER)
        if response.status_code == 201:
            print("✅ User registered successfully")
        elif response.status_code == 400 and "already exists" in response.text:
            print("ℹ️  User already exists, continuing...")
        else:
            print(f"❌ Registration failed: {response.text}")
    except Exception as e:
        print(f"❌ Registration error: {e}")
    
    # Step 2: Login
    print("\n2. Logging in...")
    try:
        login_data = {"email": TEST_USER["email"], "password": TEST_USER["password"]}
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            user_id = data.get("user", {}).get("id")
            print(f"✅ Login successful! User ID: {user_id}")
            
            headers = {"Authorization": f"Bearer {token}"}
            
        else:
            print(f"❌ Login failed: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 3: Generate TTS Audio
    print("\n3. Generating TTS audio...")
    try:
        tts_data = {
            "text": "Hello, this is a test audio generation for download functionality.",
            "language": "en",
            "voice_model": "male"
        }
        
        response = requests.post(f"{BASE_URL}/voice/generate", 
                               json=tts_data, 
                               headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            audio_id = data.get("audio_id")
            file_path = data.get("file_path")
            print(f"✅ Audio generated successfully!")
            print(f"   Audio ID: {audio_id}")
            print(f"   File Path: {file_path}")
            
        else:
            print(f"❌ Audio generation failed: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Audio generation error: {e}")
        return
    
    # Step 4: Download Audio
    print("\n4. Testing audio download...")
    try:
        download_url = f"{BASE_URL}/voice/download/{audio_id}"
        response = requests.get(download_url, headers=headers)
        
        if response.status_code == 200:
            # Save downloaded file
            download_path = f"test_download_{audio_id}.mp3"
            with open(download_path, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"✅ Audio downloaded successfully!")
            print(f"   Downloaded to: {download_path}")
            print(f"   File size: {file_size} bytes")
            
            # Verify file exists
            if os.path.exists(download_path):
                print(f"✅ Downloaded file verified on disk")
            else:
                print(f"❌ Downloaded file not found on disk")
                
        else:
            print(f"❌ Audio download failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Audio download error: {e}")
    
    # Step 5: Test alternative download endpoint
    print("\n5. Testing alternative download endpoint...")
    try:
        alt_download_url = f"{BASE_URL}/voice/download-audio/{audio_id}"
        response = requests.get(alt_download_url, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Alternative download endpoint working!")
        else:
            print(f"❌ Alternative download endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Alternative download error: {e}")
    
    print("\n🏁 Test completed!")

if __name__ == "__main__":
    test_audio_workflow()