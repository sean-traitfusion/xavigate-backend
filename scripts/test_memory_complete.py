#!/usr/bin/env python3
"""
Complete memory system test that works in both dev and prod modes
"""
import asyncio
import httpx
import os
import sys
from typing import Optional

# Add microservices to path for database access
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'microservices'))

# Configuration
STORAGE_URL = os.getenv("STORAGE_SERVICE_URL", "http://localhost:8011")
CHAT_URL = os.getenv("CHAT_SERVICE_URL", "http://localhost:8015")
ENV = os.getenv("ENV", "dev")

# Test data
TEST_USER = {
    "userId": "test-user-cognito-sub-12345",  # Simulated Cognito sub
    "username": "testuser",
    "fullName": "Test User",
    "sessionId": "test-session-001",
}

print(f"🚀 Xavigate Memory System Complete Test")
print(f"=" * 60)
print(f"🌍 Environment: {ENV}")
print(f"📍 Storage Service: {STORAGE_URL}")
print(f"📍 Chat Service: {CHAT_URL}")
print()

def get_auth_token() -> Optional[str]:
    """Get auth token for prod mode"""
    if ENV == "dev":
        return None
    
    token = os.getenv("COGNITO_TOKEN")
    if not token:
        print("⚠️  No COGNITO_TOKEN found in environment")
        print("   Please enter your Cognito token (or press Enter to skip):")
        token = input("   Token: ").strip()
        if not token:
            print("   Switching to dev mode for testing...")
            global ENV
            ENV = "dev"
            return None
    return token

