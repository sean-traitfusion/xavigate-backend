#!/usr/bin/env python3
"""
Fixed test for config dashboard functionality with proper auth
"""
import httpx
import asyncio
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get service URLs based on environment
ENV = os.getenv("ENV", "dev")
if ENV == "prod":
    STATS_URL = "http://stats_service:8013"
    STORAGE_URL = "http://storage_service:8011"
else:
    STATS_URL = "http://localhost:8012"
    STORAGE_URL = "http://localhost:8011"

# You can set a test token here or get from environment
TEST_AUTH_TOKEN = os.getenv("TEST_AUTH_TOKEN", "")

async def check_services():
    """Check if services are running"""
    services = [
        ("Storage Service", STORAGE_URL, "/health"),
        ("Stats Service", STATS_URL, "/health")
    ]
    
    all_up = True
    async with httpx.AsyncClient() as client:
        for name, url, path in services:
            try:
                resp = await client.get(f"{url}{path}", timeout=2.0)
                if resp.status_code == 200:
                    print(f"✅ {name} is running at {url}")
                else:
                    print(f"❌ {name} returned status {resp.status_code}")
                    all_up = False
            except Exception as e:
                print(f"❌ {name} is not accessible at {url}: {type(e).__name__}")
                all_up = False
    
    return all_up

async def test_config_dashboard():
    """Test config dashboard functionality"""
    print("\n🧪 Testing Config Dashboard")
    print("=" * 50)
    
    # First check if services are up
    if not await check_services():
        print("\n⚠️  Not all services are running. Please start them with:")
        print("   docker-compose up storage_service stats_service")
        return
    
    async with httpx.AsyncClient() as client:
        # 1. Test dashboard loads
        print("\n1️⃣ Testing dashboard page loads...")
        try:
            resp = await client.get(f"{STATS_URL}/dashboard/")
            print(f"   Status: {resp.status_code}")
            print(f"   ✅ Dashboard loaded" if resp.status_code == 200 else f"   ❌ Failed to load")
            
            if resp.status_code == 200:
                # Check for removed test tab
                has_test_tab = "Test Configuration" in resp.text
                print(f"   Test tab removed: {'❌ Still present' if has_test_tab else '✅ Yes'}")
                
                # Check for key elements
                has_system_prompt = "System Prompt" in resp.text
                has_memory_settings = "Memory Settings" in resp.text
                print(f"   Has System Prompt field: {'✅' if has_system_prompt else '❌'}")
                print(f"   Has Memory Settings: {'✅' if has_memory_settings else '❌'}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # 2. Test current config loading (with auth handling)
        print("\n2️⃣ Testing config loading from storage...")
        headers = {}
        if TEST_AUTH_TOKEN:
            headers["Authorization"] = f"Bearer {TEST_AUTH_TOKEN}"
        
        try:
            # First try without auth (local dev mode)
            resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config")
            
            if resp.status_code == 401 and TEST_AUTH_TOKEN:
                # Try with auth token
                resp = await client.get(
                    f"{STORAGE_URL}/api/memory/runtime-config",
                    headers=headers
                )
            
            if resp.status_code == 200:
                config = resp.json()
                print(f"   ✅ Config loaded successfully")
                print(f"   Keys found: {len(config)}")
                # Show a few key values
                for key in ["SYSTEM_PROMPT", "SESSION_MEMORY_CHAR_LIMIT", "PERSISTENT_MEMORY_COMPRESSION_RATIO"]:
                    if key in config:
                        value = str(config[key])[:50] + "..." if len(str(config[key])) > 50 else str(config[key])
                        print(f"   - {key}: {value}")
            elif resp.status_code == 401:
                print(f"   ⚠️  Auth required. Set TEST_AUTH_TOKEN environment variable")
                print(f"   You can get a token by logging into the app")
            else:
                print(f"   ❌ Failed to load config: {resp.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # 3. Test config save via dashboard API
        print("\n3️⃣ Testing config save through dashboard...")
        test_config = {
            "SYSTEM_PROMPT": "Test prompt from dashboard test",
            "SESSION_MEMORY_CHAR_LIMIT": 12000,
            "PERSISTENT_MEMORY_COMPRESSION_RATIO": 0.5,
            "SUMMARY_TEMPERATURE": 0.3,
            "AUTO_SUMMARY_ENABLED": True
        }
        
        # If we have auth token, include it in the config for the dashboard
        if TEST_AUTH_TOKEN:
            test_config["auth_token"] = TEST_AUTH_TOKEN
        
        try:
            resp = await client.post(
                f"{STATS_URL}/dashboard/api/save-config",
                json=test_config
            )
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                print(f"   ✅ Config saved successfully")
                result = resp.json()
                print(f"   Response: {result}")
            else:
                print(f"   ❌ Save failed: {resp.text}")
                if resp.status_code == 401:
                    print(f"   ⚠️  Auth required. The dashboard needs proper authentication setup")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # 4. Manual browser test instructions
        print("\n4️⃣ Manual Browser Test Instructions:")
        print(f"   1. Open http://localhost:8012/dashboard/ in your browser")
        print(f"   2. Verify:")
        print(f"      - No 'Test Configuration' tab exists")
        print(f"      - You can see three tabs: Chat Settings, Memory Settings, Prompt Templates")
        print(f"      - Current configuration values are displayed")
        print(f"   3. Try changing a value (e.g., Temperature slider)")
        print(f"   4. Click 'Save All Settings'")
        print(f"   5. Refresh the page and verify your changes persisted")
    
    print("\n✅ Config dashboard test complete!")

async def test_direct_storage_api():
    """Test direct storage API access"""
    print("\n🔧 Testing Direct Storage API")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        # Test without auth
        print("Testing without auth...")
        resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config")
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            print("✅ Storage service allows unauthenticated access (dev mode)")
        elif resp.status_code == 401:
            print("🔒 Storage service requires authentication")
            print("To run authenticated tests, set TEST_AUTH_TOKEN environment variable")

if __name__ == "__main__":
    print("Config Dashboard Test")
    print("=" * 50)
    
    if TEST_AUTH_TOKEN:
        print(f"Using auth token: {TEST_AUTH_TOKEN[:20]}...")
    else:
        print("No auth token set (testing in local/dev mode)")
    
    asyncio.run(test_config_dashboard())
    asyncio.run(test_direct_storage_api())