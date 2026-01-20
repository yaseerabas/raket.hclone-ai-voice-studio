#!/usr/bin/env python3
"""
Quick server check script
"""

import requests
import sys

def check_server():
    """Check if Flask server is running"""
    
    try:
        print("🔍 Checking if Flask server is running...")
        
        # Try to connect to the server
        response = requests.get("http://127.0.0.1:5000/api/auth/login", timeout=5)
        
        if response.status_code in [200, 400, 405]:  # Any response means server is running
            print("✅ Server is running!")
            return True
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running or not accessible")
        print("💡 Please start the server with: python run.py")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ Server is not responding (timeout)")
        return False
        
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

if __name__ == "__main__":
    if check_server():
        print("\n🚀 Server is ready for testing!")
        sys.exit(0)
    else:
        print("\n🛑 Please start the server first!")
        sys.exit(1)