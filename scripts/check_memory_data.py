#!/usr/bin/env python3
"""
Check what data exists in memory tables
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "xavigate")
DB_USER = os.getenv("POSTGRES_USER", "xavigate_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "changeme")

def check_data():
    """Check data in memory tables"""
    
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    try:
        with conn.cursor() as cur:
            # Check session_memory data
            print("=== Session Memory Data ===")
            cur.execute("""
                SELECT COUNT(*) as total, 
                       COUNT(DISTINCT session_id) as sessions,
                       COUNT(DISTINCT user_id) as users
                FROM session_memory;
            """)
            row = cur.fetchone()
            print(f"Total records: {row[0]}")
            print(f"Unique sessions: {row[1]}")
            print(f"Unique users: {row[2]}")
            
            # Show recent entries
            cur.execute("""
                SELECT session_id, user_id, role, 
                       SUBSTRING(message, 1, 50) as message_preview,
                       created_at
                FROM session_memory
                ORDER BY created_at DESC
                LIMIT 5;
            """)
            
            print("\nRecent entries:")
            for row in cur.fetchall():
                print(f"  Session: {row[0]}")
                print(f"  User: {row[1]}")
                print(f"  Role: {row[2]}")
                print(f"  Message: {row[3]}...")
                print(f"  Time: {row[4]}")
                print()
            
            # Check persistent_memory data
            print("\n=== Persistent Memory Data ===")
            cur.execute("""
                SELECT COUNT(*) as total,
                       COUNT(CASE WHEN summary IS NOT NULL AND summary != '' THEN 1 END) as with_summary
                FROM persistent_memory;
            """)
            row = cur.fetchone()
            print(f"Total users: {row[0]}")
            print(f"Users with summaries: {row[1]}")
            
            # Show sample summaries
            cur.execute("""
                SELECT user_id, 
                       SUBSTRING(summary, 1, 100) as summary_preview,
                       updated_at
                FROM persistent_memory
                WHERE summary IS NOT NULL AND summary != ''
                ORDER BY updated_at DESC
                LIMIT 3;
            """)
            
            print("\nRecent summaries:")
            for row in cur.fetchall():
                print(f"  User: {row[0]}")
                print(f"  Summary: {row[1]}...")
                print(f"  Updated: {row[2]}")
                print()
            
            # Check if the test session has data
            print("\n=== Test Session Check ===")
            test_sessions = ['test-session-1735292684', 'test-session-1735292685']
            for session_id in test_sessions:
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM session_memory 
                    WHERE session_id = %s
                """, (session_id,))
                count = cur.fetchone()[0]
                print(f"Session {session_id}: {count} messages")
                
    except Exception as e:
        print(f"Error checking data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_data()