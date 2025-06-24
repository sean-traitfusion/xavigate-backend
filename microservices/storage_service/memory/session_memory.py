# memory/session_memory.py
"""
Enhanced session memory management with character-based limits and auto-summarization
Based on Mobeus architecture
"""
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from .db import get_connection, execute_db_operation
from config import runtime_config
import json

def get_session_memory_limit() -> int:
    """Get current session memory character limit from config"""
    return runtime_config.get("SESSION_MEMORY_CHAR_LIMIT", 15000)

def get_summary_prompt() -> str:
    """Get summarization prompt from config"""
    return runtime_config.get("SESSION_SUMMARY_PROMPT")

def _log_interaction_impl(user_id: str, session_id: str, role: str, message: str):
    """Implementation of log_interaction without error handling"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO session_memory (user_id, session_id, role, message)
                VALUES (%s, %s, %s, %s);
            """, (user_id, session_id, role, message))
            conn.commit()

def log_interaction(user_id: str, session_id: str, role: str, message: str):
    """
    Log a user or assistant interaction with automatic memory management
    """
    # CRITICAL: Check memory size BEFORE adding new content
    current_size = get_session_memory_size(session_id)
    new_message_size = len(role) + len(message) + 4
    limit = get_session_memory_limit()
    
    # If adding this message would exceed 70% of limit, summarize FIRST
    if runtime_config.get("AUTO_SUMMARY_ENABLED", True):
        if (current_size + new_message_size) >= (limit * 0.7):
            print(f"⚠️ Session memory would exceed 70% limit with new message ({current_size + new_message_size}/{limit} chars). Summarizing BEFORE adding...")
            summarize_and_archive_session(user_id, session_id, "pre_limit")
            
            # Check if summarization worked
            new_size = get_session_memory_size(session_id)
            if new_size > (limit * 0.5):
                # If still too big after summarization, force clear
                print(f"🚨 Session memory still too large after summarization ({new_size} chars), forcing clear")
                clear_session_memory(session_id)
    
    # Now safe to log the new interaction
    result = execute_db_operation(_log_interaction_impl, user_id, session_id, role, message)
    
    # Double-check after adding (safety net)
    if runtime_config.get("AUTO_SUMMARY_ENABLED", True):
        check_and_manage_memory(user_id, session_id)
    
    return result

def _get_session_memory_size_impl(session_id: str) -> int:
    """Get total character count of session memory for a session"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COALESCE(SUM(LENGTH(role) + LENGTH(message) + 4), 0) as total_chars
                FROM session_memory
                WHERE session_id = %s
            """, (session_id,))
            row = cur.fetchone()
            return row[0] if row else 0

def get_session_memory_size(session_id: str) -> int:
    """Get total character count of session memory for a session"""
    return execute_db_operation(_get_session_memory_size_impl, session_id)

def _get_all_session_memory_impl(session_id: str) -> List[Dict[str, Any]]:
    """Get ALL session memory for a session (not limited by count)"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT role, message, created_at FROM session_memory
                WHERE session_id = %s
                ORDER BY created_at ASC
            """, (session_id,))
            rows = cur.fetchall()
            return [{"role": r, "message": m, "created_at": c} for r, m, c in rows]

def get_all_session_memory(session_id: str) -> List[Dict[str, Any]]:
    """
    Get ALL session memory for a session (character-based, not count-based)
    """
    return execute_db_operation(_get_all_session_memory_impl, session_id)

def _format_conversation_for_summary_impl(session_id: str) -> str:
    """Format conversation for summarization"""
    interactions = get_all_session_memory(session_id)
    conversation_lines = []
    
    for interaction in interactions:
        role = interaction["role"].title()  # User/Assistant
        message = interaction["message"]
        conversation_lines.append(f"{role}: {message}")
    
    return "\n".join(conversation_lines)

def format_conversation_for_summary(session_id: str) -> str:
    """Format conversation text for summarization"""
    return execute_db_operation(_format_conversation_for_summary_impl, session_id)

