#!/usr/bin/env python3
"""
Check if prompts are being saved
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

def check_prompts():
    """Check prompt data"""
    
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    try:
        with conn.cursor() as cur:
            # Check if session_prompts table exists
            cur.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_name = 'session_prompts'
            """)
            exists = cur.fetchone()[0]
            
            if not exists:
                print("session_prompts table does not exist!")
                return
                
            print("=== Session Prompts Data ===")
            cur.execute("SELECT COUNT(*) FROM session_prompts")
            count = cur.fetchone()[0]
            print(f"Total prompts: {count}")
            
            if count > 0:
                # Show recent prompts
                cur.execute("""
                    SELECT uuid, 
                           SUBSTRING(system_prompt, 1, 50) as sys_preview,
                           SUBSTRING(final_prompt, 1, 50) as final_preview,
                           created_at
                    FROM session_prompts
                    ORDER BY created_at DESC
                    LIMIT 5
                """)
                
                print("\nRecent prompts:")
                for row in cur.fetchall():
                    print(f"  User: {row[0]}")
                    print(f"  System: {row[1]}...")
                    print(f"  Final: {row[2]}...")
                    print(f"  Time: {row[3]}")
                    print()
                    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_prompts()