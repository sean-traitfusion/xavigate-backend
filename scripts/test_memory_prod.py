#!/usr/bin/env python3
"""
Production memory test with proper authentication handling
"""
import requests
import json
import os
import sys

# Configuration
STORAGE_URL = "http://localhost:8011"
CHAT_URL = "http://localhost:8015"

# Test data
TEST_USER = {
    "userId": "test-user-cognito-sub-12345",
    "username": "testuser",
    "fullName": "Test User",
    "sessionId": "test-session-001",
}

def test_memory_with_auth(token):
    """Test memory system with authentication"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🧪 Testing with Authentication")
    print("=" * 60)
    
    # 1. Save memory
    print("\n1️⃣ Saving memory...")
    messages = [
        {"role": "user", "content": "Hello, I need help with procrastination."},
        {"role": "assistant", "content": "I can help you with strategies for procrastination based on your personality traits."},
        {"role": "user", "content": "I have low conscientiousness and high openness."},
        {"role": "assistant", "content": "With low conscientiousness and high openness, you might benefit from flexible, creative approaches to productivity."},
    ]
    
    save_data = {
        "userId": TEST_USER["userId"],
        "sessionId": TEST_USER["sessionId"],
        "messages": messages
    }
    
    try:
        resp = requests.post(f"{STORAGE_URL}/api/memory/save", json=save_data, headers=headers)
        if resp.status_code == 204:
            print("✅ Memory saved to database!")
        else:
            print(f"❌ Save failed: {resp.status_code} - {resp.text}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # 2. Retrieve memory
    print("\n2️⃣ Retrieving memory...")
    try:
        resp = requests.get(f"{STORAGE_URL}/api/memory/get/{TEST_USER['sessionId']}", headers=headers)
        if resp.status_code == 200:
            saved_messages = resp.json()
            print(f"✅ Retrieved {len(saved_messages)} messages from database")
            
            # Show the last few messages
            print("\n📝 Recent messages:")
            for msg in saved_messages[-4:]:
                print(f"   {msg['role']}: {msg['content'][:60]}...")
        else:
            print(f"❌ Retrieve failed: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Check memory stats
    print("\n3️⃣ Checking memory statistics...")
    try:
        resp = requests.get(f"{STORAGE_URL}/api/memory/memory-stats/{TEST_USER['userId']}", headers=headers)
        if resp.status_code == 200:
            stats = resp.json()
            session_stats = stats.get("session", {})
            
            print("✅ Memory statistics:")
            print(f"   Session memory: {session_stats.get('session_memory_chars', 0)} chars")
            print(f"   Usage: {session_stats.get('session_memory_usage_percent', 0):.1f}%")
            print(f"   Has persistent memory: {session_stats.get('has_persistent_memory', False)}")
        else:
            print(f"❌ Stats failed: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Test chat with memory context
    print("\n4️⃣ Testing chat with memory context...")
    chat_request = {
        "userId": TEST_USER["userId"],
        "username": TEST_USER["username"],
        "fullName": TEST_USER["fullName"],
        "sessionId": TEST_USER["sessionId"],
        "traitScores": {
            "openness": 8.0,
            "conscientiousness": 3.0,
            "extraversion": 6.0,
            "agreeableness": 7.0,
            "neuroticism": 5.0
        },
        "message": "Can you remind me what we discussed about my procrastination issue?"
    }
    
    try:
        resp = requests.post(f"{CHAT_URL}/query", json=chat_request, headers=headers, timeout=30)
        if resp.status_code == 200:
            result = resp.json()
            print("✅ Chat response with memory context:")
            print(f"   {result['answer'][:200]}...")
        else:
            print(f"❌ Chat failed: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🚀 Xavigate Production Memory Test")
    print("=" * 60)
    
    # Check if running in prod mode
    resp = requests.get(f"{STORAGE_URL}/openapi.json")
    if "/api/storage" in resp.text:
        print("✅ Storage service is running in PRODUCTION mode")
    else:
        print("⚠️  Storage service is in DEV mode. Set ENV=prod and restart services.")
        return
    
    # Get token
    token = os.getenv("COGNITO_TOKEN", "")
    
    if not token:
        print("\n🔐 Authentication Required")
        print("=" * 60)
        print("Please enter your Cognito token:")
        print("(Get this from your browser DevTools after logging in)")
        token = input("Token: ").strip()
        
        if not token:
            print("\n❌ No token provided. Cannot test in production mode.")
            print("\nTo get a token:")
            print("1. Log into your Xavigate frontend")
            print("2. Open DevTools (F12)")
            print("3. Go to Network tab")
            print("4. Find an API call with Authorization header")
            print("5. Copy the token after 'Bearer '")
            return
    
    # Test the token
    print("\n🔑 Testing authentication...")
    test_resp = requests.get(
        f"{STORAGE_URL}/api/memory/runtime-config",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if test_resp.status_code == 401:
        print("❌ Invalid token. Please check your token and try again.")
        return
    elif test_resp.status_code == 200:
        print("✅ Authentication successful!")
    else:
        print(f"⚠️  Unexpected response: {test_resp.status_code}")
    
    # Run tests
    test_memory_with_auth(token)
    
    print("\n\n✅ Test complete!")
    print("\n📊 What to check:")
    print("1. Database should now have session_memory records")
    print("2. Memory stats should show actual usage")
    print("3. Chat responses should reference previous conversation")
    print("\n🎯 Configuration Dashboard: http://localhost:5001")

if __name__ == "__main__":
    main()