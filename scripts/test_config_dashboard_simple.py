#!/usr/bin/env python3
"""
Simple test for config dashboard functionality
"""
import httpx
import asyncio
import json

STATS_URL = "http://localhost:8012"  # Stats service with dashboard
STORAGE_URL = "http://localhost:8011"  # Storage service

async def test_config_dashboard():
    """Test config dashboard functionality"""
    print("🧪 Testing Config Dashboard")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        # 1. Test dashboard loads
        print("\n1️⃣ Testing dashboard page loads...")
        try:
            resp = await client.get(f"{STATS_URL}/dashboard/")
            print(f"   Status: {resp.status_code}")
            print(f"   ✅ Dashboard loaded" if resp.status_code == 200 else f"   ❌ Failed to load")
            
            # Check for removed test tab
            has_test_tab = "Test Configuration" in resp.text
            print(f"   Test tab removed: {'❌ Still present' if has_test_tab else '✅ Yes'}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # 2. Test current config loading
        print("\n2️⃣ Testing config loading from storage...")
        try:
            resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config")
            if resp.status_code == 200:
                config = resp.json()
                print(f"   ✅ Config loaded successfully")
                print(f"   Keys found: {len(config)}")
                # Show a few key values
                for key in ["SYSTEM_PROMPT", "SESSION_MEMORY_CHAR_LIMIT", "PERSISTENT_MEMORY_COMPRESSION_RATIO"]:
                    if key in config:
                        value = str(config[key])[:50] + "..." if len(str(config[key])) > 50 else str(config[key])
                        print(f"   - {key}: {value}")
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
            "temperature": 0.8,
            "max_tokens": 1500
        }
        
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
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # 4. Verify saved config
        print("\n4️⃣ Verifying saved configuration...")
        try:
            resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config")
            if resp.status_code == 200:
                saved_config = resp.json()
                # Check if our test values were saved
                checks = [
                    ("SYSTEM_PROMPT", "Test prompt from dashboard test"),
                    ("SESSION_MEMORY_CHAR_LIMIT", 12000),
                    ("PERSISTENT_MEMORY_COMPRESSION_RATIO", 0.5)
                ]
                
                all_good = True
                for key, expected in checks:
                    actual = saved_config.get(key)
                    matches = str(actual) == str(expected)
                    print(f"   - {key}: {'✅' if matches else '❌'} (expected: {expected}, got: {actual})")
                    if not matches:
                        all_good = False
                
                print(f"\n   Overall: {'✅ All values saved correctly' if all_good else '❌ Some values not saved'}")
            else:
                print(f"   ❌ Failed to verify: {resp.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ Config dashboard test complete!")

if __name__ == "__main__":
    print("Make sure the following services are running:")
    print("- Storage Service (port 8011)")
    print("- Stats Service (port 8012)")
    print("\nPress Enter to continue...")
    input()
    
    asyncio.run(test_config_dashboard())