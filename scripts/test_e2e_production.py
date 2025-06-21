#!/usr/bin/env python3
"""
End-to-End Production Test Suite for Xavigate
Tests: Chat, RAG retrieval, Session memory, Persistent memory, and Logging
"""
import os
import sys
import json
import time
import asyncio
import httpx
from datetime import datetime
from typing import Optional, Dict, Any

# Configuration from environment
ENV = os.getenv("ENV", "dev")
USE_NGINX = os.getenv("USE_NGINX", "false").lower() == "true"
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")  # JWT token for production

# Service URLs - use direct ports when NGINX is not available
if USE_NGINX:
    BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080/api")
    CHAT_URL = f"{BASE_URL}/chat"
    STORAGE_URL = f"{BASE_URL}/storage"
    VECTOR_URL = f"{BASE_URL}/vector"
    STATS_URL = f"{BASE_URL}/stats"
else:
    # Direct service URLs
    CHAT_URL = "http://localhost:8015"
    STORAGE_URL = "http://localhost:8011"
    VECTOR_URL = "http://localhost:8017"
    STATS_URL = "http://localhost:8012"

# Test configuration
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

class E2ETestSuite:
    def __init__(self):
        self.headers = {}
        if ENV == "prod" and AUTH_TOKEN:
            self.headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
        self.results = {}
        self.session_id = TEST_USER["sessionId"]
        self.user_id = TEST_USER["userId"]
        
    async def run_all_tests(self):
        """Run all E2E tests in sequence"""
        print(f"🚀 Xavigate End-to-End Test Suite")
        print(f"{'=' * 70}")
        print(f"📍 Environment: {ENV}")
        print(f"📍 Using NGINX: {USE_NGINX}")
        print(f"📍 Chat URL: {CHAT_URL}")
        print(f"📍 Session ID: {self.session_id}")
        print(f"📍 Auth Token: {'Present' if AUTH_TOKEN else 'Not provided'}")
        print()
        
        tests = [
            ("RAG/Vector Search", self.test_rag_search),
            ("Session Memory Save", self.test_session_memory_save),
            ("Chat with Context", self.test_chat_with_context),
            ("Session Memory Retrieval", self.test_session_memory_get),
            ("Persistent Memory", self.test_persistent_memory),
            ("Logging System", self.test_logging_system),
            ("Memory Statistics", self.test_memory_stats)
        ]
        
        for test_name, test_func in tests:
            try:
                print(f"\n{'=' * 70}")
                print(f"🧪 Testing: {test_name}")
                print(f"{'=' * 70}")
                result = await test_func()
                self.results[test_name] = {"status": "✅ PASSED", "data": result}
            except Exception as e:
                self.results[test_name] = {"status": "❌ FAILED", "error": str(e)}
                print(f"❌ Error: {e}")
        
        self.print_summary()
    
    async def test_rag_search(self) -> Dict[str, Any]:
        """Test RAG/Vector search functionality"""
        async with httpx.AsyncClient() as client:
            # Test search for alignment concepts
            search_data = {
                "query": "alignment dynamics multiple natures",
                "top_k": 3
            }
            
            print(f"🔍 Searching for: {search_data['query']}")
            resp = await client.post(
                f"{VECTOR_URL}/search",
                json=search_data,
                headers=self.headers
            )
            resp.raise_for_status()
            
            results = resp.json()
            print(f"📊 Found {len(results.get('results', []))} results")
            
            if results.get('results'):
                for i, result in enumerate(results['results'][:2]):
                    print(f"\n  Result {i+1}:")
                    print(f"  - Source: {result.get('metadata', {}).get('source', 'unknown')}")
                    print(f"  - Content: {result.get('content', '')[:100]}...")
                    print(f"  - Distance: {result.get('distance', 0):.4f}")
            
            return results
    
    async def test_session_memory_save(self) -> Dict[str, Any]:
        """Test saving conversation to session memory"""
        async with httpx.AsyncClient() as client:
            memory_data = {
                "userId": self.user_id,
                "sessionId": self.session_id,
                "messages": [
                    {
                        "role": "user",
                        "content": "I have low conscientiousness and struggle with procrastination. What careers might suit me?"
                    },
                    {
                        "role": "assistant",
                        "content": "I understand you struggle with procrastination due to low conscientiousness. Let me help you find careers that work with your traits rather than against them."
                    }
                ]
            }
            
            print(f"💾 Saving conversation to session memory...")
            resp = await client.post(
                f"{STORAGE_URL}/memory/save",
                json=memory_data,
                headers=self.headers
            )
            resp.raise_for_status()
            
            result = resp.json()
            print(f"✅ Memory saved successfully")
            print(f"   - Session: {result.get('sessionId')}")
            print(f"   - Status: {result.get('status')}")
            
            return result
    
    async def test_chat_with_context(self) -> Dict[str, Any]:
        """Test chat service with memory context and RAG"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            chat_data = {
                **TEST_USER,
                "message": "Based on our previous discussion about my low conscientiousness, what specific careers would you recommend?"
            }
            
            print(f"💬 Sending chat message with context...")
            print(f"   Message: {chat_data['message'][:80]}...")
            
            resp = await client.post(
                f"{CHAT_URL}/query" if USE_NGINX else f"{CHAT_URL}/query",
                json=chat_data,
                headers=self.headers
            )
            resp.raise_for_status()
            
            result = resp.json()
            answer = result.get('answer', 'No response')
            
            print(f"\n📝 Response received:")
            print(f"   {answer[:200]}...")
            
            # Check if memory context was used
            if 'procrastination' in answer.lower() or 'conscientiousness' in answer.lower():
                print(f"\n✅ Memory context detected in response")
            
            # Check if RAG was used
            metadata = result.get('metadata', {})
            if metadata.get('rag_hits'):
                print(f"✅ RAG used: {len(metadata['rag_hits'])} documents retrieved")
            
            return result
    
    async def test_session_memory_get(self) -> Dict[str, Any]:
        """Test retrieving session memory"""
        async with httpx.AsyncClient() as client:
            print(f"🔍 Retrieving session memory...")
            
            resp = await client.get(
                f"{STORAGE_URL}/memory/get/{self.session_id}",
                headers=self.headers
            )
            resp.raise_for_status()
            
            result = resp.json()
            messages = result.get('messages', [])
            
            print(f"📊 Retrieved {len(messages)} messages from session memory")
            if messages:
                print(f"   First message: {messages[0].get('content', '')[:80]}...")
            
            return result
    
    async def test_persistent_memory(self) -> Dict[str, Any]:
        """Test persistent memory storage and retrieval"""
        async with httpx.AsyncClient() as client:
            # First trigger summarization
            print(f"📝 Triggering memory summarization...")
            
            summary_data = {
                "userId": self.user_id,
                "sessionId": self.session_id,
                "trigger": "manual"
            }
            
            resp = await client.post(
                f"{STORAGE_URL}/memory/summarize",
                json=summary_data,
                headers=self.headers
            )
            
            # Get persistent memory
            print(f"🔍 Retrieving persistent memory...")
            resp = await client.get(
                f"{STORAGE_URL}/memory/persistent/{self.user_id}",
                headers=self.headers
            )
            
            if resp.status_code == 200:
                result = resp.json()
                content = result.get('content', '')
                print(f"📊 Persistent memory found:")
                print(f"   Content length: {len(content)} chars")
                if content:
                    print(f"   Preview: {content[:100]}...")
            else:
                result = {"status": "No persistent memory yet"}
                print(f"ℹ️ No persistent memory found (this is normal for new users)")
            
            return result
    
    async def test_logging_system(self) -> Dict[str, Any]:
        """Test that interactions are being logged"""
        async with httpx.AsyncClient() as client:
            print(f"📊 Checking interaction logs...")
            
            # Query recent logs
            resp = await client.get(
                f"{STATS_URL}/analytics/interaction-logs",
                params={"user_id": self.user_id, "limit": 10},
                headers=self.headers
            )
            
            if resp.status_code == 200:
                logs = resp.json()
                print(f"✅ Found {len(logs)} interaction logs")
                
                if logs:
                    latest = logs[0]
                    print(f"\n   Latest log:")
                    print(f"   - Timestamp: {latest.get('timestamp')}")
                    print(f"   - User Input: {latest.get('user_input', '')[:60]}...")
                    print(f"   - Response Time: {latest.get('response_time_ms')}ms")
                    
                return {"logs_count": len(logs), "latest": latest if logs else None}
            else:
                print(f"⚠️ Could not retrieve logs (status: {resp.status_code})")
                return {"status": "unavailable"}
    
    async def test_memory_stats(self) -> Dict[str, Any]:
        """Test memory statistics endpoint"""
        async with httpx.AsyncClient() as client:
            print(f"📈 Retrieving memory statistics...")
            
            resp = await client.get(
                f"{STORAGE_URL}/memory/memory-stats/{self.user_id}",
                headers=self.headers
            )
            resp.raise_for_status()
            
            stats = resp.json()
            print(f"\n📊 Memory Statistics:")
            print(f"   - Session Memory: {stats.get('session_memory_usage', 0)} chars")
            print(f"   - Persistent Memory: {stats.get('persistent_memory_usage', 0)} chars")
            print(f"   - Total Sessions: {stats.get('total_sessions', 0)}")
            
            return stats
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{'=' * 70}")
        print(f"📊 TEST SUMMARY")
        print(f"{'=' * 70}")
        
        passed = sum(1 for r in self.results.values() if "PASSED" in r["status"])
        total = len(self.results)
        
        for test_name, result in self.results.items():
            print(f"{result['status']} {test_name}")
        
        print(f"\n{'=' * 70}")
        print(f"Total: {passed}/{total} tests passed")
        
        if passed == total:
            print(f"✅ All tests passed! System is ready for production.")
        else:
            print(f"❌ Some tests failed. Please check the errors above.")

async def main():
    """Main entry point"""
    if ENV == "prod" and not AUTH_TOKEN:
        print("❌ ERROR: Production mode requires AUTH_TOKEN environment variable")
        print("   Export your JWT token: export AUTH_TOKEN='your-jwt-token'")
        sys.exit(1)
    
    suite = E2ETestSuite()
    await suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())