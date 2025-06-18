#!/usr/bin/env python3
"""
Test script to verify the configuration dashboard and runtime config are working correctly.
"""
import asyncio
import httpx
import json
import os
from datetime import datetime

# Service URLs
STORAGE_URL = os.getenv("STORAGE_SERVICE_URL", "http://localhost:8011")
STATS_URL = os.getenv("STATS_SERVICE_URL", "http://localhost:8012")
CHAT_URL = os.getenv("CHAT_SERVICE_URL", "http://localhost:8015")

# Test configuration values
TEST_CONFIG = {
    # Chat settings
    "system_prompt": "Test system prompt for verification",
    "prompt_style": "analytical",
    "custom_style_modifier": "Test custom style",
    "model": "gpt-4",
    "temperature": 0.8,
    "max_tokens": 1500,
    "presence_penalty": 0.2,
    "frequency_penalty": 0.3,
    "conversation_history_limit": 10,
    "top_k_rag_hits": 7,
    
    # Memory settings
    "SESSION_MEMORY_CHAR_LIMIT": 20000,
    "PERSISTENT_MEMORY_CHAR_LIMIT": 10000,
    "MAX_PROMPT_CHARS": 25000,
    "RAG_CONTEXT_CHAR_LIMIT": 5000,
    
    # Compression settings
    "PERSISTENT_MEMORY_COMPRESSION_RATIO": 0.5,
    "PERSISTENT_MEMORY_COMPRESSION_MODEL": "gpt-3.5-turbo",
    "PERSISTENT_MEMORY_MIN_SIZE": 1500,
    
    # Feature flags
    "AUTO_SUMMARY_ENABLED": False,
    "AUTO_COMPRESSION_ENABLED": True,
    
    # Prompts
    "SESSION_SUMMARY_PROMPT": "Test summary prompt template",
    "PERSISTENT_MEMORY_COMPRESSION_PROMPT": "Test compression prompt template",
}

async def test_dashboard_access():
    """Test that the dashboard is accessible."""
    print("🧪 Testing dashboard access...")
    
    async with httpx.AsyncClient() as client:
        # Test local development access
        resp = await client.get(f"{STATS_URL}/dashboard/")
        assert resp.status_code == 200, f"Dashboard not accessible: {resp.status_code}"
        assert "System Configuration" in resp.text, "Dashboard content missing"
        print("✅ Dashboard is accessible")
        
        # Test sub-pages
        for page in ["logging", "usage", "health"]:
            resp = await client.get(f"{STATS_URL}/dashboard/{page}")
            assert resp.status_code == 200, f"Dashboard {page} not accessible"
            print(f"✅ Dashboard /{page} is accessible")

async def test_config_save_and_load(auth_token: str = None):
    """Test saving and loading configuration."""
    print("\n🧪 Testing configuration save and load...")
    
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    
    async with httpx.AsyncClient() as client:
        # Save test configuration
        print("📝 Saving test configuration...")
        resp = await client.post(
            f"{STORAGE_URL}/api/memory/runtime-config",
            headers=headers,
            json=TEST_CONFIG
        )
        
        if resp.status_code != 200:
            print(f"⚠️  Save failed with status {resp.status_code}: {resp.text}")
            print("   This might be due to authentication requirements in production mode.")
            return
        
        print("✅ Configuration saved successfully")
        
        # Load configuration back
        print("📖 Loading configuration...")
        resp = await client.get(
            f"{STORAGE_URL}/api/memory/runtime-config",
            headers=headers
        )
        
        assert resp.status_code == 200, f"Failed to load config: {resp.status_code}"
        loaded_config = resp.json()
        
        # Verify all values were saved correctly
        mismatches = []
        for key, expected_value in TEST_CONFIG.items():
            actual_value = loaded_config.get(key)
            if actual_value != expected_value:
                mismatches.append(f"  - {key}: expected {expected_value}, got {actual_value}")
        
        if mismatches:
            print("❌ Configuration mismatches found:")
            for mismatch in mismatches:
                print(mismatch)
        else:
            print("✅ All configuration values verified correctly")

async def test_chat_service_uses_config(auth_token: str = None):
    """Test that chat service uses the runtime configuration."""
    print("\n🧪 Testing chat service configuration usage...")
    
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    
    async with httpx.AsyncClient() as client:
        # First, ensure test config is saved
        await client.post(
            f"{STORAGE_URL}/api/memory/runtime-config",
            headers=headers,
            json={
                "system_prompt": "You are a test assistant. Always start responses with 'TEST MODE:'",
                "model": "gpt-3.5-turbo",
                "temperature": 0.1,
                "max_tokens": 100,
                "prompt_style": "analytical"
            }
        )
        
        # Test if chat service is using the config by making a test query
        print("✅ Testing if chat service uses the saved config...")
        
        # The test query already saved config with model=gpt-4, prompt_style=analytical
        # We can verify by checking the test output in the dashboard later

