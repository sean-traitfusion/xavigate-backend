#!/usr/bin/env python3
"""
Test script to debug why memory and RAG contexts are empty
"""

import httpx
import asyncio
import json
import sys

# Service URLs - adjust these based on your environment
STORAGE_URL = "http://localhost:8011"
VECTOR_URL = "http://localhost:8017"
CHAT_URL = "http://localhost:8015"

# Test data
TEST_SESSION_ID = "test-session-123"
TEST_USER_ID = "test-user-123"

async def test_storage_service():
    """Test storage service endpoints"""
    print("\n=== Testing Storage Service ===")
    
    async with httpx.AsyncClient() as client:
        # Test session memory endpoint
        print(f"\n1. Testing session memory endpoint:")
        url = f"{STORAGE_URL}/api/memory/session-memory/{TEST_SESSION_ID}"
        print(f"   URL: {url}")
        
        try:
            resp = await client.get(url)
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}...")
            if resp.status_code == 200:
                data = resp.json()
                print(f"   Data type: {type(data)}")
                print(f"   Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                if 'exchanges' in data:
                    print(f"   Exchanges count: {len(data['exchanges'])}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Test summaries endpoint
        print(f"\n2. Testing summaries endpoint:")
        url = f"{STORAGE_URL}/api/memory/all-summaries/{TEST_USER_ID}"
        print(f"   URL: {url}")
        
        try:
            resp = await client.get(url)
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}...")
            if resp.status_code == 200:
                data = resp.json()
                print(f"   Data type: {type(data)}")
                print(f"   Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                if 'summaries' in data:
                    print(f"   Summaries count: {len(data['summaries'])}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Test runtime config endpoint
        print(f"\n3. Testing runtime config endpoint:")
        url = f"{STORAGE_URL}/api/memory/runtime-config"
        print(f"   URL: {url}")
        
        try:
            resp = await client.get(url)
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"   Config keys: {list(data.keys())}")
        except Exception as e:
            print(f"   Error: {e}")

async def test_vector_service():
    """Test vector/RAG service"""
    print("\n=== Testing Vector Service ===")
    
    async with httpx.AsyncClient() as client:
        # Test search endpoint
        print(f"\n1. Testing search endpoint:")
        url = f"{VECTOR_URL}/search"
        print(f"   URL: {url}")
        
        search_request = {
            "query": "What is creative energy?",
            "top_k": 5
        }
        print(f"   Request: {search_request}")
        
        try:
            resp = await client.post(url, json=search_request)
            print(f"   Status: {resp.status_code}")
            print(f"   Response preview: {resp.text[:200]}...")
            if resp.status_code == 200:
                data = resp.json()
                print(f"   Data type: {type(data)}")
                print(f"   Results count: {len(data) if isinstance(data, list) else 'Not a list'}")
                if data and isinstance(data, list):
                    print(f"   First result keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'Not a dict'}")
        except Exception as e:
            print(f"   Error: {e}")

async def insert_test_data():
    """Insert test data into storage service"""
    print("\n=== Inserting Test Data ===")
    
    async with httpx.AsyncClient() as client:
        # Insert session memory
        print(f"\n1. Inserting session memory:")
        url = f"{STORAGE_URL}/api/memory/session-memory"
        
        test_exchanges = [
            {"user_prompt": "Hello, I need help understanding my traits", 
             "assistant_response": "I'd be happy to help you understand your traits. Based on your assessment..."},
            {"user_prompt": "What does creative mean?",
             "assistant_response": "Creative energy represents imagination, originality, and artistic expression..."}
        ]
        
        payload = {
            "uuid": TEST_SESSION_ID,
            "conversation_log": {"exchanges": test_exchanges}
        }
        
        try:
            resp = await client.post(url, json=payload)
            print(f"   Status: {resp.status_code}")
            print(f"   Response: {resp.text}")
        except Exception as e:
            print(f"   Error: {e}")

async def main():
    """Run all tests"""
    import argparse
    parser = argparse.ArgumentParser(description="Test services for memory debug")
    parser.add_argument("--insert", action="store_true", help="Insert test data first")
    parser.add_argument("--storage-only", action="store_true", help="Test only storage service")
    parser.add_argument("--vector-only", action="store_true", help="Test only vector service")
    
    args = parser.parse_args()
    
    if args.insert:
        await insert_test_data()
    
    if not args.vector_only:
        await test_storage_service()
    
    if not args.storage_only:
        await test_vector_service()

if __name__ == "__main__":
    asyncio.run(main())