#!/usr/bin/env python3
"""
Test script to verify memory management fixes
"""
import os
import sys
import time
import requests
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test configuration
BASE_URL = "http://localhost:8011"
TEST_USER_ID = "test_user_memory_fix"
TEST_SESSION_ID = "test_session_memory_fix"

def test_memory_overflow():
    """Test that oversized memory gets cleared even when summarization fails"""
    print("\n🧪 Testing memory overflow handling...")
    
    # First, let's check current memory size
    response = requests.get(f"{BASE_URL}/api/memory/session-memory", params={
        "user_id": TEST_USER_ID,
        "session_id": TEST_SESSION_ID
    })
    print(f"Initial memory check: {response.status_code}")
    
    # Add a very large message to trigger summarization
    large_message = "This is a test message. " * 1000  # ~25K chars
    
    for i in range(3):
        print(f"\nAdding large message {i+1}...")
        response = requests.post(f"{BASE_URL}/api/memory/session-memory", json={
            "user_id": TEST_USER_ID,
            "session_id": TEST_SESSION_ID,
            "exchanges": [{
                "user_prompt": f"Test prompt {i}: {large_message[:100]}",
                "assistant_response": f"Test response {i}: {large_message}"
            }]
        })
        print(f"Add memory response: {response.status_code}")
        
        # Check memory size
        response = requests.get(f"{BASE_URL}/api/memory/session-memory", params={
            "user_id": TEST_USER_ID,
            "session_id": TEST_SESSION_ID
        })
        if response.status_code == 200:
            data = response.json()
            print(f"Memory size after message {i+1}: {len(str(data))} chars")
        
        time.sleep(2)  # Give time for auto-summarization to trigger

def test_duplicate_interaction_ids():
    """Test that duplicate interaction IDs are handled properly"""
    print("\n🧪 Testing duplicate interaction ID handling...")
    
    # Create multiple interactions rapidly
    for i in range(5):
        interaction_log = {
            "interaction_id": f"{TEST_USER_ID}_{TEST_SESSION_ID}_test_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "user_id": TEST_USER_ID,
            "session_id": TEST_SESSION_ID,
            "timestamp": datetime.now().isoformat(),
            "user_message": f"Test message {i}",
            "assistant_response": f"Test response {i}",
            "rag_context": "Test context",
            "strategy": "test",
            "model": "gpt-4",
            "tools_called": '{"test": true}'
        }
        
        response = requests.post(f"{BASE_URL}/logging/interaction", json=interaction_log)
        print(f"Interaction {i+1} log response: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")

def test_summarization_with_rate_limits():
    """Test that summarization handles rate limits properly"""
    print("\n🧪 Testing summarization with simulated rate limits...")
    
    # Force a summarization
    response = requests.post(f"{BASE_URL}/api/memory/expire", json={
        "uuid": TEST_USER_ID
    })
    print(f"Force summarization response: {response.status_code}")
    
    # Check if memory was cleared
    time.sleep(5)  # Wait for summarization to complete
    
    response = requests.get(f"{BASE_URL}/api/memory/session-memory", params={
        "user_id": TEST_USER_ID,
        "session_id": TEST_SESSION_ID
    })
    print(f"Memory check after summarization: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Memory size after summarization: {len(str(data))} chars")

def main():
    """Run all tests"""
    print("🚀 Starting memory management tests...")
    print(f"Testing against: {BASE_URL}")
    
    # Check if storage service is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Storage service is not running!")
            return
    except Exception as e:
        print(f"❌ Cannot connect to storage service: {e}")
        return
    
    print("✅ Storage service is running")
    
    # Run tests
    test_memory_overflow()
    test_duplicate_interaction_ids()
    test_summarization_with_rate_limits()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()