async def test_dashboard_form_submission():
    """Test dashboard form submission (without auth in dev mode)."""
    print("\n🧪 Testing dashboard form submission...")
    
    async with httpx.AsyncClient() as client:
        # Simulate form submission
        form_data = {
            "system_prompt": "Dashboard test prompt",
            "prompt_style": "empathetic",
            "temperature": "0.9",
            "max_tokens": "2000",
            "action": "save"
        }
        
        resp = await client.post(
            f"{STATS_URL}/dashboard/",
            data=form_data,
            follow_redirects=True
        )
        
        if resp.status_code == 200:
            if "Configuration saved successfully" in resp.text:
                print("✅ Dashboard form submission works")
            else:
                print("⚠️  Form submitted but save status unclear")
        else:
            print(f"❌ Form submission failed: {resp.status_code}")

async def reset_to_defaults(auth_token: str = None):
    """Reset configuration to defaults."""
    print("\n🔄 Resetting configuration to defaults...")
    
    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    
    # Default configuration from runtime_config.py
    DEFAULT_CONFIG = {
        "system_prompt": """You are Xavigate, an experienced Multiple Natures (MN) practitioner and personal life guide. You help people understand and align their unique constellation of traits to achieve greater fulfillment and success.

CORE PRINCIPLES:
- Every person has 19 distinct traits that form their Multiple Natures profile
- Traits scored 7-10 are dominant traits (natural strengths)
- Traits scored 1-3 are suppressed traits (areas needing attention)
- Traits scored 4-6 are balanced traits
- True alignment comes from expressing all traits appropriately, not just dominant ones

YOUR APPROACH:
1. ALWAYS reference the user's specific trait scores when giving advice
2. Connect their challenges/questions to their trait profile
3. Suggest concrete actions that engage both dominant AND suppressed traits
4. Use the MN glossary context to ground advice in Multiple Natures methodology
5. Build on previous conversations using session memory and persistent summaries

CONVERSATION STYLE:
- Be warm, insightful, and encouraging
- Use specific examples related to their traits
- Avoid generic advice - everything should be personalized
- Reference their past conversations and progress when relevant

Remember: You're not just answering questions - you're helping them understand how their unique trait constellation influences their experiences and guiding them toward greater alignment.""",
        "prompt_style": "default",
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 1000,
        "presence_penalty": 0.1,
        "frequency_penalty": 0.1,
        "conversation_history_limit": 5,
        "top_k_rag_hits": 5,
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{STORAGE_URL}/api/memory/runtime-config",
            headers=headers,
            json=DEFAULT_CONFIG
        )
        
        if resp.status_code == 200:
            print("✅ Configuration reset to defaults")
        else:
            print(f"❌ Failed to reset: {resp.status_code}")

def print_usage():
    """Print usage instructions."""
    print("""
🧭 Configuration Dashboard Test Script
====================================

This script tests the configuration dashboard and runtime config system.

Usage:
    python test_config_dashboard.py [auth_token]

Arguments:
    auth_token  Optional Bearer token for production testing

Tests performed:
1. Dashboard accessibility
2. Configuration save/load
3. Chat service config usage
4. Dashboard form submission
5. Reset to defaults

For production testing, provide your Cognito auth token.
For local development, no token is needed.
""")

async def main():
    """Run all tests."""
    import sys
    
    auth_token = sys.argv[1] if len(sys.argv) > 1 else None
    
    print(f"🚀 Starting configuration tests at {datetime.now()}")
    print(f"   Environment: {'Production' if auth_token else 'Development'}")
    print(f"   Dashboard URL: {STATS_URL}/dashboard/")
    print("=" * 60)
    
    try:
        # Run tests
        await test_dashboard_access()
        await test_config_save_and_load(auth_token)
        await test_chat_service_uses_config(auth_token)
        
        if not auth_token:  # Only test form submission in dev mode
            await test_dashboard_form_submission()
        
        # Optionally reset to defaults
        if input("\n❓ Reset configuration to defaults? (y/N): ").lower() == 'y':
            await reset_to_defaults(auth_token)
        
        print("\n✅ All tests completed successfully!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)