def _clear_session_memory_impl(session_id: str):
    """Clear all session memory for a session"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM session_memory WHERE session_id = %s", (session_id,))
            conn.commit()

def clear_session_memory(session_id: str):
    """Clear all session memory for a session"""
    return execute_db_operation(_clear_session_memory_impl, session_id)

def check_and_manage_memory(user_id: str, session_id: str):
    """
    Check if session memory needs to be summarized and managed
    This is called after each interaction
    """
    memory_size = get_session_memory_size(session_id)
    limit = get_session_memory_limit()
    
    # Lower threshold to 80% to ensure we never get close to 20k
    if memory_size >= (limit * 0.8):
        print(f"📝 Session memory for user {user_id} session {session_id} approaching limit ({memory_size}/{limit} chars). Triggering summarization...")
        result = summarize_and_archive_session(user_id, session_id, "auto_limit")
        
        # If summarization failed and memory is still large, force clear it
        if not result:
            final_size = get_session_memory_size(session_id)
            if final_size >= limit:
                print(f"🚨 EMERGENCY: Force clearing session memory that failed to summarize ({final_size} chars)")
                clear_session_memory(session_id)

def log_summarization_event(user_id: str, session_id: str, event_type: str, details: Optional[dict] = None):
    """Log summarization events for dashboard visibility - now to both file AND database"""
    
    # File logging (for backwards compatibility)
    log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    try:
        with open(os.path.join(log_dir, "summarization_events.jsonl"), "a") as f:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "session_id": session_id,
                "event_type": event_type,
                "details": details or {}
            }
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"⚠️ Failed to log to file: {e}")
    
    # Database logging
    def _log_to_db():
        with get_connection() as conn:
            with conn.cursor() as cur:
                details_dict = details or {}
                # CRITICAL: In this codebase, 'uuid' column actually stores user_id values!
                # See debug_disaster.md for details on this confusion
                cur.execute("""
                    INSERT INTO summarization_events 
                    (uuid, event_type, trigger_reason, conversation_length, 
                     summary_length, summary_generated, chars_before, chars_after, details, user_id, session_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    user_id,  # uuid column MUST be user_id (see debug_disaster.md)
                    event_type,
                    details_dict.get('trigger_reason', event_type),
                    details_dict.get('conversation_length', 0),
                    len(details_dict.get('summary', '')),  # summary_length
                    details_dict.get('summary', ''),
                    details_dict.get('chars_before', 0),
                    details_dict.get('chars_after', 0),
                    json.dumps(details_dict),
                    user_id,  # user_id column (redundant but needed if column exists)
                    session_id  # session_id column
                ))
                conn.commit()
    
    execute_db_operation(_log_to_db)

