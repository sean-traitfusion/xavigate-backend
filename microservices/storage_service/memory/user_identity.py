# memory/user_identity.py
"""
User identity management for memory system
"""
from typing import Optional, Dict, Any
from .db import get_connection, execute_db_operation
from datetime import datetime

def _upsert_user_impl(user_id: str, username: str, full_name: Optional[str] = None):
    """Implementation of upsert_user without error handling"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO user_identity (user_id, username, full_name)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE
                SET username = EXCLUDED.username,
                    full_name = EXCLUDED.full_name,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (user_id, username, full_name)
            )
            conn.commit()

def upsert_user(user_id: str, username: str, full_name: Optional[str] = None):
    """
    Insert or update user information.
    """
    return execute_db_operation(_upsert_user_impl, user_id, username, full_name)

def _get_user_impl(user_id: str) -> Optional[Dict[str, Any]]:
    """Implementation of get_user without error handling"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT user_id, username, full_name, created_at, updated_at FROM user_identity WHERE user_id = %s",
                (user_id,)
            )
            row = cur.fetchone()
            if row:
                return {
                    "user_id": row[0],
                    "username": row[1],
                    "full_name": row[2],
                    "created_at": row[3].isoformat() if row[3] else None,
                    "updated_at": row[4].isoformat() if row[4] else None
                }
            return None

def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve user information by user ID.
    """
    return execute_db_operation(_get_user_impl, user_id)