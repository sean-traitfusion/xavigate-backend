#!/usr/bin/env python3
"""
Fix database schema mismatch for memory tables
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

def fix_schema():
    """Fix the schema mismatch in memory tables"""
    
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    try:
        with conn.cursor() as cur:
            # Check current schema
            print("Checking current schema...")
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'session_memory'
                ORDER BY ordinal_position;
            """)
            columns = [row[0] for row in cur.fetchall()]
            print(f"Current session_memory columns: {columns}")
            
            # Add missing columns if they don't exist
            if 'user_id' not in columns:
                print("Adding user_id column...")
                cur.execute("""
                    ALTER TABLE session_memory 
                    ADD COLUMN user_id VARCHAR(255);
                """)
                
            if 'session_id' not in columns:
                print("Adding session_id column...")
                cur.execute("""
                    ALTER TABLE session_memory 
                    ADD COLUMN session_id VARCHAR(255);
                """)
                
                # Create index on session_id
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_session_memory_session_id 
                    ON session_memory (session_id);
                """)
            
            # Migrate data from uuid to session_id if needed
            if 'uuid' in columns and 'session_id' in columns:
                print("Migrating uuid data to session_id...")
                cur.execute("""
                    UPDATE session_memory 
                    SET session_id = uuid 
                    WHERE session_id IS NULL AND uuid IS NOT NULL;
                """)
            
            # Check persistent_memory table
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'persistent_memory'
                ORDER BY ordinal_position;
            """)
            p_columns = [row[0] for row in cur.fetchall()]
            print(f"Current persistent_memory columns: {p_columns}")
            
            # Add user_id column if missing
            if 'user_id' not in p_columns:
                print("Adding user_id column to persistent_memory...")
                cur.execute("""
                    ALTER TABLE persistent_memory 
                    ADD COLUMN user_id VARCHAR(255);
                """)
                
                # Migrate uuid to user_id
                cur.execute("""
                    UPDATE persistent_memory 
                    SET user_id = uuid 
                    WHERE user_id IS NULL;
                """)
            
            conn.commit()
            print("Schema fix completed successfully!")
            
            # Show final schema
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'session_memory'
                ORDER BY ordinal_position;
            """)
            print("\nFinal session_memory schema:")
            for row in cur.fetchall():
                print(f"  {row[0]}: {row[1]}")
                
    except Exception as e:
        print(f"Error fixing schema: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_schema()