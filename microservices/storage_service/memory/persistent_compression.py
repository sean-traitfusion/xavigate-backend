# memory/persistent_compression.py
"""
Persistent memory compression logic
Based on Mobeus architecture
"""
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
import re
from config import runtime_config
from .persistent_memory import get_summary, clear_summary
from .db import get_connection, execute_db_operation
from .session_memory import log_summarization_event

def get_persistent_memory_limit() -> int:
    """Get persistent memory character limit from config"""
    return runtime_config.get("PERSISTENT_MEMORY_CHAR_LIMIT", 8000)

def get_compression_ratio() -> float:
    """Get target compression ratio from config"""
    return runtime_config.get("PERSISTENT_MEMORY_COMPRESSION_RATIO", 0.6)

def get_compression_model() -> str:
    """Get model to use for compression"""
    return runtime_config.get("PERSISTENT_MEMORY_COMPRESSION_MODEL", "gpt-4")

def get_min_compression_size() -> int:
    """Get minimum size before we stop compressing"""
    return runtime_config.get("PERSISTENT_MEMORY_MIN_SIZE", 1000)

def get_max_compressions() -> int:
    """Get maximum number of compressions allowed"""
    return runtime_config.get("PERSISTENT_MEMORY_MAX_COMPRESSIONS", 3)

def get_compression_count(summary: str) -> int:
    """
    Extract compression count from summary markers
    
    Looks for patterns like:
    - [COMPRESSED SUMMARY as of 2024-01-15]
    - [COMPRESSED 2x as of 2024-01-15]
    """
    if not summary:
        return 0
    
    # Look for compression markers
    compression_patterns = [
        r'\[COMPRESSED (\d+)x as of',  # [COMPRESSED 2x as of ...]
        r'\[COMPRESSED SUMMARY as of'   # [COMPRESSED SUMMARY as of ...] counts as 1
    ]
    
    for pattern in compression_patterns:
        match = re.search(pattern, summary)
        if match:
            if match.groups():
                return int(match.group(1))
            else:
                return 1  # Simple COMPRESSED SUMMARY marker
    
    return 0

def check_and_compress_persistent_memory(user_id: str) -> bool:
    """
    Check if persistent memory needs compression and perform it if necessary
    
    Returns:
        True if compression was performed, False otherwise
    """
    current_size = get_persistent_memory_size(user_id)
    limit = get_persistent_memory_limit()
    
    # Check if we need compression
    if current_size < (limit * 0.9):
        return False
    
    # Check compression count
    current_summary = get_summary(user_id)
    compression_count = get_compression_count(current_summary)
    
    # Log compression count but don't limit
    if compression_count >= get_max_compressions():
        print(f"📊 High compression count ({compression_count}) for {user_id}. Memory has been compressed multiple times.")
    
    # Check minimum size
    if current_size < get_min_compression_size():
        print(f"⚠️ Persistent memory for {user_id} is below minimum size ({current_size} chars). Skipping compression.")
        return False
    
    print(f"📝 Persistent memory for {user_id} approaching limit ({current_size}/{limit} chars). Triggering compression...")
    return compress_persistent_memory(user_id, compression_count)

