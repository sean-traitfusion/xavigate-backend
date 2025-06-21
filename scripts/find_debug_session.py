#!/usr/bin/env python3
"""
Find session data for debug-test-user
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

def find_session():
    """Find session for debug-test-user"""
    
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    try:
        with conn.cursor() as cur:
            # Look for any session with debug-test-user
            print("Looking for debug-test-user sessions...")
            cur.execute("""
                SELECT DISTINCT session_id, user_id, COUNT(*) as msg_count
                FROM session_memory
                WHERE user_id LIKE '%debug%' OR user_id = 'debug-test-user'
                GROUP BY session_id, user_id;
            """)
            
            rows = cur.fetchall()
            if rows:
                print("Found sessions:")
                for row in rows:
                    print(f"  Session: {row[0]}, User: {row[1]}, Messages: {row[2]}")
            else:
                print("No sessions found for debug-test-user")
                
            # Check interaction logs table
            print("\nChecking interaction_logs for debug-test-user...")
            cur.execute("""
                SELECT uuid, interaction_id, created_at, 
                       SUBSTRING(user_message, 1, 50) as msg
                FROM interaction_logs
                WHERE uuid = 'debug-test-user' OR uuid LIKE '%debug%'
                ORDER BY created_at DESC
                LIMIT 5;
            """)
            
            rows = cur.fetchall()
            if rows:
                print("Found in interaction_logs:")
                for row in rows:
                    print(f"  User: {row[0]}")
                    print(f"  ID: {row[1]}")
                    print(f"  Time: {row[2]}")
                    print(f"  Message: {row[3]}...")
                    print()
            else:
                print("No interaction logs found")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    find_session()