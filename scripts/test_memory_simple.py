#!/usr/bin/env python3
"""
Simple memory test that works with Docker setup
"""
import requests
import json
import os

# Configuration
STORAGE_URL = "http://localhost:8011"
CHAT_URL = "http://localhost:8015"  # Chat service port in Docker

# Test data
TEST_USER = {
    "userId": "test-user-cognito-sub-12345",
    "username": "testuser",
    "fullName": "Test User",
    "sessionId": "test-session-001",
}

def main():
    print("🚀 Testing Xavigate Memory System")
    print("=" * 60)
    
    # Get token if needed
    token = os.getenv("COGNITO_TOKEN", "")
    headers = {}
    
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Using Cognito token for authentication")
        print(f"   Token preview: {token[:20]}...{token[-10:]}")
    else:
        print("ℹ️  No token provided, testing without authentication")
        print("   Set COGNITO_TOKEN environment variable to test with auth")
    
    # 1. Test health endpoint
    print("\n1️⃣ Testing storage service health...")
    try:
        resp = requests.get(f"{STORAGE_URL}/health")
        if resp.status_code == 200:
            print(f"✅ Storage service is running: {resp.json()}")
        else:
            print(f"❌ Storage service error: {resp.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to storage service: {e}")
        return
    
    # 2. Save memory
    print("\n2️⃣ Testing memory save...")
    messages = [
        {"role": "user", "content": "Hello, I need help with procrastination."},
        {"role": "assistant", "content": "I can help you with strategies for procrastination."},
    ]
    
    save_data = {
        "userId": TEST_USER["userId"],
        "sessionId": TEST_USER["sessionId"],
        "messages": messages
    }
    
    try:
        resp = requests.post(
            f"{STORAGE_URL}/api/memory/save",
            json=save_data,
            headers=headers
        )
        if resp.status_code == 204:
            print("✅ Memory saved successfully")
        else:
            print(f"❌ Failed to save: {resp.status_code}")
            print(f"   Response: {resp.text}")
    except Exception as e:
        print(f"❌ Error saving: {e}")
    
    # 3. Get memory
    print("\n3️⃣ Testing memory retrieval...")
    try:
        resp = requests.get(
            f"{STORAGE_URL}/api/memory/get/{TEST_USER['sessionId']}",
            headers=headers
        )
        if resp.status_code == 200:
            messages = resp.json()
            print(f"✅ Retrieved {len(messages)} messages")
            for msg in messages[-2:]:  # Show last 2
                print(f"   - {msg['role']}: {msg['content']}")
        else:
            print(f"❌ Failed to retrieve: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error retrieving: {e}")
    
    # 4. Check runtime config
    print("\n4️⃣ Checking runtime configuration...")
    try:
        resp = requests.get(
            f"{STORAGE_URL}/api/memory/runtime-config",
            headers=headers
        )
        if resp.status_code == 200:
            config = resp.json()
            print("✅ Runtime config:")
            print(f"   {json.dumps(config, indent=2)}")
        else:
            print(f"❌ Failed to get config: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error getting config: {e}")
    
    # 5. Test chat service
    print("\n5️⃣ Testing chat service...")
    try:
        resp = requests.get(f"{CHAT_URL}/health")
        if resp.status_code == 200:
            print(f"✅ Chat service is running: {resp.json()}")
            
            # Try a chat request
            chat_request = {
                "userId": TEST_USER["userId"],
                "username": TEST_USER["username"],
                "fullName": TEST_USER["fullName"],
                "sessionId": TEST_USER["sessionId"],
                "traitScores": {
                    "openness": 7.5,
                    "conscientiousness": 4.0,
                    "extraversion": 6.0,
                    "agreeableness": 7.0,
                    "neuroticism": 5.0
                },
                "message": "What specific techniques help with procrastination for someone with low conscientiousness?"
            }
            
            print("\n   Sending chat request...")
            chat_resp = requests.post(
                f"{CHAT_URL}/query",
                json=chat_request,
                headers=headers,
                timeout=30
            )
            
            if chat_resp.status_code == 200:
                result = chat_resp.json()
                print("✅ Chat response received!")
                print(f"   Answer preview: {result['answer'][:150]}...")
            else:
                print(f"❌ Chat failed: {chat_resp.status_code}")
                print(f"   Response: {chat_resp.text}")
                
        else:
            print(f"❌ Chat service not responding: {resp.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to chat service: {e}")
    
    print("\n\n✅ Test complete!")
    print("\n📝 Configuration Dashboard: http://localhost:5001")

if __name__ == "__main__":
    main()