def compress_persistent_memory(user_id: str, current_compression_count: int = 0) -> bool:
    """
    Compress persistent memory by creating a summary of summaries
    
    Args:
        user_id: User ID
        current_compression_count: Number of times this memory has been compressed
        
    Returns:
        True if successful, False otherwise
    """
    # Store backup of original summary first
    backup_summary = None
    
    try:
        current_summary = get_summary(user_id)
        if not current_summary:
            print(f"⚠️ No persistent memory to compress for {user_id}")
            return False
        
        # CRITICAL: Store backup before any operations
        backup_summary = current_summary
        original_size = len(current_summary)
        print(f"📝 COMPRESSING PERSISTENT MEMORY for {user_id}: {original_size} chars (compression #{current_compression_count + 1})")
        
        # Generate compressed summary using OpenAI
        compressed_summary, metadata = generate_compressed_summary(
            current_summary, 
            current_compression_count
        )
        
        # Validate compressed summary before proceeding
        if not compressed_summary or not compressed_summary.strip():
            print(f"❌ Compressed summary is empty or invalid for {user_id}")
            return False
        
        # Ensure compressed summary actually contains content
        if len(compressed_summary) < 10:  # Minimum reasonable summary length
            print(f"❌ Compressed summary too short ({len(compressed_summary)} chars) for {user_id}")
            return False
        
        # Add compression marker with count
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        compression_marker = f"[COMPRESSED {current_compression_count + 1}x as of {timestamp}]"
        if current_compression_count == 0:
            compression_marker = f"[COMPRESSED SUMMARY as of {timestamp}]"
        
        compressed_with_marker = f"{compression_marker}\n\n{compressed_summary}"
        
        # CRITICAL: Use atomic operation to replace memory
        success = _atomic_replace_summary(user_id, compressed_with_marker, backup_summary)
        
        if not success:
            print(f"❌ Failed to atomically replace summary for {user_id}")
            return False
        
        compressed_size = len(compressed_with_marker)
        compression_ratio = compressed_size / original_size if original_size > 0 else 1
        
        print(f"✅ Persistent memory compressed for {user_id}: {original_size} -> {compressed_size} chars ({compression_ratio:.2%})")
        
        # Log the compression event - need a dummy session_id for now
        log_summarization_event(user_id, "system_compression", "persistent_memory_compression", {
            "chars_before": original_size,
            "chars_after": compressed_size,
            "compression_ratio": compression_ratio,
            "compression_count": current_compression_count + 1,
            "compressed_summary_preview": compressed_summary[:500],
            "metadata": metadata,
            "timestamp": timestamp,
            "model_used": get_compression_model()
        })
        
        # Track compression in database
        _track_compression_event(user_id, original_size, compressed_size, current_compression_count + 1)
        
        return True
            
    except Exception as e:
        print(f"❌ Error compressing persistent memory for {user_id}: {e}")
        import traceback
        traceback.print_exc()
        
        # CRITICAL: Attempt to restore backup if available
        if backup_summary:
            print(f"🔄 Attempting to restore backup for {user_id}")
            try:
                _store_compressed_summary(user_id, backup_summary)
                print(f"✅ Backup restored successfully for {user_id}")
            except Exception as restore_error:
                print(f"❌ CRITICAL: Failed to restore backup for {user_id}: {restore_error}")
        
        return False

