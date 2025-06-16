# memory/client.py
"""
High-level client for session and persistent memory operations.
Based on Mobeus architecture but adapted for Xavigate
"""
from typing import Any, Dict, List, Optional
from datetime import datetime

from .db import get_connection, execute_db_operation
from .session_memory import (
    log_interaction,
    get_session_memory_size,
    get_all_session_memory,
    format_conversation_for_summary,
    clear_session_memory,
    log_summarization_event,
    store_session_prompt,
    debug_prompt_storage,
    force_session_summary as force_summary_impl,
)
from .persistent_memory import (
    get_summary,
    append_to_summary,
    clear_summary,
)
from .user_identity import upsert_user, get_user

class MemoryClient:
    """Client to manage session and persistent memory operations."""

    def __init__(self):
        # Table initialization is handled by execute_db_operation wrapper.
        pass

    def log_interaction(self, user_id: str, session_id: str, role: str, message: str) -> Any:
        """Log a user or assistant interaction."""
        return log_interaction(user_id, session_id, role, message)

    def get_session_size(self, session_id: str) -> int:
        """Return total character count of session memory for a session."""
        return get_session_memory_size(session_id)

    def get_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Return all session memory entries for a session."""
        return get_all_session_memory(session_id) or []

    def clear_session(self, session_id: str) -> Any:
        """Clear all session memory for a session."""
        return clear_session_memory(session_id)

    def summarize_conversation(self, session_id: str) -> str:
        """Format conversation text for summarization."""
        return format_conversation_for_summary(session_id)

    def store_prompt(self, user_id: str, session_id: str, prompt_data: Dict[str, Any]) -> Any:
        """Store session prompt details for debugging."""
        return store_session_prompt(user_id, session_id, prompt_data)

    def debug_prompt_storage(self, user_id: str) -> Any:
        """Return debug info for stored prompts for a user."""
        return debug_prompt_storage(user_id)

    def get_conversation_data(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """Return current session and recent historical interaction data."""
        # inline historical retrieval as in legacy code
        def _get_historical() -> List[Dict[str, Any]]:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT user_message, assistant_response, created_at, interaction_id
                        FROM interaction_logs
                        WHERE user_id = %s
                        ORDER BY created_at DESC
                        LIMIT 5
                        """,
                        (user_id,),
                    )
                    rows = cur.fetchall()
            return [
                {
                    "user_message": row[0][:100] + "..." if row[0] and len(row[0]) > 100 else row[0],
                    "assistant_response": row[1][:100] + "..." if row[1] and len(row[1]) > 100 else row[1],
                    "created_at": row[2].isoformat() if row[2] else None,
                    "interaction_id": row[3],
                }
                for row in rows
            ]

        conversation = self.get_session(session_id)
        historical = execute_db_operation(_get_historical) or []
        return {
            "user_id": user_id,
            "session_id": session_id,
            "current_session_count": len(conversation),
            "current_session_preview": conversation[:2],
            "historical_interactions_count": len(historical),
            "historical_interactions_preview": historical,
        }

    def get_summary(self, user_id: str) -> Optional[str]:
        """Return the long-term summary for a user."""
        return get_summary(user_id)

    def append_summary(self, user_id: str, new_info: str) -> Any:
        """Append information to the persistent memory summary."""
        return append_to_summary(user_id, new_info)

    def clear_summary(self, user_id: str) -> Any:
        """Clear the persistent memory summary for a user."""
        return clear_summary(user_id)

    def upsert_user(self, user_id: str, username: str, full_name: str = None) -> Any:
        """Insert or update user information."""
        return upsert_user(user_id, username, full_name)

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user information by user ID."""
        return get_user(user_id)

    def force_session_summary(self, user_id: str, session_id: str, reason: str = "user_requested") -> bool:
        """Force summarization of current session memory and archive it to persistent memory."""
        return force_summary_impl(user_id, session_id, reason)