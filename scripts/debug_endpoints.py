#!/usr/bin/env python3
"""Debug script to test individual endpoints"""
import os
import httpx
import asyncio
import json

# Show environment
print(f"Current ENV: {os.getenv('ENV')}")
print(f"AUTH_TOKEN present: {'Yes' if os.getenv('AUTH_TOKEN') else 'No'}")
print("=" * 60)

async def test_endpoints():
    headers = {}
    auth_token = os.getenv("AUTH_TOKEN", "")
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
        print(f"Using auth token: {auth_token[:20]}...")
    else:
        print("No auth token provided")
    
    # Test each endpoint
    tests = [
        ("Storage Health", "GET", "http://localhost:8011/health", None),
        ("Storage Memory Save", "POST", "http://localhost:8011/api/memory/save", {
            "userId": "test-user",
            "sessionId": "test-session",
            "messages": [{"role": "user", "content": "test"}]
        }),
        ("Vector Health", "GET", "http://localhost:8017/health", None),
        ("Vector Search", "POST", "http://localhost:8017/search", {
            "query": "test query",
            "top_k": 3
        }),
        ("Chat Health", "GET", "http://localhost:8015/health", None),
        ("Chat Query", "POST", "http://localhost:8015/query", {
            "userId": "test-user",
            "username": "testuser",
            "fullName": "Test User",
            "sessionId": "test-session",
            "message": "Hello"
        }),
    ]
    
    async with httpx.AsyncClient() as client:
        for name, method, url, data in tests:
            print(f"\nTesting: {name}")
            print(f"  URL: {url}")
            print(f"  Method: {method}")
            if data:
                print(f"  Data: {json.dumps(data, indent=2)}")
            
            try:
                if method == "GET":
                    resp = await client.get(url, headers=headers)
                else:
                    resp = await client.post(url, json=data, headers=headers)
                
                print(f"  Status: {resp.status_code}")
                if resp.status_code != 200:
                    print(f"  Response: {resp.text[:200]}")
                else:
                    print(f"  Success!")
                    
            except Exception as e:
                print(f"  Error: {e}")

asyncio.run(test_endpoints())