def generate_compressed_summary(current_summary: str, compression_count: int = 0) -> Tuple[Optional[str], Dict[str, Any]]:
    """
    Generate a compressed summary of the persistent memory using OpenAI
    
    Returns:
        Tuple of (compressed_summary, metadata)
    """
    # Validate input
    if not current_summary or not current_summary.strip():
        print(f"⚠️ Empty or invalid summary provided for compression")
        return None, {"error": "Empty input summary"}
    
    try:
        from openai import OpenAI
        import os
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print(f"❌ OPENAI_API_KEY not found in environment")
            return None, {"error": "Missing API key"}
        
        client = OpenAI(api_key=api_key)
        
        # Get configuration
        model = get_compression_model()
        temperature = runtime_config.get("SUMMARY_TEMPERATURE", 0.3)
        compression_ratio = get_compression_ratio()
        
        # Get compression prompt
        prompt_template = runtime_config.get("PERSISTENT_MEMORY_COMPRESSION_PROMPT")
        if not prompt_template:
            print(f"❌ Missing PERSISTENT_MEMORY_COMPRESSION_PROMPT in config")
            return None, {"error": "Missing prompt template"}
        
        prompt = prompt_template.format(
            current_summary=current_summary,
            compression_ratio=int((1 - compression_ratio) * 100)
        )
        
        # Estimate token count (rough approximation: 1 token ≈ 4 characters)
        estimated_tokens = len(prompt) / 4
        
        # Choose appropriate model based on token count
        if estimated_tokens > 6000:  # Leave buffer for response
            # Use 16k model for large contexts
            if "gpt-4" in model:
                model = "gpt-4-1106-preview"  # GPT-4 Turbo with 128k context
            else:
                model = "gpt-3.5-turbo-16k"  # 16k context window
            print(f"📝 Using large context model {model} for {estimated_tokens:.0f} estimated tokens")
        
        # If still too large, truncate the summary
        max_chars = 50000  # Roughly 12.5k tokens, leaving room for prompt template
        if len(current_summary) > max_chars:
            print(f"⚠️ Truncating summary from {len(current_summary)} to {max_chars} chars")
            current_summary = current_summary[:max_chars] + "\n\n[TRUNCATED DUE TO LENGTH]"
            prompt = prompt_template.format(
                current_summary=current_summary,
                compression_ratio=int((1 - compression_ratio) * 100)
            )
        
        # Track timing
        start_time = datetime.now()
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant that creates concise, comprehensive summaries while preserving ALL important information. Never lose personal details, names, dates, or specific facts."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=2500  # Reasonable limit for compressed summaries
            )
        except Exception as e:
            print(f"❌ OpenAI API error: {str(e)}")
            # If we still hit token limits, use a more aggressive truncation
            if "context_length_exceeded" in str(e):
                print(f"📝 Retrying with more aggressive truncation")
                current_summary = current_summary[:20000] + "\n\n[HEAVILY TRUNCATED DUE TO LENGTH]"
                prompt = prompt_template.format(
                    current_summary=current_summary,
                    compression_ratio=int((1 - compression_ratio) * 100)
                )
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a helpful assistant that creates concise, comprehensive summaries while preserving ALL important information. Never lose personal details, names, dates, or specific facts."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=2500
                )
            else:
                raise
        
        end_time = datetime.now()
        duration_ms = (end_time - start_time).total_seconds() * 1000
        
        # Validate response
        if not response or not response.choices or len(response.choices) == 0:
            print(f"❌ Invalid response from OpenAI API")
            return None, {"error": "Invalid API response"}
        
        content = response.choices[0].message.content
        compressed = content.strip() if content is not None else None
        
        # Validate output
        if not compressed:
            print(f"❌ OpenAI returned empty compression result")
            return None, {"error": "Empty compression result"}
        
        # Ensure we didn't lose too much content
        if len(compressed) < len(current_summary) * 0.1:  # Less than 10% of original
            print(f"⚠️ Compression too aggressive: {len(current_summary)} -> {len(compressed)} chars")
            # Don't fail, but log warning
        
        # Collect metadata
        metadata = {
            "model": model,
            "temperature": temperature,
            "compression_ratio_target": compression_ratio,
            "compression_count": compression_count,
            "duration_ms": duration_ms,
            "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            "completion_tokens": response.usage.completion_tokens if response.usage else 0,
            "total_tokens": response.usage.total_tokens if response.usage else 0,
            "original_length": len(current_summary),
            "compressed_length": len(compressed)
        }
        
        return compressed, metadata
        
    except Exception as e:
        print(f"❌ Error generating compressed summary: {e}")
        import traceback
        traceback.print_exc()
        return None, {"error": str(e)}

