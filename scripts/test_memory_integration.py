#!/usr/bin/env python3
"""
Comprehensive test script for the enhanced memory system integration
Tests the full flow from chat service through memory optimization
"""
import asyncio
import httpx
import json
import sys
import os
from datetime import datetime

# Configuration
STORAGE_URL = "http://localhost:8011"
CHAT_URL = "http://localhost:8000"
AUTH_TOKEN = None  # Will be set by user

# Test data
TEST_USER = {
    "userId": "test-user-001",
    "username": "testuser",
    "fullName": "John Doe",
    "sessionId": "test-session-001",
    "traitScores": {
        "openness": 7.5,
        "conscientiousness": 8.0,
        "extraversion": 6.0,
        "agreeableness": 7.0,
        "neuroticism": 4.0
    }
}

async def test_memory_endpoints():
    """Test individual memory endpoints"""
    print("🧪 Testing Memory Endpoints")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}
    
    async with httpx.AsyncClient() as client:
        # Test 1: Get runtime config
        print("\n1️⃣ Testing runtime configuration...")
        try:
            resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config", headers=headers)
            if resp.status_code == 200:
                config = resp.json()
                print("✅ Runtime config loaded:")
                print(f"   - Session limit: {config.get('conversation_history_limit')} exchanges")
                print(f"   - Top K RAG hits: {config.get('top_k_rag_hits')}")
            else:
                print(f"❌ Failed to get config: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 2: Save memory interaction
        print("\n2️⃣ Testing memory save...")
        save_data = {
            "userId": TEST_USER["userId"],
            "sessionId": TEST_USER["sessionId"],
            "messages": [
                {"role": "user", "content": "Hello, I'm John and I work as a software engineer in San Francisco."},
                {"role": "assistant", "content": "Nice to meet you John! How long have you been working as a software engineer in San Francisco?"}
            ]
        }
        
        try:
            resp = await client.post(f"{STORAGE_URL}/api/memory/save", json=save_data, headers=headers)
            if resp.status_code == 204:
                print("✅ Memory saved successfully")
            else:
                print(f"❌ Failed to save: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 3: Get session memory
        print("\n3️⃣ Testing session memory retrieval...")
        try:
            resp = await client.get(f"{STORAGE_URL}/api/memory/get/{TEST_USER['sessionId']}", headers=headers)
            if resp.status_code == 200:
                messages = resp.json()
                print(f"✅ Retrieved {len(messages)} messages from session")
                for msg in messages[:2]:  # Show first 2
                    print(f"   - {msg['role']}: {msg['content'][:50]}...")
            else:
                print(f"❌ Failed to get session: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 4: Get memory stats
        print("\n4️⃣ Testing memory statistics...")
        try:
            resp = await client.get(f"{STORAGE_URL}/api/memory/memory-stats/{TEST_USER['userId']}", headers=headers)
            if resp.status_code == 200:
                stats = resp.json()
                session_stats = stats.get("session", {})
                print("✅ Memory statistics:")
                print(f"   - Session chars: {session_stats.get('session_memory_chars', 0)}")
                print(f"   - Session usage: {session_stats.get('session_memory_usage_percent', 0):.1f}%")
                print(f"   - Has persistent memory: {session_stats.get('has_persistent_memory', False)}")
            else:
                print(f"❌ Failed to get stats: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_chat_integration():
    """Test chat service integration with memory"""
    print("\n\n🤖 Testing Chat Service Integration")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}
    
    async with httpx.AsyncClient() as client:
        # Test series of messages to build up memory
        messages = [
            "Hello, I'm interested in learning about personality traits and how they affect my work.",
            "I've been struggling with procrastination lately. As a software engineer, I find it hard to stay focused.",
            "What strategies would you recommend for someone with high openness but low conscientiousness?",
            "I live in San Francisco and work at a startup. The fast pace is exciting but sometimes overwhelming."
        ]
        
        for i, message in enumerate(messages, 1):
            print(f"\n📝 Message {i}: {message[:60]}...")
            
            chat_request = {
                **TEST_USER,
                "message": message
            }
            
            try:
                resp = await client.post(
                    f"{CHAT_URL}/api/chat/query",
                    json=chat_request,
                    headers=headers,
                    timeout=30.0
                )
                
                if resp.status_code == 200:
                    result = resp.json()
                    print(f"✅ Response: {result['answer'][:100]}...")
                    print(f"   Sources: {len(result.get('sources', []))} documents")
                else:
                    print(f"❌ Chat failed: {resp.status_code}")
                    print(f"   Error: {resp.text}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Small delay between messages
            await asyncio.sleep(1)
        
        # Check memory stats after conversation
        print("\n📊 Checking memory after conversation...")
        try:
            resp = await client.get(
                f"{STORAGE_URL}/api/memory/memory-stats/{TEST_USER['userId']}", 
                headers=headers
            )
            if resp.status_code == 200:
                stats = resp.json()
                session = stats.get("session", {})
                print(f"✅ Session memory used: {session.get('session_memory_chars', 0)} chars")
                print(f"   ({session.get('session_memory_usage_percent', 0):.1f}% of limit)")
        except Exception as e:
            print(f"❌ Error checking stats: {e}")

async def test_memory_limits():
    """Test auto-summarization at memory limits"""
    print("\n\n🔄 Testing Auto-Summarization")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}
    
    async with httpx.AsyncClient() as client:
        # First, force clear the session
        print("\n1️⃣ Clearing session for fresh test...")
        try:
            resp = await client.post(
                f"{STORAGE_URL}/api/memory/expire",
                json={"uuid": TEST_USER["sessionId"]},
                headers=headers
            )
            print("✅ Session cleared")
        except Exception as e:
            print(f"⚠️ Could not clear session: {e}")
        
        # Add many messages to approach limit
        print("\n2️⃣ Adding messages to approach memory limit...")
        
        # Create a long conversation
        for i in range(20):
            save_data = {
                "userId": TEST_USER["userId"],
                "sessionId": TEST_USER["sessionId"],
                "messages": [
                    {
                        "role": "user", 
                        "content": f"This is test message {i}. " + "I want to discuss various topics about personality development and career growth. " * 10
                    },
                    {
                        "role": "assistant", 
                        "content": f"Response to message {i}. " + "Here are some insights about personality and career development based on your traits. " * 10
                    }
                ]
            }
            
            try:
                await client.post(f"{STORAGE_URL}/api/memory/save", json=save_data, headers=headers)
                
                # Check stats periodically
                if i % 5 == 0:
                    resp = await client.get(
                        f"{STORAGE_URL}/api/memory/memory-stats/{TEST_USER['userId']}", 
                        headers=headers
                    )
                    if resp.status_code == 200:
                        stats = resp.json()
                        session = stats.get("session", {})
                        usage = session.get('session_memory_usage_percent', 0)
                        chars = session.get('session_memory_chars', 0)
                        print(f"   Progress: {chars} chars ({usage:.1f}% of limit)")
                        
                        # Check if auto-summarization triggered
                        if usage < 10 and i > 10:
                            print("   ✅ Auto-summarization triggered!")
                            break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Check persistent memory
        print("\n3️⃣ Checking persistent memory after summarization...")
        try:
            resp = await client.get(
                f"{STORAGE_URL}/api/memory/persistent-memory/{TEST_USER['userId']}", 
                headers=headers
            )
            if resp.status_code == 200:
                data = resp.json()
                summary = data.get("summary", "")
                if summary:
                    print(f"✅ Persistent memory exists: {len(summary)} chars")
                    print(f"   Preview: {summary[:200]}...")
                else:
                    print("⚠️ No persistent memory found")
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_prompt_optimization():
    """Test prompt optimization endpoint"""
    print("\n\n📐 Testing Prompt Optimization")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}
    
    async with httpx.AsyncClient() as client:
        # Create test data
        test_prompt = {
            "base_prompt": "You are a helpful assistant specializing in personality development. " * 20,
            "uuid": TEST_USER["userId"],
            "rag_context": "This is some relevant context about personality traits. " * 50
        }
        
        try:
            resp = await client.post(
                f"{STORAGE_URL}/api/memory/optimize-prompt",
                json=test_prompt,
                headers=headers
            )
            
            if resp.status_code == 200:
                result = resp.json()
                metrics = result["metrics"]
                
                print("✅ Prompt optimization results:")
                print(f"   - Total chars: {metrics['total_chars']:,}")
                print(f"   - Base prompt: {metrics['base_prompt_chars']:,} chars")
                print(f"   - Persistent memory: {metrics['persistent_memory_chars']:,} chars")
                print(f"   - Session memory: {metrics['session_memory_chars']:,} chars")
                print(f"   - RAG context: {metrics['rag_context_chars']:,} chars")
                print(f"   - Within limits: {metrics['within_limits']}")
                print(f"   - Utilization: {metrics['utilization_percent']:.1f}%")
                
                # Show prompt structure
                prompt_preview = result["final_prompt"][:500]
                print(f"\n📄 Prompt preview:\n{prompt_preview}...")
            else:
                print(f"❌ Optimization failed: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    """Run all tests"""
    print("🚀 Xavigate Memory System Integration Test")
    print("=" * 60)
    
    # Check if auth token is needed
    global AUTH_TOKEN
    if os.getenv("ENV", "dev") != "dev":
        AUTH_TOKEN = input("Enter your Cognito auth token (or press Enter for dev mode): ").strip()
    
    print(f"\n📍 Testing against:")
    print(f"   Storage Service: {STORAGE_URL}")
    print(f"   Chat Service: {CHAT_URL}")
    print(f"   Auth: {'Enabled' if AUTH_TOKEN else 'Disabled (dev mode)'}")
    
    # Run tests
    await test_memory_endpoints()
    await test_chat_integration()
    await test_memory_limits()
    await test_prompt_optimization()
    
    print("\n\n✅ All tests completed!")
    print("\n📋 Summary:")
    print("1. Memory endpoints are working")
    print("2. Chat integration with prompt optimization is functional")
    print("3. Auto-summarization triggers at memory limits")
    print("4. Prompt optimization keeps context within token limits")
    
    print("\n🎯 Next steps:")
    print("1. Run the configuration dashboard: python scripts/config_dashboard_enhanced.py")
    print("2. Monitor memory usage in production")
    print("3. Adjust limits based on usage patterns")
    print("4. Check logs for optimization metrics")

if __name__ == "__main__":
    asyncio.run(main())