async def test_storage_endpoints():
    """Test storage service memory endpoints"""
    print("🧪 Testing Storage Service Memory Endpoints")
    print("=" * 60)
    
    auth_token = get_auth_token()
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Save memory
        print("\n1️⃣ Testing memory save...")
        messages = [
            {"role": "user", "content": "Hello, I'm interested in learning about personality traits."},
            {"role": "assistant", "content": "I'd be happy to help you understand personality traits!"},
            {"role": "user", "content": "I've been struggling with procrastination lately."},
            {"role": "assistant", "content": "Procrastination is common. Let's explore strategies based on your traits."},
        ]
        
        save_data = {
            "userId": TEST_USER["userId"],
            "sessionId": TEST_USER["sessionId"],
            "messages": messages
        }
        
        try:
            resp = await client.post(f"{STORAGE_URL}/api/memory/save", json=save_data, headers=headers)
            if resp.status_code == 204:
                print("✅ Memory saved successfully")
            else:
                print(f"❌ Failed to save memory: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"❌ Error saving memory: {e}")
        
        # 2. Get session memory
        print("\n2️⃣ Testing session memory retrieval...")
        try:
            resp = await client.get(f"{STORAGE_URL}/api/memory/get/{TEST_USER['sessionId']}", headers=headers)
            if resp.status_code == 200:
                messages = resp.json()
                print(f"✅ Retrieved {len(messages)} messages from session")
                for msg in messages[:2]:
                    print(f"   - {msg['role']}: {msg['content'][:50]}...")
            else:
                print(f"❌ Failed to get session: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error getting session: {e}")
        
        # 3. Get memory stats
        print("\n3️⃣ Testing memory statistics...")
        try:
            resp = await client.get(f"{STORAGE_URL}/api/memory/memory-stats/{TEST_USER['userId']}", headers=headers)
            if resp.status_code == 200:
                stats = resp.json()
                print("✅ Memory statistics retrieved")
                print(f"   Session: {stats.get('session', {})}")
                print(f"   Compression: {stats.get('compression', {})}")
            else:
                print(f"❌ Failed to get stats: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
        
        # 4. Test runtime config
        print("\n4️⃣ Testing runtime configuration...")
        try:
            resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config", headers=headers)
            if resp.status_code == 200:
                config = resp.json()
                print("✅ Runtime config retrieved:")
                print(f"   - History limit: {config.get('conversation_history_limit')}")
                print(f"   - Top K RAG: {config.get('top_k_rag_hits')}")
            else:
                print(f"❌ Failed to get config: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error getting config: {e}")

async def test_database_persistence():
    """Test if data is persisted in database (prod mode only)"""
    if ENV == "dev":
        print("\n📝 Note: Running in dev mode - using in-memory storage")
        return
    
    print("\n🗄️ Testing Database Persistence")
    print("=" * 60)
    
    try:
        from shared.db import get_connection
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Check session memory
                cur.execute("""
                    SELECT COUNT(*) FROM session_memory 
                    WHERE user_id = %s AND session_id = %s
                """, (TEST_USER["userId"], TEST_USER["sessionId"]))
                
                count = cur.fetchone()[0]
                print(f"✅ Session memory records in database: {count}")
                
                # Check persistent memory
                cur.execute("""
                    SELECT summary FROM persistent_memory 
                    WHERE user_id = %s
                """, (TEST_USER["userId"],))
                
                row = cur.fetchone()
                if row:
                    print(f"✅ Persistent memory found: {len(row[0])} chars")
                else:
                    print("ℹ️  No persistent memory yet (will be created after summarization)")
                    
    except Exception as e:
        print(f"❌ Error checking database: {e}")

async def test_auto_summarization():
    """Test auto-summarization by filling session memory"""
    print("\n🔄 Testing Auto-Summarization")
    print("=" * 60)
    
    auth_token = get_auth_token()
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Clear session first
        print("1️⃣ Clearing session for fresh test...")
        try:
            resp = await client.post(
                f"{STORAGE_URL}/api/memory/expire",
                json={"uuid": TEST_USER["sessionId"]},
                headers=headers
            )
            if resp.status_code == 204:
                print("✅ Session cleared")
        except Exception as e:
            print(f"⚠️  Could not clear session: {e}")
        
        # Add many messages to trigger auto-summarization
        print("\n2️⃣ Adding messages to trigger auto-summarization...")
        large_messages = []
        for i in range(20):
            large_messages.extend([
                {"role": "user", "content": f"Message {i}: " + "This is a long message about personality development. " * 20},
                {"role": "assistant", "content": f"Response {i}: " + "Here's detailed information about your traits. " * 20}
            ])
        
        save_data = {
            "userId": TEST_USER["userId"],
            "sessionId": TEST_USER["sessionId"],
            "messages": large_messages
        }
        
        try:
            resp = await client.post(f"{STORAGE_URL}/api/memory/save", json=save_data, headers=headers)
            if resp.status_code == 204:
                print("✅ Large conversation saved")
            else:
                print(f"❌ Failed to save: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Check if summarization happened
        await asyncio.sleep(2)  # Give it time to process
        
        print("\n3️⃣ Checking for summarization...")
        try:
            resp = await client.get(f"{STORAGE_URL}/api/memory/memory-stats/{TEST_USER['userId']}", headers=headers)
            if resp.status_code == 200:
                stats = resp.json()
                session_stats = stats.get("session", {})
                has_persistent = session_stats.get("has_persistent_memory", False)
                
                if has_persistent:
                    print("✅ Auto-summarization triggered! Persistent memory created.")
                else:
                    print("ℹ️  No auto-summarization yet (may need more messages)")
                    
                print(f"   Session memory: {session_stats.get('session_memory_chars', 0)} chars")
                print(f"   Persistent memory: {session_stats.get('persistent_memory_chars', 0)} chars")
        except Exception as e:
            print(f"❌ Error checking summarization: {e}")

async def test_chat_integration():
    """Test chat service integration if running"""
    print("\n🤖 Testing Chat Service Integration")
    print("=" * 60)
    
    auth_token = get_auth_token()
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    
    # First check if chat service is running
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{CHAT_URL}/health")
            if resp.status_code != 200:
                print("⚠️  Chat service not responding. Skipping chat tests.")
                return
    except:
        print("⚠️  Chat service not running. Skipping chat tests.")
        return
    
    print("✅ Chat service is running")
    
    # Test chat with memory integration
    async with httpx.AsyncClient(timeout=30.0) as client:
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
            "message": "Based on our previous conversation about procrastination, what specific techniques would work best for someone with low conscientiousness?"
        }
        
        try:
            resp = await client.post(
                f"{CHAT_URL}/api/chat/query",
                json=chat_request,
                headers=headers
            )
            
            if resp.status_code == 200:
                result = resp.json()
                print("✅ Chat response received with memory context")
                print(f"   Response: {result['answer'][:200]}...")
                
                if "Checking memory optimization" in str(result):
                    print("✅ Memory optimization working!")
            else:
                print(f"❌ Chat failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"❌ Error calling chat: {e}")

async def main():
    """Run all tests"""
    await test_storage_endpoints()
    await test_database_persistence()
    await test_auto_summarization()
    await test_chat_integration()
    
    print("\n\n✅ Test Complete!")
    print("=" * 60)
    
    if ENV == "dev":
        print("\n📝 To test with database persistence:")
        print("   1. Set ENV=prod in .env file")
        print("   2. Restart storage service")
        print("   3. Run this test again")
    else:
        print("\n📝 To test with a real Cognito token:")
        print("   1. Get a token from your frontend")
        print("   2. Export COGNITO_TOKEN='your-token-here'")
        print("   3. Run this test again")
    
    print("\n🎯 Configuration Dashboard:")
    print("   Run: python scripts/config_dashboard_enhanced.py")
    print("   Access: http://localhost:5001")

if __name__ == "__main__":
    asyncio.run(main())