def _atomic_replace_summary(user_id: str, new_summary: str, backup_summary: str) -> bool:
    """
    Atomically replace persistent memory with new summary.
    Uses a database transaction to ensure either complete success or rollback.
    
    Args:
        user_id: User ID
        new_summary: New compressed summary to store
        backup_summary: Original summary for verification
        
    Returns:
        True if successful, False otherwise
    """
    def _atomic_replace_impl():
        with get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    # Start transaction
                    cur.execute("BEGIN")
                    
                    # Verify current summary matches our backup (ensure no concurrent modifications)
                    cur.execute(
                        "SELECT summary FROM persistent_memory WHERE user_id = %s FOR UPDATE",
                        (user_id,)
                    )
                    row = cur.fetchone()
                    current_db_summary = row[0] if row and row[0] else None
                    
                    if current_db_summary != backup_summary:
                        print(f"⚠️ Summary mismatch detected for {user_id}. Aborting compression.")
                        conn.rollback()
                        return False
                    
                    # Update with new compressed summary
                    cur.execute(
                        """
                        INSERT INTO persistent_memory (user_id, summary)
                        VALUES (%s, %s)
                        ON CONFLICT (user_id) DO UPDATE
                        SET summary = EXCLUDED.summary,
                            updated_at = CURRENT_TIMESTAMP
                        """, (user_id, new_summary)
                    )
                    
                    # Verify the update was successful
                    cur.execute(
                        "SELECT summary FROM persistent_memory WHERE user_id = %s",
                        (user_id,)
                    )
                    row = cur.fetchone()
                    stored_summary = row[0] if row and row[0] else None
                    
                    if stored_summary != new_summary:
                        print(f"❌ Failed to verify stored summary for {user_id}")
                        conn.rollback()
                        return False
                    
                    # Commit transaction
                    conn.commit()
                    return True
                    
            except Exception as e:
                print(f"❌ Error in atomic replace for {user_id}: {e}")
                conn.rollback()
                return False
    
    try:
        return execute_db_operation(_atomic_replace_impl)
    except Exception as e:
        print(f"❌ Failed to execute atomic replace for {user_id}: {e}")
        return False

def _store_compressed_summary(user_id: str, compressed_summary: str):
    """Store compressed summary in persistent memory"""
    def _store_impl():
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO persistent_memory (user_id, summary)
                    VALUES (%s, %s)
                    ON CONFLICT (user_id) DO UPDATE
                    SET summary = EXCLUDED.summary,
                        updated_at = CURRENT_TIMESTAMP
                    """, (user_id, compressed_summary)
                )
                conn.commit()
    
    execute_db_operation(_store_impl)

def _track_compression_event(user_id: str, original_size: int, compressed_size: int, compression_count: int):
    """Track compression event in database for analytics"""
    def _track_impl():
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Insert compression event
                compression_ratio = compressed_size / original_size if original_size > 0 else 1
                # CRITICAL: 'uuid' column stores user_id in this codebase!
                cur.execute("""
                    INSERT INTO compression_events 
                    (uuid, original_size, compressed_size, compression_ratio, compression_count, model_used)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    user_id,  # Goes into 'uuid' column per debug_disaster.md
                    original_size,
                    compressed_size,
                    compression_ratio,
                    compression_count,
                    get_compression_model()
                ))
                conn.commit()
    
    try:
        execute_db_operation(_track_impl)
    except Exception as e:
        print(f"⚠️ Failed to track compression event: {e}")

def get_compression_stats(user_id: str) -> Dict[str, Any]:
    """Get compression statistics for a user"""
    def _get_stats():
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Get compression stats
                cur.execute("""
                    SELECT 
                        COUNT(*) as total_compressions,
                        AVG(compression_ratio) as avg_compression_ratio,
                        SUM(original_size - compressed_size) as total_chars_saved,
                        MAX(compression_count) as max_compression_count,
                        MAX(created_at) as last_compression
                    FROM compression_events
                    WHERE user_id = %s
                """, (user_id,))
                
                row = cur.fetchone()
                if row:
                    return {
                        'total_compressions': row[0] or 0,
                        'avg_compression_ratio': float(row[1]) if row[1] else 0,
                        'total_chars_saved': row[2] or 0,
                        'max_compression_count': row[3] or 0,
                        'last_compression': row[4].isoformat() if row[4] else None
                    }
                return {}
    
    try:
        return execute_db_operation(_get_stats) or {}
    except Exception as e:
        print(f"⚠️ Error getting compression stats: {e}")
        return {}

def get_persistent_memory_size(user_id: str) -> int:
    """Get the current size of persistent memory for a user"""
    summary = get_summary(user_id)
    return len(summary) if summary else 0