# memory/db.py
"""
Database connection management for memory operations
Provides error handling and connection pooling
"""
import os
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from typing import Any, Callable, Optional
import traceback

# Load environment variables
ENV = os.getenv("ENV", "dev")
# Use same env vars as the rest of the application
DB_HOST = os.getenv("POSTGRES_HOST", os.getenv("DB_HOST", "localhost"))
DB_PORT = os.getenv("POSTGRES_PORT", os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", os.getenv("DB_NAME", "postgres"))
DB_USER = os.getenv("POSTGRES_USER", os.getenv("DB_USER", "postgres"))
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", os.getenv("DB_PASSWORD", ""))

# Connection pool for production
_connection_pool: Optional[pool.SimpleConnectionPool] = None

def _initialize_pool():
    """Initialize the connection pool"""
    global _connection_pool
    if ENV != "dev" and _connection_pool is None:
        try:
            _connection_pool = pool.SimpleConnectionPool(
                1, 10,  # min and max connections
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("✅ Database connection pool initialized")
        except Exception as e:
            print(f"❌ Failed to initialize connection pool: {e}")
            raise

@contextmanager
def get_connection():
    """Get a database connection from the pool"""
    if ENV == "dev":
        # In dev mode, use shared connection from parent module
        from shared.db import get_connection as shared_get_connection
        conn = shared_get_connection()
        try:
            yield conn
        finally:
            pass  # Don't close shared connection
    else:
        # In production, use connection pool
        if _connection_pool is None:
            _initialize_pool()
        
        conn = _connection_pool.getconn()
        try:
            yield conn
        finally:
            _connection_pool.putconn(conn)

def execute_db_operation(operation: Callable, *args, **kwargs) -> Any:
    """
    Execute a database operation with error handling and retry logic
    
    Args:
        operation: Function to execute that takes connection as first argument
        *args: Arguments to pass to the operation
        **kwargs: Keyword arguments to pass to the operation
        
    Returns:
        Result of the operation
    """
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            result = operation(*args, **kwargs)
            return result
        except psycopg2.OperationalError as e:
            retry_count += 1
            if retry_count >= max_retries:
                print(f"❌ Database operation failed after {max_retries} retries: {e}")
                raise
            print(f"⚠️ Database connection error, retrying ({retry_count}/{max_retries})...")
            # Reset connection pool if needed
            if _connection_pool:
                _connection_pool.closeall()
                _initialize_pool()
        except Exception as e:
            print(f"❌ Database operation error: {e}")
            traceback.print_exc()
            raise

def initialize_memory_tables():
    """Initialize all memory-related tables"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Session memory table
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
                ON session_memory (user_id, created_at);
            """)
            
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_memory_session 
                ON session_memory (session_id, created_at);
            """)
            
            # Persistent memory table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS persistent_memory (
                    user_id VARCHAR(255) PRIMARY KEY,
                    summary TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Summarization events table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS summarization_events (
                    id SERIAL PRIMARY KEY,
                    uuid VARCHAR(255) NOT NULL,
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
                CREATE INDEX IF NOT EXISTS idx_summarization_events_uuid_created 
                ON summarization_events (uuid, created_at);
            """)
            
            # Session prompts table (for debugging)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS session_prompts (
                    id SERIAL PRIMARY KEY,
                    uuid VARCHAR(255) NOT NULL,
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
                CREATE INDEX IF NOT EXISTS idx_session_prompts_uuid 
                ON session_prompts (uuid);
            """)
            
            # Compression events table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS compression_events (
                    id SERIAL PRIMARY KEY,
                    uuid VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    original_size INTEGER,
                    compressed_size INTEGER,
                    compression_ratio FLOAT,
                    compression_count INTEGER,
                    model_used VARCHAR(100)
                );
            """)
            
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_compression_events_uuid 
                ON compression_events (uuid);
            """)
            
            # Interaction logs table (for historical data)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS interaction_logs (
                    id SERIAL PRIMARY KEY,
                    uuid VARCHAR(255) NOT NULL,
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
                CREATE INDEX IF NOT EXISTS idx_interaction_logs_uuid_created 
                ON interaction_logs (uuid, created_at);
            """)
            
            # User identity table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_identity (
                    uuid VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            conn.commit()
            print("✅ Memory tables initialized")