#!/usr/bin/env python3
"""
Debug script to diagnose why memory and RAG contexts are empty
"""

import os
import sys
import psycopg2
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.db import get_connection
from memory.client import MemoryClient
from memory.session_memory import get_all_session_memory
from memory.persistent_memory import get_summary

def check_database_schema():
    """Check if the database tables have the correct schema"""
    print("\n=== Checking Database Schema ===")
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Check session_memory columns
                cur.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'session_memory'
                    ORDER BY ordinal_position;
                """)
                print("\nSession Memory Table Columns:")
                for col in cur.fetchall():
                    print(f"  - {col[0]}: {col[1]}")
                
                # Check persistent_memory columns
                cur.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'persistent_memory'
                    ORDER BY ordinal_position;
                """)
                print("\nPersistent Memory Table Columns:")
                for col in cur.fetchall():
                    print(f"  - {col[0]}: {col[1]}")
                    
                # Check if there's any data
                cur.execute("SELECT COUNT(*) FROM session_memory")
                session_count = cur.fetchone()[0]
                print(f"\nSession Memory Records: {session_count}")
                
                cur.execute("SELECT COUNT(*) FROM persistent_memory")
                persistent_count = cur.fetchone()[0]
                print(f"Persistent Memory Records: {persistent_count}")
                
    except Exception as e:
        print(f"Error checking schema: {e}")

def test_memory_retrieval(session_id="test-session", user_id="test-user"):
    """Test memory retrieval functions"""
    print(f"\n=== Testing Memory Retrieval ===")
    print(f"Session ID: {session_id}")
    print(f"User ID: {user_id}")
    
    client = MemoryClient()
    
    # Test session memory retrieval
    print("\n1. Testing Session Memory Retrieval:")
    try:
        session_data = client.get_session(session_id)
        print(f"   - Session data type: {type(session_data)}")
        print(f"   - Session data length: {len(session_data)}")
        if session_data:
            print(f"   - First entry: {session_data[0]}")
    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test persistent memory retrieval
    print("\n2. Testing Persistent Memory Retrieval:")
    try:
        summary = client.get_summary(user_id)
        print(f"   - Summary type: {type(summary)}")
        print(f"   - Summary length: {len(summary) if summary else 0}")
        if summary:
            print(f"   - Summary preview: {summary[:100]}...")
    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

def insert_test_data(session_id="test-session", user_id="test-user"):
    """Insert test data to verify the system works"""
    print(f"\n=== Inserting Test Data ===")
    
    client = MemoryClient()
    
    # Insert test session memory
    try:
        client.log_interaction(user_id, session_id, "user", "This is a test user message")
        client.log_interaction(user_id, session_id, "assistant", "This is a test assistant response")
        print("✅ Test session data inserted")
    except Exception as e:
        print(f"❌ Error inserting session data: {e}")
    
    # Insert test persistent memory
    try:
        client.append_summary(user_id, f"[{datetime.now().isoformat()}] Test summary entry")
        print("✅ Test persistent memory inserted")
    except Exception as e:
        print(f"❌ Error inserting persistent memory: {e}")

def check_raw_data(session_id="test-session", user_id="test-user"):
    """Check raw data in tables"""
    print(f"\n=== Checking Raw Data ===")
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Check session_memory for both uuid and session_id columns
                print("\n1. Session Memory Raw Query (by uuid):")
                cur.execute("""
                    SELECT * FROM session_memory 
                    WHERE uuid = %s 
                    ORDER BY created_at DESC 
                    LIMIT 5
                """, (session_id,))
                rows = cur.fetchall()
                print(f"   Found {len(rows)} rows by uuid")
                
                print("\n2. Session Memory Raw Query (by session_id if exists):")
                try:
                    cur.execute("""
                        SELECT * FROM session_memory 
                        WHERE session_id = %s 
                        ORDER BY created_at DESC 
                        LIMIT 5
                    """, (session_id,))
                    rows = cur.fetchall()
                    print(f"   Found {len(rows)} rows by session_id")
                    if rows:
                        print(f"   Sample row: {rows[0]}")
                except psycopg2.errors.UndefinedColumn:
                    print("   Column 'session_id' does not exist")
                
                # Check persistent_memory
                print("\n3. Persistent Memory Raw Query (by uuid):")
                cur.execute("""
                    SELECT * FROM persistent_memory 
                    WHERE uuid = %s
                """, (user_id,))
                row = cur.fetchone()
                if row:
                    print(f"   Found data: {row}")
                else:
                    print("   No data found")
                    
                print("\n4. Persistent Memory Raw Query (by user_id if exists):")
                try:
                    cur.execute("""
                        SELECT * FROM persistent_memory 
                        WHERE user_id = %s
                    """, (user_id,))
                    row = cur.fetchone()
                    if row:
                        print(f"   Found data: {row}")
                    else:
                        print("   No data found")
                except psycopg2.errors.UndefinedColumn:
                    print("   Column 'user_id' does not exist")
                    
    except Exception as e:
        print(f"Error checking raw data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Debug memory retrieval issues")
    parser.add_argument("--session-id", default="test-session", help="Session ID to test")
    parser.add_argument("--user-id", default="test-user", help="User ID to test")
    parser.add_argument("--insert-test-data", action="store_true", help="Insert test data")
    parser.add_argument("--fix-schema", action="store_true", help="Apply schema fixes")
    
    args = parser.parse_args()
    
    # Check current schema
    check_database_schema()
    
    # Apply schema fixes if requested
    if args.fix_schema:
        print("\n=== Applying Schema Fixes ===")
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    # Read and execute the fix SQL
                    fix_sql_path = os.path.join(os.path.dirname(__file__), "db_schema_fix.sql")
                    with open(fix_sql_path, 'r') as f:
                        sql = f.read()
                    cur.execute(sql)
                    conn.commit()
                    print("✅ Schema fixes applied")
        except Exception as e:
            print(f"❌ Error applying fixes: {e}")
    
    # Insert test data if requested
    if args.insert_test_data:
        insert_test_data(args.session_id, args.user_id)
    
    # Check raw data
    check_raw_data(args.session_id, args.user_id)
    
    # Test retrieval functions
    test_memory_retrieval(args.session_id, args.user_id)