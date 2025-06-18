#!/usr/bin/env python3
"""
Test script to verify persistent compression safety features
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'microservices', 'storage_service'))

from memory.persistent_compression import (
    compress_persistent_memory,
    get_compression_count,
    check_and_compress_persistent_memory
)
from memory.persistent_memory import get_summary, append_to_summary
from config import runtime_config

def test_compression_safety():
    """Test compression with safety features"""
    test_user_id = "test-compression-user"
    
    print("🧪 Testing Persistent Compression Safety Features")
    print("=" * 50)
    
    # 1. Test empty compression handling
    print("\n1️⃣ Testing empty summary compression...")
    result = compress_persistent_memory(test_user_id, 0)
    print(f"   Result: {'✅ Correctly rejected' if not result else '❌ Should have failed'}")
    
    # 2. Test compression with content
    print("\n2️⃣ Setting up test content...")
    test_content = """
    User Profile: John Doe
    - Software Engineer at TechCorp
    - Interests: Python, Machine Learning, Rock Climbing
    - Traits: Creative (8), Logical (7), Emotional (5)
    - Goals: Learn advanced ML techniques, improve work-life balance
    - Recent discussions: Career advancement, project management strategies
    """ * 10  # Repeat to make it long enough
    
    # Add test content
    append_to_summary(test_user_id, test_content)
    original = get_summary(test_user_id)
    print(f"   Original size: {len(original)} chars")
    
    # 3. Test compression
    print("\n3️⃣ Testing compression...")
    result = compress_persistent_memory(test_user_id, 0)
    if result:
        compressed = get_summary(test_user_id)
        print(f"   ✅ Compression successful!")
        print(f"   Compressed size: {len(compressed)} chars")
        print(f"   Compression ratio: {len(compressed)/len(original):.2%}")
        print(f"   Has compression marker: {'[COMPRESSED' in compressed}")
        
        # Verify content preservation
        important_terms = ["John Doe", "Software Engineer", "TechCorp", "Creative", "Logical"]
        preserved = sum(1 for term in important_terms if term.lower() in compressed.lower())
        print(f"   Key terms preserved: {preserved}/{len(important_terms)}")
    else:
        print("   ❌ Compression failed")
    
    # 4. Test compression count detection
    print("\n4️⃣ Testing compression count detection...")
    count = get_compression_count(get_summary(test_user_id))
    print(f"   Compression count: {count}")
    
    # 5. Test automatic compression trigger
    print("\n5️⃣ Testing automatic compression trigger...")
    # Set a low limit to trigger compression
    runtime_config.set_config("PERSISTENT_MEMORY_CHAR_LIMIT", 500)
    
    # Add more content to trigger compression
    append_to_summary(test_user_id, "Additional content to trigger automatic compression" * 20)
    
    result = check_and_compress_persistent_memory(test_user_id)
    print(f"   Auto-compression triggered: {'✅ Yes' if result else '❌ No'}")
    
    # Reset config
    runtime_config.set_config("PERSISTENT_MEMORY_CHAR_LIMIT", 8000)
    
    print("\n✅ Compression safety test complete!")

if __name__ == "__main__":
    test_compression_safety()