def store_session_prompt(user_id: str, session_id: str, prompt_data: dict):
    """Store the actual prompt used for a session - for debugging"""
    def _store_impl():
        with get_connection() as conn:
            with conn.cursor() as cur:
                final_prompt = prompt_data.get('final_prompt', '')
                prompt_length = len(final_prompt)
                
                cur.execute("""
                    INSERT INTO session_prompts 
                    (user_id, session_id, system_prompt, persistent_summary, session_context, 
                     final_prompt, prompt_length, estimated_tokens, strategy, model)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    user_id,
                    session_id,
                    prompt_data.get('system_prompt', ''),
                    prompt_data.get('persistent_summary', ''),
                    prompt_data.get('session_context', ''),
                    final_prompt,
                    prompt_length,
                    prompt_data.get('estimated_tokens', 0),
                    prompt_data.get('strategy', 'auto'),
                    prompt_data.get('model', '')
                ))
                conn.commit()
    
    execute_db_operation(_store_impl)

def summarize_and_archive_session(user_id: str, session_id: str, reason: str = "auto_limit"):
    """
    Summarize current session memory and move it to persistent memory
    """
    try:
        # Store session snapshot before summarization
        interactions_stored = store_session_snapshot_before_summarization(user_id, session_id, reason)
        
        # Get conversation text for summarization
        conversation_text = format_conversation_for_summary(session_id)
        chars_before = len(conversation_text)
        
        if not conversation_text.strip():
            print(f"⚠️ No conversation to summarize for user {user_id} session {session_id}")
            return
        
        # Generate summary using OpenAI
        summary = generate_conversation_summary(conversation_text)
        
        if summary:
            # Store summary in persistent memory
            from .persistent_memory import append_to_summary
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            summary_with_timestamp = f"[{timestamp}] {summary}"
            append_to_summary(user_id, summary_with_timestamp)
            
            # Log the event
            log_summarization_event(user_id, session_id, reason, {
                "conversation_length": chars_before,
                "summary_length": len(summary),
                "summary": summary,
                "chars_before": chars_before,
                "chars_after": 0,
                "interactions_preserved": interactions_stored,
                "timestamp": timestamp,
                "trigger_reason": reason
            })
            
            # Clear session memory
            clear_session_memory(session_id)
            
            print(f"✅ Session memory summarized and archived for user {user_id} session {session_id}")
            return True
        else:
            print(f"⚠️ Failed to generate summary for user {user_id} session {session_id}")
            
            # CRITICAL FIX: Store raw conversation as fallback when summarization fails
            if chars_before > get_session_memory_limit() * 2:
                print(f"🚨 Session memory critically oversized ({chars_before} chars), storing raw conversation as fallback")
                
                # Store the raw conversation in persistent memory as a fallback
                from .persistent_memory import append_to_summary
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                # Truncate if necessary to prevent persistent memory overflow
                max_raw_size = 10000  # Store up to 10k chars of raw conversation
                if chars_before > max_raw_size:
                    truncated_conversation = conversation_text[-max_raw_size:]
                    fallback_summary = f"[{timestamp}] [AUTOSUMMARY FAILED - RAW CONVERSATION TRUNCATED]: ...{truncated_conversation}"
                else:
                    fallback_summary = f"[{timestamp}] [AUTOSUMMARY FAILED - RAW CONVERSATION]: {conversation_text}"
                
                append_to_summary(user_id, fallback_summary)
                
                # Log the event
                log_summarization_event(user_id, session_id, f"{reason}_failed_cleared", {
                    "conversation_length": chars_before,
                    "summary_length": len(fallback_summary),
                    "summary": "FAILED - Raw conversation stored as fallback",
                    "chars_before": chars_before,
                    "chars_after": 0,
                    "interactions_preserved": interactions_stored,
                    "error": "Summarization failed - stored raw conversation",
                    "trigger_reason": reason
                })
                
                # Now clear session memory
                clear_session_memory(session_id)
                print(f"🧹 Cleared oversized session memory after storing fallback for user {user_id} session {session_id}")
            
            return False
            
    except Exception as e:
        print(f"❌ Error summarizing session for user {user_id} session {session_id}: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_conversation_summary(conversation_text: str) -> Optional[str]:
    """
    Generate a summary of the conversation using OpenAI
    """
    try:
        from openai import OpenAI
        import os
        import time
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print(f"❌ OPENAI_API_KEY not found in environment")
            return None
        
        client = OpenAI(api_key=api_key)
        
        # Get model and temperature from config
        model = runtime_config.get("GPT_MODEL", "gpt-4")
        temperature = runtime_config.get("SUMMARY_TEMPERATURE", 0.3)
        
        # Format the prompt
        prompt = get_summary_prompt().format(conversation_text=conversation_text)
        
        # Implement retry logic with exponential backoff for rate limits
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                # Keep conversation size reasonable for summarization
                conversation_to_summarize = conversation_text
                if len(conversation_text) > 20000:
                    # Take only the most recent 20k chars to ensure we never exceed context
                    conversation_to_summarize = conversation_text[-20000:]
                    print(f"📊 Truncating conversation from {len(conversation_text)} to 20k chars for summarization")
                
                # Use the truncated conversation in the prompt
                safe_prompt = get_summary_prompt().format(conversation_text=conversation_to_summarize)
                
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that creates concise, comprehensive conversation summaries."},
                        {"role": "user", "content": safe_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=800  # Slightly reduced to ensure we stay within limits
                )
                
                summary = response.choices[0].message.content.strip()
                return summary
                
            except Exception as api_error:
                error_str = str(api_error)
                
                # Handle rate limits
                if "rate_limit_exceeded" in error_str:
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2 ** attempt)
                        print(f"⏳ Rate limit hit, waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"❌ Rate limit exceeded after {max_retries} attempts")
                        
                # Handle context length errors
                elif "context_length_exceeded" in error_str:
                    print(f"❌ Context too long for {model}, truncating conversation")
                    # Truncate to last 20k chars and retry
                    truncated_text = conversation_text[-20000:]
                    truncated_prompt = get_summary_prompt().format(conversation_text=truncated_text)
                    try:
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo-16k",
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant that creates concise summaries."},
                                {"role": "user", "content": truncated_prompt}
                            ],
                            temperature=temperature,
                            max_tokens=500
                        )
                        return "[TRUNCATED] " + response.choices[0].message.content.strip()
                    except:
                        return None
                else:
                    print(f"❌ API error: {api_error}")
                    return None
        
        return None
        
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return None

def get_memory_stats(user_id: str, session_id: str) -> Dict[str, Any]:
    """
    Get memory statistics for debugging/dashboard
    """
    try:
        session_size = get_session_memory_size(session_id)
        limit = get_session_memory_limit()
        
        # Get persistent memory info
        from .persistent_memory import get_summary
        persistent_summary = get_summary(user_id)
        persistent_size = len(persistent_summary) if persistent_summary else 0
        
        return {
            "session_memory_chars": session_size,
            "session_memory_limit": limit,
            "session_memory_usage_percent": (session_size / limit * 100) if limit > 0 else 0,
            "persistent_memory_chars": persistent_size,
            "has_persistent_memory": persistent_summary is not None
        }
    except Exception as e:
        print(f"❌ Error getting memory stats: {e}")
        return {}

def force_session_summary(user_id: str, session_id: str, reason: str = "user_requested"):
    """
    Force summarization with comprehensive logging and validation
    """
    try:
        print(f"🤖 FORCE SUMMARIZATION: Starting for user {user_id} session {session_id} - reason: {reason}")
        
        # Check if there's anything to summarize
        current_size = get_session_memory_size(session_id)
        print(f"📊 CURRENT SESSION SIZE: {current_size} chars")
        
        # For auto_disconnect, check if we've already summarized recently to avoid duplicates
        if reason == "auto_disconnect":
            # Check if we've already summarized recently (within last 5 minutes)
            def _check_recent_summary():
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT COUNT(*) FROM summarization_events
                            WHERE user_id = %s 
                            AND session_id = %s
                            AND created_at > NOW() - INTERVAL '5 minutes'
                            AND event_type != 'auto_disconnect'
                        """, (user_id, session_id))
                        return cur.fetchone()[0] > 0
            
            has_recent_summary = execute_db_operation(_check_recent_summary)
            if has_recent_summary and current_size == 0:
                print(f"✅ Session already summarized recently and cleared, skipping duplicate")
                return True
        
        if current_size == 0:
            print(f"⚠️ Session already empty, nothing to summarize")
            return True
            
        result = summarize_and_archive_session(user_id, session_id, reason)
        
        # Verify it worked
        final_size = get_session_memory_size(session_id)
        print(f"📊 FINAL SESSION SIZE: {final_size} chars")
        
        return result
            
    except Exception as e:
        print(f"❌ FORCE SUMMARIZATION FAILED for user {user_id} session {session_id}: {e}")
        import traceback
        traceback.print_exc()
        return False

