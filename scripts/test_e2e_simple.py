#!/usr/bin/env python3
"""
Simplified E2E Test for Xavigate in Production Mode
"""
import os
import json
import time
import requests
from typing import Dict, Any

# Configuration
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")
BASE_URL = "http://localhost"

# Test user
TEST_USER = {
    "userId": f"e2e-test-{int(time.time())}",
    "username": "e2e_tester", 
    "fullName": "E2E Test User",
    "sessionId": f"e2e-session-{int(time.time())}",
    "traitScores": {
        "openness": 7.5,
        "conscientiousness": 6.0,
        "extraversion": 7.0,
        "agreeableness": 8.0,
        "neuroticism": 4.5
    }
}

class SimpleE2ETest:
    def __init__(self):
        self.headers = {"Content-Type": "application/json"}
        if AUTH_TOKEN:
            self.headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
        self.session_id = TEST_USER["sessionId"]
        self.user_id = TEST_USER["userId"]
        self.results = {}
    
    def test_endpoint(self, name: str, method: str, url: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Test a single endpoint"""
        print(f"\n{'='*60}")
        print(f"Testing: {name}")
        print(f"URL: {url}")
        print(f"Method: {method}")
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            else:
                response = requests.post(url, json=data, headers=self.headers)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Success")
                return {"status": "passed", "data": response.json()}
            else:
                print(f"❌ Failed: {response.text[:200]}")
                return {"status": "failed", "error": f"{response.status_code}: {response.text[:200]}"}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "error", "error": str(e)}
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"🚀 Xavigate E2E Test (Simplified)")
        print(f"{'='*60}")
        print(f"Auth Token: {'Present' if AUTH_TOKEN else 'Missing'}")
        print(f"Session ID: {self.session_id}")
        
        # Test 1: Vector Search (no auth required)
        print(f"\n1️⃣ Vector Search Test")
        result = self.test_endpoint(
            "Vector Search",
            "POST",
            f"{BASE_URL}:8017/search",
            {
                "query": "alignment dynamics",
                "top_k": 3
            }
        )
        self.results["vector_search"] = result
        
        # Test 2: Auth Service Verify
        if AUTH_TOKEN:
            print(f"\n2️⃣ Auth Token Verification")
            result = self.test_endpoint(
                "Auth Verify",
                "POST", 
                f"{BASE_URL}:8014/verify",
                {"key": AUTH_TOKEN}
            )
            self.results["auth_verify"] = result
        
        # Test 3: Memory Save (requires auth in prod)
        print(f"\n3️⃣ Memory Save Test")
        result = self.test_endpoint(
            "Memory Save",
            "POST",
            f"{BASE_URL}:8011/api/memory/save",
            {
                "userId": self.user_id,
                "sessionId": self.session_id,
                "messages": [
                    {"role": "user", "content": "Test message"},
                    {"role": "assistant", "content": "Test response"}
                ]
            }
        )
        self.results["memory_save"] = result
        
        # Test 4: Chat Query (requires auth in prod)
        print(f"\n4️⃣ Chat Query Test")
        result = self.test_endpoint(
            "Chat Query",
            "POST",
            f"{BASE_URL}:8015/query",
            {
                **TEST_USER,
                "message": "Hello, can you help me?"
            }
        )
        self.results["chat_query"] = result
        
        # Test 5: Memory Retrieve
        print(f"\n5️⃣ Memory Retrieve Test")
        result = self.test_endpoint(
            "Memory Get",
            "GET",
            f"{BASE_URL}:8011/api/memory/get/{self.session_id}",
        )
        self.results["memory_get"] = result
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print(f"📊 TEST SUMMARY")
        print(f"{'='*60}")
        
        passed = sum(1 for r in self.results.values() if r.get("status") == "passed")
        total = len(self.results)
        
        for test_name, result in self.results.items():
            status = "✅" if result.get("status") == "passed" else "❌"
            print(f"{status} {test_name}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        
        if passed < total:
            print(f"\n⚠️  Authentication Issues Detected:")
            print(f"The services are in production mode (ENV=prod) and require valid JWT tokens.")
            print(f"Your token may not be valid for this environment.")
            print(f"\nTo fix:")
            print(f"1. Ensure AUTH_TOKEN is a valid Cognito JWT token")
            print(f"2. Check that auth service has Cognito configuration:")
            print(f"   - COGNITO_REGION")
            print(f"   - COGNITO_USER_POOL_ID") 
            print(f"   - COGNITO_APP_CLIENT_ID")
            print(f"3. Or temporarily set ENV=dev in .env file for testing")

if __name__ == "__main__":
    test = SimpleE2ETest()
    test.run_all_tests()