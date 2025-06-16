#!/usr/bin/env python3
"""
Test the chat service with Cognito authentication
"""
import asyncio
import httpx
import json
import sys

# Configuration
CHAT_URL = "http://localhost:8000"

# Test data
TEST_REQUEST = {
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
    },
    "message": "Hello, I'm interested in learning about personality traits and how they affect my work."
}

async def test_chat_with_token(token: str):
    """Test chat endpoint with authentication token"""
    print("🤖 Testing Chat Service with Authentication")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        print(f"\n📝 Sending message: {TEST_REQUEST['message'][:60]}...")
        
        try:
            resp = await client.post(
                f"{CHAT_URL}/api/chat/query",
                json=TEST_REQUEST,
                headers=headers,
                timeout=30.0
            )
            
            print(f"\n📊 Response Status: {resp.status_code}")
            
            if resp.status_code == 200:
                result = resp.json()
                print(f"\n✅ Success!")
                print(f"\n🤖 Assistant Response:")
                print(f"{result['answer'][:500]}...")
                
                if result.get('sources'):
                    print(f"\n📚 Sources: {len(result['sources'])} documents")
                    for i, source in enumerate(result['sources'][:2], 1):
                        print(f"\n   Source {i}:")
                        print(f"   - Text: {source['text'][:100]}...")
                        print(f"   - Metadata: {source.get('metadata', {})}")
            else:
                print(f"\n❌ Error: {resp.status_code}")
                print(f"Response: {resp.text}")
                
        except httpx.ConnectError:
            print("\n❌ Connection Error: Make sure the chat service is running on port 8000")
        except Exception as e:
            print(f"\n❌ Error: {e}")

async def test_chat_dev_mode():
    """Test chat endpoint in dev mode (no auth)"""
    print("🤖 Testing Chat Service in Dev Mode (No Auth)")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        print(f"\n📝 Sending message: {TEST_REQUEST['message'][:60]}...")
        
        try:
            resp = await client.post(
                f"{CHAT_URL}/api/chat/query",
                json=TEST_REQUEST,
                timeout=30.0
            )
            
            print(f"\n📊 Response Status: {resp.status_code}")
            
            if resp.status_code == 200:
                result = resp.json()
                print(f"\n✅ Success!")
                print(f"\n🤖 Assistant Response:")
                print(f"{result['answer']}")
                
                # In dev mode, we get a stub response
                if result['answer'] == "Dev stub response":
                    print("\n⚠️  Dev mode stub response received.")
                    print("   To test real functionality, set ENV=prod and provide a token")
            else:
                print(f"\n❌ Error: {resp.status_code}")
                print(f"Response: {resp.text}")
                
        except httpx.ConnectError:
            print("\n❌ Connection Error: Make sure the chat service is running on port 8000")
        except Exception as e:
            print(f"\n❌ Error: {e}")

async def get_cognito_token():
    """Guide for getting a Cognito token"""
    print("\n📋 How to get a Cognito token:")
    print("=" * 60)
    print("\n1. Using AWS CLI:")
    print("   aws cognito-idp initiate-auth \\")
    print("     --auth-flow USER_PASSWORD_AUTH \\")
    print("     --client-id YOUR_CLIENT_ID \\")
    print("     --auth-parameters USERNAME=your-username,PASSWORD=your-password")
    print("\n2. Using the frontend:")
    print("   - Log into your application")
    print("   - Open browser DevTools (F12)")
    print("   - Go to Network tab")
    print("   - Look for API calls with Authorization header")
    print("   - Copy the token after 'Bearer '")
    print("\n3. From your auth service:")
    print("   - Make a login request to your auth endpoint")
    print("   - Extract the token from the response")

def main():
    """Main test function"""
    print("🚀 Xavigate Chat Service Test")
    print("=" * 60)
    
    # Check if we're in dev or prod mode
    import os
    env = os.getenv("ENV", "dev")
    
    if env == "dev":
        print(f"\n🔧 Running in DEV mode (no authentication required)")
        asyncio.run(test_chat_dev_mode())
    else:
        print(f"\n🔐 Running in PROD mode (authentication required)")
        
        # Get token from user
        print("\nPlease enter your Cognito Bearer token:")
        print("(You can get this from your browser's DevTools after logging in)")
        token = input("Token: ").strip()
        
        if not token:
            print("\n❌ No token provided!")
            asyncio.run(get_cognito_token())
            return
        
        # Remove 'Bearer ' prefix if included
        if token.startswith("Bearer "):
            token = token[7:]
        
        asyncio.run(test_chat_with_token(token))
    
    print("\n\n📝 Additional Testing:")
    print("=" * 60)
    print("\n1. Test multiple messages in sequence:")
    print("   - Modify the TEST_REQUEST message")
    print("   - Run the script multiple times")
    print("   - Check if context is maintained")
    print("\n2. Test memory limits:")
    print("   - Send many messages to fill session memory")
    print("   - Watch for auto-summarization")
    print("\n3. Monitor logs:")
    print("   - Check storage service logs for memory operations")
    print("   - Check chat service logs for prompt optimization")

if __name__ == "__main__":
    main()