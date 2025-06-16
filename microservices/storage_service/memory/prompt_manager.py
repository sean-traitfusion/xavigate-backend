# memory/prompt_manager.py
"""
Prompt size management to ensure final prompts stay within limits
Based on Mobeus architecture
"""
from config import runtime_config
from typing import Dict, Any, Tuple, Optional

def get_max_prompt_chars() -> int:
    """Get maximum allowed characters for the final prompt"""
    return runtime_config.get("MAX_PROMPT_CHARS", 20000)

def get_rag_context_limit() -> int:
    """Get character limit reserved for RAG context"""
    return runtime_config.get("RAG_CONTEXT_CHAR_LIMIT", 4000)

def calculate_prompt_components(
    base_prompt: str,
    persistent_memory: str,
    session_memory: str,
    rag_context: str = ""
) -> Dict[str, Any]:
    """
    Calculate the size of each prompt component and total
    
    Returns:
        Dict with component sizes and whether we're within limits
    """
    components = {
        "base_prompt": len(base_prompt),
        "persistent_memory": len(persistent_memory),
        "session_memory": len(session_memory),
        "rag_context": len(rag_context),
        "total": len(base_prompt) + len(persistent_memory) + len(session_memory) + len(rag_context),
        "max_allowed": get_max_prompt_chars(),
        "within_limits": True
    }
    
    components["within_limits"] = components["total"] <= components["max_allowed"]
    components["overhead"] = components["total"] - components["max_allowed"] if not components["within_limits"] else 0
    
    return components

def optimize_prompt_size(
    base_prompt: str,
    persistent_memory: str,
    session_memory_lines: list,
    rag_context: str = ""
) -> Tuple[str, Dict[str, Any]]:
    """
    Optimize prompt size by trimming session memory if needed
    
    Args:
        base_prompt: The system prompt
        persistent_memory: User's persistent memory summary
        session_memory_lines: List of session memory lines (newest first)
        rag_context: RAG retrieval context
        
    Returns:
        Tuple of (optimized_prompt, metrics)
    """
    max_chars = get_max_prompt_chars()
    rag_limit = get_rag_context_limit()
    
    # Calculate fixed components size
    fixed_size = len(base_prompt) + len(persistent_memory) + len(rag_context)
    
    # If RAG context is too large, truncate it
    if len(rag_context) > rag_limit:
        rag_context = rag_context[:rag_limit] + "\n... [RAG context truncated]"
        fixed_size = len(base_prompt) + len(persistent_memory) + len(rag_context)
    
    # Calculate available space for session memory
    available_for_session = max_chars - fixed_size - 500  # 500 char buffer
    
    # Build session memory within limits
    session_memory_text = ""
    included_lines = 0
    
    for line in session_memory_lines:
        if len(session_memory_text) + len(line) + 1 <= available_for_session:
            session_memory_text = line + "\n" + session_memory_text  # Prepend to maintain order
            included_lines += 1
        else:
            break
    
    # Build final prompt
    context_parts = []
    
    if persistent_memory:
        context_parts.append(f"User Background:\n{persistent_memory}")
    
    if session_memory_text:
        context_parts.append(f"Recent Conversation:\n{session_memory_text}")
    
    if rag_context:
        context_parts.append(f"Relevant Context:\n{rag_context}")
    
    if context_parts:
        # Join with double newlines to separate sections clearly
        final_prompt = base_prompt + f"\n\nContext about this user:\n\n" + "\n\n".join(context_parts)
    else:
        final_prompt = base_prompt
    
    # Calculate metrics
    metrics = {
        "total_chars": len(final_prompt),
        "base_prompt_chars": len(base_prompt),
        "persistent_memory_chars": len(persistent_memory),
        "session_memory_chars": len(session_memory_text),
        "rag_context_chars": len(rag_context),
        "session_lines_included": included_lines,
        "session_lines_total": len(session_memory_lines),
        "within_limits": len(final_prompt) <= max_chars,
        "utilization_percent": (len(final_prompt) / max_chars) * 100
    }
    
    return final_prompt, metrics

def estimate_tokens(text: str) -> int:
    """
    Estimate token count from character count
    Rough approximation: 1 token ≈ 4 characters
    """
    return len(text) // 4

def log_prompt_metrics(user_id: str, session_id: str, metrics: Dict[str, Any]):
    """Log prompt size metrics for monitoring"""
    try:
        import json
        from datetime import datetime
        import os
        
        log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        log_path = os.path.join(log_dir, "prompt_metrics.jsonl")
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "session_id": session_id,
            **metrics,
            "estimated_tokens": estimate_tokens(str(metrics.get("total_chars", 0)))
        }
        
        with open(log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
            
    except Exception as e:
        print(f"⚠️ Failed to log prompt metrics: {e}")

def should_trigger_compression(
    persistent_memory_size: int,
    session_memory_size: int
) -> Tuple[bool, str]:
    """
    Determine if we should trigger memory compression
    
    Returns:
        Tuple of (should_compress, reason)
    """
    max_prompt = get_max_prompt_chars()
    
    # Reserve space for base prompt (~2000) and RAG context (~4000)
    reserved_space = 6000
    available_for_memory = max_prompt - reserved_space
    
    total_memory = persistent_memory_size + session_memory_size
    
    if total_memory > available_for_memory:
        if persistent_memory_size > (available_for_memory * 0.5):
            return True, "persistent_memory_too_large"
        elif session_memory_size > (available_for_memory * 0.7):
            return True, "session_memory_too_large"
    
    return False, ""