def store_session_snapshot_before_summarization(user_id: str, session_id: str, reason: str):
    """
    Store complete session data BEFORE summarization for historical analysis
    """
    try:
        # Get all current session data
        conversation = get_all_session_memory(session_id)
        if not conversation:
            return 0
            
        # Store each interaction in interaction_logs for historical analysis
        snapshot_time = datetime.now()
        
        def _store_snapshot():
            with get_connection() as conn:
                with conn.cursor() as cur:
                    # Create pairs of user->assistant interactions
                    current_user_msg = None
                    interaction_count = 0
                    
                    for msg in conversation:
                        if msg["role"] == "user":
                            current_user_msg = msg["message"]
                        elif msg["role"] == "assistant" and current_user_msg:
                            interaction_count += 1
                            # Add microseconds to ensure uniqueness even in rapid succession
                            interaction_id = f"{user_id}_{session_id}_snapshot_{snapshot_time.strftime('%Y%m%d_%H%M%S_%f')}_{interaction_count}"
                            
                            cur.execute("""
                                INSERT INTO interaction_logs 
                                (uuid, interaction_id, created_at, user_message, assistant_response, 
                                 rag_context, strategy, model, tools_called,
                                 user_id, session_id)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (interaction_id) DO UPDATE SET
                                    created_at = EXCLUDED.created_at
                            """, (
                                user_id,  # This goes into 'uuid' column which contains user_id values
                                interaction_id,
                                msg.get("created_at", snapshot_time),
                                current_user_msg,
                                msg["message"],
                                f"Pre-summarization snapshot - {reason}",
                                "historical_data",
                                runtime_config.get("GPT_MODEL", "gpt-4"),
                                "Historical snapshot - no tool data",
                                user_id,  # for user_id column
                                session_id  # for session_id column
                            ))
                            current_user_msg = None
                    
                    conn.commit()
                    return interaction_count
        
        return execute_db_operation(_store_snapshot)
        
    except Exception as e:
        print(f"❌ Error storing session snapshot: {e}")
        return 0

def debug_prompt_storage(user_id: str):
    """Debug function to check what prompt data exists for a user"""
    def _debug_impl():
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Check if table exists
                cur.execute("""
                    SELECT COUNT(*) FROM information_schema.tables 
                    WHERE table_name = 'session_prompts'
                """)
                table_exists = cur.fetchone()[0] > 0
                
                if not table_exists:
                    return {"error": "session_prompts table does not exist"}
                
                # Check all records for this user
                cur.execute("""
                    SELECT id, created_at, prompt_length, strategy, model, 
                           LENGTH(final_prompt) as actual_prompt_length
                    FROM session_prompts 
                    WHERE user_id = %s 
                    ORDER BY created_at DESC
                """, (user_id,))
                
                records = []
                for row in cur.fetchall():
                    records.append({
                        "id": row[0],
                        "created_at": row[1].isoformat() if row[1] else None,
                        "stored_prompt_length": row[2],
                        "actual_prompt_length": row[5],
                        "strategy": row[3],
                        "model": row[4]
                    })
                
                return {
                    "total_records": len(records),
                    "records": records
                }
    
    result = execute_db_operation(_debug_impl)
    print(f"🔍 PROMPT DEBUG for user {user_id}: {result}")
    return result