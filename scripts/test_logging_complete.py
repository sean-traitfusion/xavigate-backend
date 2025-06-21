#!/usr/bin/env python3
"""
Complete test of the logging system with proper authentication
"""

import requests
import json
import time
from datetime import datetime

# Configuration  
CHAT_URL = "http://localhost:8015/query"
STORAGE_URL = "http://localhost:8011"
LOGGING_URL = "http://localhost:8015/admin"

# Your Cognito token (if needed)
AUTH_TOKEN = "YOUR_COGNITO_TOKEN_HERE"  # Replace with actual token if needed

# Test user data
test_user = {
    "userId": f"logging-test-{int(time.time())}",
    "username": "logtester",
    "fullName": "Logging Test User",
    "sessionId": f"logging-session-{int(time.time())}",
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

def test_chat_with_logging():
    print("=== Testing Complete Logging Pipeline ===\n")
    print(f"User ID: {test_user['userId']}")
    print(f"Session ID: {test_user['sessionId']}\n")
    
    headers = {}
    if AUTH_TOKEN and AUTH_TOKEN != "YOUR_COGNITO_TOKEN_HERE":
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
    
    # Send a test message
    message = "Based on my high creativity and empathy scores, what career paths would you recommend?"
    print(f"Sending message: {message}")
    
    payload = {
        **test_user,
        "message": message
    }
    
    try:
        response = requests.post(CHAT_URL, json=payload, headers=headers)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Response received: {result['answer'][:100]}...")
            print(f"✓ Sources: {len(result.get('sources', []))} RAG chunks")
            
            # Wait for async logging to complete
            print("\nWaiting 3 seconds for logs to be processed...")
            time.sleep(3)
            
            # Check the logs
            check_logs(test_user['userId'])
            
        elif response.status_code == 401:
            print("✗ Authentication required. Please set AUTH_TOKEN in the script.")
            print("  ENV is set to 'prod' which requires authentication.")
        else:
            print(f"✗ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"✗ Failed to send message: {e}")

def check_logs(user_id):
    """Check if the logs were saved correctly"""
    print("\n=== Checking Saved Logs ===")
    
    try:
        # Get user's interaction logs
        logs_response = requests.get(f"{STORAGE_URL}/api/logging/interactions/{user_id}?limit=1")
        if logs_response.status_code == 200:
            logs_data = logs_response.json()
            
            if logs_data['interactions']:
                log = logs_data['interactions'][0]
                print(f"\n✓ Log found!")
                print(f"  Interaction ID: {log['interaction_id']}")
                print(f"  Timestamp: {log['timestamp']}")
                print(f"  RAG Context: {'Present' if log.get('rag_context') else 'Empty'}")
                print(f"  Metrics: {log.get('metrics', {})}")
                
                # Check prompt details
                prompts_response = requests.get(f"{STORAGE_URL}/api/logging/prompts/{user_id}?limit=1")
                if prompts_response.status_code == 200:
                    prompts_data = prompts_response.json()
                    if prompts_data['prompts']:
                        prompt = prompts_data['prompts'][0]
                        print(f"\n✓ Prompt details found!")
                        print(f"  System prompt: {'Present' if prompt.get('system_prompt') else 'Empty'}")
                        print(f"  Session context: {'Present' if prompt.get('session_context') else 'Empty'}")
                        print(f"  Persistent summary: {'Present' if prompt.get('persistent_summary') else 'Empty'}")
                        print(f"  Final prompt length: {prompt.get('prompt_length', 0)} chars")
                    else:
                        print("\n✗ No prompt details found")
                else:
                    print(f"\n✗ Failed to get prompt details: {prompts_response.status_code}")
            else:
                print("\n✗ No logs found for this user")
        else:
            print(f"\n✗ Failed to retrieve logs: {logs_response.status_code}")
            
    except Exception as e:
        print(f"\n✗ Error checking logs: {e}")
    
    print(f"\n📊 Check the dashboard at: {LOGGING_URL}")
    print(f"   Look for user ID: {user_id}")

if __name__ == "__main__":
    test_chat_with_logging()