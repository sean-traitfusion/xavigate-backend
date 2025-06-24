#!/usr/bin/env python3
"""
Get a test JWT token for API testing
"""
import requests
import json

AUTH_URL = "http://localhost:8014"

def get_test_token():
    """Get a test JWT token"""
    
    # In dev mode, the auth service accepts any user_id
    test_user_id = "test_memory_limit_user"
    
    print(f"🔑 Getting JWT token for user: {test_user_id}")
    
    response = requests.post(f"{AUTH_URL}/api/auth/get-token", json={
        "user_id": test_user_id
    })
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"\n✅ Token obtained successfully!")
        print(f"\nRun the test with:")
        print(f"export AUTH_TOKEN='{token}'")
        print(f"python scripts/test_memory_limits.py")
        return token
    else:
        print(f"❌ Failed to get token: {response.status_code}")
        print(f"Response: {response.text}")
        return None

if __name__ == "__main__":
    get_test_token()