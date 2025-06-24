#!/usr/bin/env python3
"""
Test script to verify memory limits are enforced
"""
import requests
import time
import sys

BASE_URL = "http://localhost:8011"
TEST_USER = "test_memory_limit_user"
TEST_SESSION = "test_memory_limit_session"

def test_memory_limits():
    """Test that memory limits are properly enforced"""
    
    print("🧪 Testing memory limit enforcement...")
    print(f"Test user: {TEST_USER}")
    print(f"Test session: {TEST_SESSION}\n")
    
    # Create a large message (2K chars each)
    large_message = "This is a test message that simulates a long conversation. " * 35
    
    print(f"📝 Each message is ~{len(large_message)} chars")
    print("📊 Memory limit is 15,000 chars (should trigger at ~10,500 chars / 70%)\n")
    
    for i in range(10):  # This should trigger summarization around message 5-6
        print(f"\n--- Message {i+1} ---")
        
        # Check current memory size
        try:
            response = requests.get(f"{BASE_URL}/api/memory/session-memory", params={
                "user_id": TEST_USER,
                "session_id": TEST_SESSION
            })
            
            if response.status_code == 200:
                current_memory = response.json()
                current_size = sum(len(msg.get("user_prompt", "")) + len(msg.get("assistant_response", "")) 
                                 for msg in current_memory.get("exchanges", []))
                print(f"📏 Current memory size: {current_size:,} chars")
        except:
            print("⚠️ Could not check memory size")
        
        # Add new interaction
        print(f"➕ Adding message {i+1}...")
        response = requests.post(f"{BASE_URL}/api/memory/session-memory", json={
            "user_id": TEST_USER,
            "session_id": TEST_SESSION,
            "exchanges": [{
                "user_prompt": f"Test question {i+1}: {large_message}",
                "assistant_response": f"Test response {i+1}: {large_message}"
            }]
        })
        
        if response.status_code == 200:
            print("✅ Message added successfully")
        else:
            print(f"❌ Error adding message: {response.status_code}")
            print(f"   Response: {response.text}")
        
        # Give time for auto-summarization to trigger
        time.sleep(2)
        
        # Check if summarization happened
        try:
            response = requests.get(f"{BASE_URL}/api/memory/session-memory", params={
                "user_id": TEST_USER,
                "session_id": TEST_SESSION
            })
            
            if response.status_code == 200:
                new_memory = response.json()
                new_size = sum(len(msg.get("user_prompt", "")) + len(msg.get("assistant_response", "")) 
                             for msg in new_memory.get("exchanges", []))
                
                if new_size < current_size:
                    print(f"🎉 SUMMARIZATION TRIGGERED! Memory reduced from {current_size:,} to {new_size:,} chars")
                    break
        except:
            pass
    
    # Final check
    print("\n📊 Final memory check:")
    response = requests.get(f"{BASE_URL}/api/memory/session-memory", params={
        "user_id": TEST_USER,
        "session_id": TEST_SESSION
    })
    
    if response.status_code == 200:
        final_memory = response.json()
        final_size = sum(len(msg.get("user_prompt", "")) + len(msg.get("assistant_response", "")) 
                       for msg in final_memory.get("exchanges", []))
        print(f"✅ Final memory size: {final_size:,} chars")
        
        if final_size > 20000:
            print("❌ TEST FAILED: Memory exceeded 20K limit!")
            return False
        else:
            print("✅ TEST PASSED: Memory stayed within limits!")
            return True
    
    return False

def cleanup_test_session():
    """Clean up test session"""
    print("\n🧹 Cleaning up test session...")
    response = requests.post(f"{BASE_URL}/api/memory/expire", json={
        "uuid": TEST_USER
    })
    print(f"Cleanup response: {response.status_code}")

if __name__ == "__main__":
    print("🚀 Memory Limit Test\n")
    
    # Check if storage service is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Storage service is not running!")
            sys.exit(1)
    except:
        print("❌ Cannot connect to storage service!")
        sys.exit(1)
    
    print("✅ Storage service is running\n")
    
    # Run test
    success = test_memory_limits()
    
    # Cleanup
    cleanup_test_session()
    
    if success:
        print("\n✅ All tests passed! Memory limits are working correctly.")
    else:
        print("\n❌ Tests failed! Memory limits may not be working correctly.")
        sys.exit(1)