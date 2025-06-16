# memory/persistent_memory.py
"""
Persistent memory management for long-term user summaries
Based on Mobeus architecture
"""
from .db import get_connection, execute_db_operation
from typing import Optional
from datetime import datetime
from config import runtime_config

def _get_summary_impl(user_id: str) -> Optional[str]:
    """Implementation of get_summary without error handling"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT summary FROM persistent_memory WHERE user_id = %s",
                (user_id,)
            )
            row = cur.fetchone()
            return row[0] if row and row[0] is not None else None

def get_summary(user_id: str) -> Optional[str]:
    """
    Get long-term summary for a user.
    Returns the summary text if it exists, otherwise None.
    """
    return execute_db_operation(_get_summary_impl, user_id)

def _append_to_summary_impl(user_id: str, new_info: str):
    """Implementation of append_to_summary without error handling"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Get current summary
            cur.execute(
                "SELECT summary FROM persistent_memory WHERE user_id = %s",
                (user_id,)
            )
            row = cur.fetchone()
            current_summary = row[0] if row and row[0] else ""
            
            # Append new information
            if current_summary:
                updated_summary = f"{current_summary}\n{new_info}"
            else:
                updated_summary = new_info
            
            # Update the summary
            cur.execute(
                """
                INSERT INTO persistent_memory (user_id, summary)
                VALUES (%s, %s)
                ON CONFLICT (user_id) DO UPDATE
                SET summary = EXCLUDED.summary,
                    updated_at = CURRENT_TIMESTAMP
                """, (user_id, updated_summary)
            )
            conn.commit()

def append_to_summary(user_id: str, new_info: str):
    """
    Append new information to existing summary.
    If no summary exists, creates a new one.
    Also checks if compression is needed after appending.
    """
    result = execute_db_operation(_append_to_summary_impl, user_id, new_info)
    
    # Check if we need to compress after appending
    if runtime_config.get("AUTO_COMPRESSION_ENABLED", True):
        from .persistent_compression import check_and_compress_persistent_memory
        check_and_compress_persistent_memory(user_id)
    
    return result

def _clear_summary_impl(user_id: str):
    """Implementation of clear_summary without error handling"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM persistent_memory WHERE user_id = %s",
                (user_id,)
            )
            conn.commit()

def clear_summary(user_id: str):
    """
    Clear all persistent memory for a user.
    Returns True if successful, False otherwise.
    """
    try:
        execute_db_operation(_clear_summary_impl, user_id)
        return True
    except Exception as e:
        print(f"❌ Error clearing persistent memory for {user_id}: {e}")
        return False

def get_persistent_memory_size(user_id: str) -> int:
    """Get the current size of persistent memory for a user"""
    summary = get_summary(user_id)
    return len(summary) if summary else 0