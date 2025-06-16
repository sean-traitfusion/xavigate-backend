#!/usr/bin/env python3
"""
Test script for the enhanced memory system
Tests auto-summarization, compression, and prompt optimization
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'microservices', 'storage_service'))

from memory.client import MemoryClient
from memory.prompt_manager import optimize_prompt_size
from config import runtime_config
import time
import json

def test_memory_system():
    """Test the memory system with various scenarios"""
    
    # Initialize client
    client = MemoryClient()
    test_uuid = "test_user_123"
    
    print("🧪 Testing Enhanced Memory System")
    print("=" * 50)
    
    # Test 1: Basic interaction logging
    print("\n1️⃣ Testing basic interaction logging...")
    client.log_interaction(test_uuid, "user", "Hello, my name is John and I live in New York.")
    client.log_interaction(test_uuid, "assistant", "Nice to meet you John! How long have you lived in New York?")
    client.log_interaction(test_uuid, "user", "About 10 years now. I work as a software engineer.")
    client.log_interaction(test_uuid, "assistant", "That's great! Software engineering in NYC must be exciting.")
    
    session_size = client.get_session_size(test_uuid)
    print(f"✅ Session size after 4 interactions: {session_size} chars")
    
    # Test 2: Voice command detection
    print("\n2️⃣ Testing voice command detection...")
    trigger = client.check_voice_commands("Please remember this for next time")
    print(f"✅ Voice command detected: {trigger}")
    
    trigger = client.check_voice_commands("Do you remember what I told you?")
    print(f"✅ Question (should not trigger): {trigger}")
    
    # Test 3: Get session data
    print("\n3️⃣ Testing session retrieval...")
    session = client.get_session(test_uuid)
    print(f"✅ Session has {len(session)} entries")
    
    # Test 4: Force summarization
    print("\n4️⃣ Testing forced summarization...")
    success = client.force_session_summary(test_uuid, "test_trigger")
    print(f"✅ Summarization result: {success}")
    
    # Check session was cleared
    new_size = client.get_session_size(test_uuid)
    print(f"✅ Session size after summarization: {new_size} chars")
    
    # Test 5: Check persistent memory
    print("\n5️⃣ Testing persistent memory...")
    summary = client.get_summary(test_uuid)
    if summary:
        print(f"✅ Persistent memory exists: {len(summary)} chars")
        print(f"   Preview: {summary[:200]}...")
    else:
        print("❌ No persistent memory found")
    
    # Test 6: Add more data to test auto-summarization
    print("\n6️⃣ Testing auto-summarization at limit...")
    
    # Get current limit
    limit = runtime_config.get("SESSION_MEMORY_CHAR_LIMIT", 15000)
    print(f"   Session memory limit: {limit} chars")
    
    # Add interactions until we approach the limit
    for i in range(50):
        client.log_interaction(test_uuid, "user", f"This is test message {i}. " * 20)
        client.log_interaction(test_uuid, "assistant", f"Response to message {i}. " * 20)
        
        current_size = client.get_session_size(test_uuid)
        if current_size > limit * 0.8:
            print(f"   Approaching limit at {current_size} chars...")
            break
    
    # Check if auto-summarization triggered
    final_size = client.get_session_size(test_uuid)
    print(f"✅ Final session size: {final_size} chars")
    
    # Test 7: Prompt optimization
    print("\n7️⃣ Testing prompt optimization...")
    
    # Create test data
    base_prompt = "You are a helpful assistant. " * 50  # ~850 chars
    persistent_memory = client.get_summary(test_uuid) or ""
    session_data = client.get_session(test_uuid)
    
    # Convert session to lines
    session_lines = []
    for entry in reversed(session_data):
        line = f"{entry['role'].title()}: {entry['message']}"
        session_lines.append(line)
    
    rag_context = "This is some RAG context. " * 100  # ~2600 chars
    
    # Optimize
    final_prompt, metrics = optimize_prompt_size(
        base_prompt=base_prompt,
        persistent_memory=persistent_memory,
        session_memory_lines=session_lines,
        rag_context=rag_context
    )
    
    print(f"✅ Prompt optimization results:")
    print(f"   Total chars: {metrics['total_chars']}")
    print(f"   Base prompt: {metrics['base_prompt_chars']} chars")
    print(f"   Persistent memory: {metrics['persistent_memory_chars']} chars")
    print(f"   Session memory: {metrics['session_memory_chars']} chars")
    print(f"   RAG context: {metrics['rag_context_chars']} chars")
    print(f"   Session lines included: {metrics['session_lines_included']}/{metrics['session_lines_total']}")
    print(f"   Within limits: {metrics['within_limits']}")
    print(f"   Utilization: {metrics['utilization_percent']:.1f}%")
    
    # Test 8: Clear session for next test
    print("\n8️⃣ Testing session clearing...")
    client.clear_session(test_uuid)
    cleared_size = client.get_session_size(test_uuid)
    print(f"✅ Session size after clearing: {cleared_size} chars")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")

if __name__ == "__main__":
    # Set test environment
    os.environ["ENV"] = "test"
    
    try:
        test_memory_system()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()