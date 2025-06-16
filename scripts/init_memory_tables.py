#!/usr/bin/env python3
"""
Initialize or migrate database tables for the enhanced memory system
"""
import os
import sys
import psycopg2
from psycopg2 import sql

# Add microservices directory to the path to access shared.db module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'microservices'))

from shared.db import get_connection

def init_memory_tables():
    """Initialize all memory-related tables"""
    print("🔧 Initializing Memory System Tables")
    print("=" * 60)
    
    try:
        conn = get_connection()
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if we need to migrate existing session_memory table
        print("\n1️⃣ Checking existing tables...")
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'session_memory'
            ORDER BY ordinal_position
        """)
        existing_columns = cur.fetchall()
        
        if existing_columns:
            print("   Found existing session_memory table with columns:")
            for col in existing_columns:
                print(f"   - {col[0]}: {col[1]}")
            
            # Backup existing data if needed
            print("\n   ⚠️  Backing up existing session_memory data...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS session_memory_backup AS 
                SELECT * FROM session_memory
            """)
            
            # Drop the old table
            print("   Dropping old session_memory table...")
            cur.execute("DROP TABLE IF EXISTS session_memory CASCADE")
        
        # Create new session_memory table
        print("\n2️⃣ Creating new session_memory table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS session_memory (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                session_id VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create indexes
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_session_memory_user_created 
            ON session_memory(user_id, created_at);
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_session_memory_session 
            ON session_memory(session_id, created_at);
        """)
        print("   ✅ session_memory table created")
        
        # Create persistent_memory table
        print("\n3️⃣ Creating persistent_memory table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS persistent_memory (
                user_id VARCHAR(255) PRIMARY KEY,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("   ✅ persistent_memory table created")
        
        # Create summarization_events table
        print("\n4️⃣ Creating summarization_events table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS summarization_events (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                session_id VARCHAR(255),
                event_type VARCHAR(50),
                trigger_reason VARCHAR(100),
                conversation_length INTEGER,
                summary_length INTEGER,
                summary_generated TEXT,
                chars_before INTEGER,
                chars_after INTEGER,
                details JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_summarization_events_user_created 
            ON summarization_events(user_id, created_at);
        """)
        print("   ✅ summarization_events table created")
        
        # Create session_prompts table
        print("\n5️⃣ Creating session_prompts table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS session_prompts (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                session_id VARCHAR(255),
                system_prompt TEXT,
                persistent_summary TEXT,
                session_context TEXT,
                final_prompt TEXT,
                prompt_length INTEGER,
                estimated_tokens INTEGER,
                strategy VARCHAR(50),
                model VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_session_prompts_user 
            ON session_prompts(user_id);
        """)
        print("   ✅ session_prompts table created")
        
        # Create compression_events table
        print("\n6️⃣ Creating compression_events table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS compression_events (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                original_size INTEGER,
                compressed_size INTEGER,
                compression_ratio FLOAT,
                compression_count INTEGER,
                model_used VARCHAR(100)
            );
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_compression_events_user 
            ON compression_events(user_id);
        """)
        print("   ✅ compression_events table created")
        
        # Create interaction_logs table
        print("\n7️⃣ Creating interaction_logs table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS interaction_logs (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                session_id VARCHAR(255),
                interaction_id VARCHAR(255) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT,
                assistant_response TEXT,
                rag_context TEXT,
                strategy VARCHAR(100),
                model VARCHAR(100),
                tools_called TEXT
            );
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_interaction_logs_user_created 
            ON interaction_logs(user_id, created_at);
        """)
        print("   ✅ interaction_logs table created")
        
        # Create user_identity table
        print("\n8️⃣ Creating user_identity table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_identity (
                user_id VARCHAR(255) PRIMARY KEY,
                username VARCHAR(255),
                full_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("   ✅ user_identity table created")
        
        # Check if we have backup data to restore
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'session_memory_backup'
            );
        """)
        
        if cur.fetchone()[0]:
            print("\n9️⃣ Found backup data...")
            cur.execute("SELECT COUNT(*) FROM session_memory_backup")
            count = cur.fetchone()[0]
            print(f"   Backup contains {count} records")
            print("   (Migration of old data would need custom logic based on schema)")
        
        print("\n✅ All tables created successfully!")
        
        # Show final table status
        print("\n📊 Table Status:")
        tables = [
            'session_memory', 'persistent_memory', 'summarization_events',
            'session_prompts', 'compression_events', 'interaction_logs',
            'user_identity'
        ]
        
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"   - {table}: {count} records")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error initializing tables: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Memory System Database Initialization")
    print("=" * 60)
    print("This script will create all necessary tables for the enhanced memory system.")
    print("If tables exist, they will be backed up first.")
    
    response = input("\nProceed with initialization? (y/n): ")
    if response.lower() == 'y':
        if init_memory_tables():
            print("\n✅ Database initialization complete!")
            print("\nNext steps:")
            print("1. Restart the storage service")
            print("2. Run the test script again")
        else:
            print("\n❌ Database initialization failed!")
    else:
        print("\n❌ Initialization cancelled")