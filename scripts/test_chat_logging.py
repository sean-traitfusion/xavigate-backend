#!/usr/bin/env python3
"""
Test script for chat logging functionality
"""

import requests
import json
import time
from datetime import datetime

# Configuration  
CHAT_URL = "http://localhost:8015/query"
STORAGE_URL = "http://localhost:8011"

# Test user data
test_user = {
    "userId": "test-user-123",
    "username": "testuser",
    "fullName": "Test User",
    "sessionId": f"test-session-{int(time.time())}",
    "traitScores": {
        "creativity": 8.5,
        "analytical_thinking": 7.2,
        "empathy": 9.0,
        "leadership": 6.5,
        "adaptability": 7.8,
        "communication": 8.0,
        "problem_solving": 7.5,
        "teamwork": 8.2,
        "attention_to_detail": 6.8,
        "time_management": 7.0,
        "stress_management": 6.5,
        "decision_making": 7.3,
        "innovation": 8.0,
        "persistence": 7.5,
        "emotional_intelligence": 8.5,
        "critical_thinking": 7.8,
        "flexibility": 7.2,
        "initiative": 7.0,
        "integrity": 9.0
    }
}

# Test messages
test_messages = [
    "What are my greatest strengths based on my trait scores?",
    "How can I improve my stress management skills?",
    "Tell me about leadership development strategies.",
]

def test_chat_logging():
    print("=== Testing Chat Logging System ===\n")
    
    # Send test messages
    for i, message in enumerate(test_messages):
        print(f"\n[{i+1}] Sending message: {message}")
        
        payload = {
            **test_user,
            "message": message
        }
        
        try:
            response = requests.post(CHAT_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Response received: {result['answer'][:100]}...")
                time.sleep(1)  # Give logging time to complete
            else:
                print(f"✗ Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"✗ Failed to send message: {e}")
    
    # Wait a moment for async logging to complete
    print("\n\nWaiting for logs to be processed...")
    time.sleep(2)
    
    # Check if logs were saved
    print("\n=== Checking Saved Logs ===\n")
    
    try:
        # Get interaction logs
        logs_response = requests.get(f"{STORAGE_URL}/api/logging/all-interactions?limit=10")
        if logs_response.status_code == 200:
            logs_data = logs_response.json()
            print(f"✓ Found {logs_data['total']} total logs")
            
            # Display recent logs
            for log in logs_data['interactions'][:3]:
                print(f"\n- Log ID: {log['interaction_id']}")
                print(f"  User: {log['user_id']}")
                print(f"  Time: {log['timestamp']}")
                print(f"  Message: {log['user_message'][:50]}...")
                print(f"  Response: {log['assistant_response'][:50]}...")
                print(f"  RAG Context: {'Yes' if log.get('rag_context') else 'No'}")
                print(f"  Metrics: {log.get('metrics', {})}")
        else:
            print(f"✗ Failed to retrieve logs: {logs_response.status_code}")
    except Exception as e:
        print(f"✗ Error checking logs: {e}")

if __name__ == "__main__":
    test_chat_logging()