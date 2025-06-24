#!/usr/bin/env python3
"""
Quick fix for summarization_events table and function.
This script updates the table schema and fixes the logging function.
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_PARAMS = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "database": os.getenv("POSTGRES_DATABASE", "xavigate"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres")
}

def fix_database_schema():
    """Fix the summarization_events table schema"""
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    
    try:
        # First, add the missing columns if they don't exist
        cursor.execute("""
            DO $$ 
            BEGIN
                -- Add user_id column if it doesn't exist
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'summarization_events' 
                    AND column_name = 'user_id'
                ) THEN
                    ALTER TABLE summarization_events 
                    ADD COLUMN user_id VARCHAR(255);
                END IF;

                -- Add session_id column if it doesn't exist
                IF NOT EXISTS (
                    SELECT 1 
                    FROM information_schema.columns 
                    WHERE table_name = 'summarization_events' 
                    AND column_name = 'session_id'
                ) THEN
                    ALTER TABLE summarization_events 
                    ADD COLUMN session_id VARCHAR(255);
                END IF;
            END $$;
        """)
        
        # Update existing rows to use uuid as user_id for backward compatibility
        cursor.execute("""
            UPDATE summarization_events 
            SET user_id = uuid,
                session_id = uuid
            WHERE user_id IS NULL OR session_id IS NULL;
        """)
        
        conn.commit()
        print("✅ Database schema fixed successfully")
        
    except Exception as e:
        print(f"❌ Error fixing database schema: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_database_schema()