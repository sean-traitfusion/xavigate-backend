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
    try:
        current_summary = get_summary(user_id)
        if not current_summary:
            print(f"⚠️ No persistent memory to compress for {user_id}")
            return False
        
        original_size = len(current_summary)
        print(f"📝 COMPRESSING PERSISTENT MEMORY for {user_id}: {original_size} chars (compression #{current_compression_count + 1})")
        
        # Generate compressed summary using OpenAI
        compressed_summary, metadata = generate_compressed_summary(
            current_summary, 
            current_compression_count
        )
        
        if compressed_summary:
            # Clear existing summary
            clear_summary(user_id)
            
            # Add compression marker with count
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            compression_marker = f"[COMPRESSED {current_compression_count + 1}x as of {timestamp}]"
            if current_compression_count == 0:
                compression_marker = f"[COMPRESSED SUMMARY as of {timestamp}]"
            
            compressed_with_marker = f"{compression_marker}\n\n{compressed_summary}"
            
            # Store compressed summary
            _store_compressed_summary(user_id, compressed_with_marker)
            
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
        else:
            print(f"⚠️ Failed to generate compressed summary for {user_id}")
            return False
            
    except Exception as e:
        print(f"❌ Error compressing persistent memory for {user_id}: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_compressed_summary(current_summary: str, compression_count: int = 0) -> Tuple[Optional[str], Dict[str, Any]]:
    """
    Generate a compressed summary of the persistent memory using OpenAI
    
    Returns:
        Tuple of (compressed_summary, metadata)
    """
    try:
        import openai
        
        # Get configuration
        model = get_compression_model()
        temperature = runtime_config.get("SUMMARY_TEMPERATURE", 0.3)
        compression_ratio = get_compression_ratio()
        
        # Get compression prompt
        prompt_template = runtime_config.get("PERSISTENT_MEMORY_COMPRESSION_PROMPT")
        prompt = prompt_template.format(
            current_summary=current_summary,
            compression_ratio=int((1 - compression_ratio) * 100)
        )
        
        # Track timing
        start_time = datetime.now()
        
        response = openai.ChatCompletion.create(
            model=model,
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
        
        end_time = datetime.now()
        duration_ms = (end_time - start_time).total_seconds() * 1000
        
        compressed = response.choices[0].message.content.strip()
        
        # Collect metadata
        metadata = {
            "model": model,
            "temperature": temperature,
            "compression_ratio_target": compression_ratio,
            "compression_count": compression_count,
            "duration_ms": duration_ms,
            "prompt_tokens": response.usage.prompt_tokens if hasattr(response, 'usage') else 0,
            "completion_tokens": response.usage.completion_tokens if hasattr(response, 'usage') else 0,
            "total_tokens": response.usage.total_tokens if hasattr(response, 'usage') else 0
        }
        
        return compressed, metadata
        
    except Exception as e:
        print(f"❌ Error generating compressed summary: {e}")
        return None, {}

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
                cur.execute("""
                    INSERT INTO compression_events 
                    (user_id, original_size, compressed_size, compression_ratio, compression_count, model_used)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    user_id,
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