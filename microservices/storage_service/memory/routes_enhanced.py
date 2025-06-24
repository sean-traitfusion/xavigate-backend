# backend/memory/routes_enhanced.py
"""
Enhanced memory routes with auto-summarization and compression
Compatible with existing endpoints while adding new capabilities
"""
from fastapi import APIRouter, HTTPException, Header, Response, Body, Depends, Request
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime, timezone
import os
import json
import requests

from memory.models import RuntimeConfig
from memory.client import MemoryClient
from memory.prompt_manager import optimize_prompt_size, log_prompt_metrics
from memory.db import initialize_memory_tables, get_connection
from config import runtime_config

from dotenv import load_dotenv
# Load root and service .env for unified configuration
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)
service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=service_env, override=True)

ENV = os.getenv("ENV", "dev")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8014")

# Initialize memory client
memory_client = MemoryClient()

# Initialize memory tables on startup
if ENV != "dev":
    try:
        initialize_memory_tables()
    except Exception as e:
        print(f"⚠️ Failed to initialize memory tables: {e}")

## JWT authentication dependency (shared)
def require_jwt(authorization: str | None = Header(None, alias="Authorization")):
    # In dev mode, skip authentication entirely
    if ENV == "dev":
        return
    # In prod, require Bearer token
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized or missing token")
    token = authorization.split(" ", 1)[1]
    resp = requests.post(f"{AUTH_SERVICE_URL}/verify", json={"key": token})
    if resp.status_code != 200 or not resp.json().get("valid", False):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

router = APIRouter(dependencies=[Depends(require_jwt)])

print("✅ Enhanced memory routes loaded")
print("🌍 ENV =", ENV)

## In-memory store for dev mode
DEV_SESSION_STORE: dict[str, list[dict]] = {}
DEV_SUMMARIES: dict[str, dict] = {}

# === MODELS ===

class SessionMemory(BaseModel):
    # session identifier from frontend (string)
    uuid: str
    session_start: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_active: Optional[datetime] = None
    conversation_log: Dict[str, Any]
    interim_scores: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None

class UserMemory(BaseModel):
    uuid: UUID
    initial_personality_scores: Optional[dict] = None
    score_explanations: Optional[dict] = None
    trait_history: Optional[dict] = None
    preferences: Optional[dict] = None

class MemorySaveRequest(BaseModel):
    userId: str
    sessionId: str
    messages: List[Dict[str, str]]

class ExpireRequest(BaseModel):
    uuid: str

# === ROUTES ===

# Frontend compatibility: save memory with enhanced features
@router.post("/save", status_code=204, tags=["memory"])
def save_memory(req: MemorySaveRequest):
    """Enhanced save with auto-summarization and voice command detection"""
    # Dev mode: store in memory
    if ENV == "dev":
        DEV_SESSION_STORE.setdefault(req.sessionId, [])
        for msg in req.messages:
            role = msg.get("role")
            content = msg.get("content")
            DEV_SESSION_STORE[req.sessionId].append({"role": role, "content": content})
        return Response(status_code=204)
    
    # Production: Use enhanced memory system
    for entry in req.messages:
        if entry.get("role") and entry.get("content"):
            role = entry["role"]
            content = entry["content"]
            
            # Log interaction
            memory_client.log_interaction(req.userId, req.sessionId, role, content)
    
    return Response(status_code=204)

@router.get("/get/{uuid}", tags=["memory"])
def get_memory(uuid: str):
    """Get session memory with enhanced format"""
    if ENV == "dev":
        return DEV_SESSION_STORE.get(uuid, [])
    
    # Use memory client to get session
    session_data = memory_client.get_session(uuid)
    
    # Convert to expected format
    messages = []
    for entry in session_data:
        messages.append({
            "role": entry.get("role", ""),
            "content": entry.get("message", "")
        })
    
    return messages

@router.get("/session-memory/{uuid}")
def get_session(uuid: str):
    """Get session memory in original format for compatibility"""
    if ENV == "dev":
        return {"exchanges": DEV_SESSION_STORE.get(uuid, [])}
    
    # Use memory client to get session
    session_data = memory_client.get_session(uuid)
    
    # Convert to exchanges format
    exchanges = []
    current_exchange = {}
    
    for entry in session_data:
        if entry["role"] == "user":
            if current_exchange:
                exchanges.append(current_exchange)
            current_exchange = {"user_prompt": entry["message"]}
        elif entry["role"] == "assistant" and current_exchange:
            current_exchange["assistant_response"] = entry["message"]
            exchanges.append(current_exchange)
            current_exchange = {}
    
    if current_exchange:
        exchanges.append(current_exchange)
    
    return {"exchanges": exchanges}

@router.post("/session-memory")
def upsert_session(mem: SessionMemory):
    """Legacy endpoint - redirect to new system"""
    if ENV == "dev":
        DEV_SESSION_STORE[mem.uuid] = mem.conversation_log.get("exchanges", [])
        return {"status": "session memory updated"}
    
    # Convert to new format and use memory client
    exchanges = mem.conversation_log.get("exchanges", [])
    session_id = mem.conversation_log.get("session_id", mem.uuid)  # Use uuid as session_id if not provided
    user_id = mem.conversation_log.get("user_id", "unknown")  # Get user_id from conversation_log
    
    for exchange in exchanges:
        if "user_prompt" in exchange:
            memory_client.log_interaction(user_id, session_id, "user", exchange["user_prompt"])
        if "assistant_response" in exchange:
            memory_client.log_interaction(user_id, session_id, "assistant", exchange["assistant_response"])
    
    return {"status": "session memory updated"}

@router.get("/persistent-memory/{uuid}")
def get_user(uuid: str):
    """Get persistent memory (user summary)"""
    summary = memory_client.get_summary(uuid)
    
    if not summary:
        return {}
    
    # Return in expected format
    return {
        "uuid": uuid,
        "summary": summary,
        "initial_personality_scores": {},
        "score_explanations": {},
        "trait_history": {},
        "preferences": {}
    }

@router.post("/persistent-memory")
def upsert_user(mem: UserMemory):
    """Update persistent memory"""
    # Extract any relevant info and append to summary
    summary_parts = []
    
    if mem.initial_personality_scores:
        summary_parts.append(f"Personality scores: {json.dumps(mem.initial_personality_scores)}")
    
    if mem.trait_history:
        summary_parts.append(f"Trait history: {json.dumps(mem.trait_history)}")
    
    if mem.preferences:
        summary_parts.append(f"Preferences: {json.dumps(mem.preferences)}")
    
    if summary_parts:
        memory_client.append_summary(str(mem.uuid), "\n".join(summary_parts))
    
    return {"status": "persistent memory updated"}

@router.get("/summary/{uuid}", tags=["memory"])
def get_summary(uuid: str):
    """Get conversation summaries"""
    if ENV == "dev":
        return DEV_SUMMARIES.get(uuid, {})
    
    summary = memory_client.get_summary(uuid)
    
    if not summary:
        return {}
    
    return {
        "summary_text": summary,
        "full_transcript": {},
        "created_at": datetime.now(timezone.utc).isoformat()
    }

@router.get("/all-summaries/{uuid}")
def get_all_summaries(uuid: str):
    """Get all summaries for a user"""
    summary = memory_client.get_summary(uuid)
    
    if not summary:
        return {"summaries": []}
    
    # Split by timestamp markers
    summaries = []
    lines = summary.split('\n')
    
    for line in lines:
        if line.strip() and line.startswith('[') and ']' in line:
            # Extract just the summary text
            summary_text = line.split(']', 1)[1].strip() if ']' in line else line
            if summary_text:
                summaries.append(summary_text)
    
    return {"summaries": summaries}

@router.post("/expire", status_code=204, tags=["memory"])
def expire_session(payload: ExpireRequest):
    """Force session expiration and summarization"""
    if ENV == "dev":
        exchanges = DEV_SESSION_STORE.pop(payload.uuid, [])
        DEV_SUMMARIES[payload.uuid] = {
            "summary_text": "Dev mode summary",
            "full_transcript": {"exchanges": exchanges},
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        return Response(status_code=204)
    
    # Use memory client to force summarization
    # Using uuid as both user_id and session_id for legacy compatibility
    memory_client.force_session_summary(payload.uuid, payload.uuid, "manual_expiration")
    return Response(status_code=204)

@router.get("/review/{uuid}")
def get_session_review(uuid: str):
    """Get complete memory review"""
    session_data = memory_client.get_session(uuid)
    persistent_summary = memory_client.get_summary(uuid)
    
    # Convert session to exchanges format
    exchanges = []
    current_exchange = {}
    
    for entry in session_data:
        if entry["role"] == "user":
            if current_exchange:
                exchanges.append(current_exchange)
            current_exchange = {"user_prompt": entry["message"]}
        elif entry["role"] == "assistant" and current_exchange:
            current_exchange["assistant_response"] = entry["message"]
            exchanges.append(current_exchange)
            current_exchange = {}
    
    if current_exchange:
        exchanges.append(current_exchange)
    
    return {
        "conversation_log": {"exchanges": exchanges},
        "persistent_memory": {
            "uuid": uuid,
            "summary": persistent_summary,
            "initial_personality_scores": {},
            "score_explanations": {},
            "trait_history": {},
            "preferences": {},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_updated": datetime.now(timezone.utc).isoformat()
        } if persistent_summary else {}
    }

# Runtime configuration endpoints
@router.get("/runtime-config")
def get_runtime_config():
    """Get runtime configuration - returns all stored config values"""
    # Get all config values from runtime_config
    config_dict = {}
    
    # Chat settings
    config_dict["system_prompt"] = runtime_config.get("SYSTEM_PROMPT", "Hi, I'm Xavigate...")
    config_dict["conversation_history_limit"] = runtime_config.get("CONVERSATION_HISTORY_LIMIT", 3)
    config_dict["top_k_rag_hits"] = runtime_config.get("TOP_K_RAG_HITS", 4)
    config_dict["prompt_style"] = runtime_config.get("PROMPT_STYLE", "default")
    config_dict["custom_style_modifier"] = runtime_config.get("CUSTOM_STYLE_MODIFIER", None)
    config_dict["temperature"] = runtime_config.get("TEMPERATURE", 0.7)
    config_dict["max_tokens"] = runtime_config.get("MAX_TOKENS", 1000)
    config_dict["presence_penalty"] = runtime_config.get("PRESENCE_PENALTY", 0.1)
    config_dict["frequency_penalty"] = runtime_config.get("FREQUENCY_PENALTY", 0.1)
    config_dict["model"] = runtime_config.get("MODEL", "gpt-3.5-turbo")
    
    # Memory settings
    config_dict["SESSION_MEMORY_CHAR_LIMIT"] = runtime_config.get("SESSION_MEMORY_CHAR_LIMIT", 15000)
    config_dict["PERSISTENT_MEMORY_CHAR_LIMIT"] = runtime_config.get("PERSISTENT_MEMORY_CHAR_LIMIT", 8000)
    config_dict["MAX_PROMPT_CHARS"] = runtime_config.get("MAX_PROMPT_CHARS", 20000)
    config_dict["RAG_CONTEXT_CHAR_LIMIT"] = runtime_config.get("RAG_CONTEXT_CHAR_LIMIT", 4000)
    
    # Compression settings
    config_dict["PERSISTENT_MEMORY_COMPRESSION_RATIO"] = runtime_config.get("PERSISTENT_MEMORY_COMPRESSION_RATIO", 0.6)
    config_dict["PERSISTENT_MEMORY_COMPRESSION_MODEL"] = runtime_config.get("PERSISTENT_MEMORY_COMPRESSION_MODEL", "gpt-4")
    config_dict["PERSISTENT_MEMORY_MIN_SIZE"] = runtime_config.get("PERSISTENT_MEMORY_MIN_SIZE", 1000)
    
    # Summary settings
    config_dict["SUMMARY_TEMPERATURE"] = runtime_config.get("SUMMARY_TEMPERATURE", 0.3)
    
    # Feature flags
    config_dict["AUTO_SUMMARY_ENABLED"] = runtime_config.get("AUTO_SUMMARY_ENABLED", True)
    config_dict["AUTO_COMPRESSION_ENABLED"] = runtime_config.get("AUTO_COMPRESSION_ENABLED", True)
    
    # Prompts
    config_dict["SESSION_SUMMARY_PROMPT"] = runtime_config.get("SESSION_SUMMARY_PROMPT", "")
    config_dict["PERSISTENT_MEMORY_COMPRESSION_PROMPT"] = runtime_config.get("PERSISTENT_MEMORY_COMPRESSION_PROMPT", "")
    
    return config_dict

@router.post("/runtime-config")
def update_runtime_config(cfg: Dict[str, Any], request: Request = None):
    """Update runtime configuration - accepts any configuration fields"""
    # Update all provided configuration values
    for key, value in cfg.items():
        if value is not None:  # Only update non-None values
            runtime_config.set_config(key, value)
    
    # For backwards compatibility, also set uppercase versions of lowercase keys
    key_mappings = {
        "system_prompt": "SYSTEM_PROMPT",
        "conversation_history_limit": "CONVERSATION_HISTORY_LIMIT",
        "top_k_rag_hits": "TOP_K_RAG_HITS",
        "prompt_style": "PROMPT_STYLE",
        "custom_style_modifier": "CUSTOM_STYLE_MODIFIER",
        "temperature": "TEMPERATURE",
        "max_tokens": "MAX_TOKENS",
        "presence_penalty": "PRESENCE_PENALTY",
        "frequency_penalty": "FREQUENCY_PENALTY",
        "model": "MODEL"
    }
    
    for lower_key, upper_key in key_mappings.items():
        if lower_key in cfg and cfg[lower_key] is not None:
            runtime_config.set_config(upper_key, cfg[lower_key])
    
    # Save to database for persistence
    try:
        from config.config_persistence import save_config_to_db
        # Try to get user info from request if available
        user_id = None
        if request and hasattr(request, 'state') and hasattr(request.state, 'user'):
            user_id = request.state.user.get('email', 'unknown')
        save_config_to_db(user_id)
    except Exception as e:
        print(f"Warning: Could not persist config to database: {e}")
    
    return {"status": "ok"}

# Memory stats endpoint (new)
@router.get("/memory-stats/{uuid}")
def get_memory_stats(uuid: str):
    """Get memory usage statistics"""
    from memory.session_memory import get_memory_stats as get_session_stats
    from memory.persistent_compression import get_compression_stats
    
    # Using uuid as both user_id and session_id for legacy compatibility
    session_stats = get_session_stats(uuid, uuid)
    compression_stats = get_compression_stats(uuid)
    
    return {
        "session": session_stats,
        "compression": compression_stats,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Prompt optimization endpoint (new)
@router.post("/optimize-prompt")
def optimize_prompt(request: Dict[str, Any]):
    """Optimize prompt for size constraints"""
    base_prompt = request.get("base_prompt", "")
    uuid = request.get("uuid", "")
    rag_context = request.get("rag_context", "")
    
    # Get memories
    # Using uuid as user_id for persistent memory
    persistent_memory = memory_client.get_summary(uuid) or ""
    # Using uuid as session_id for session memory
    session_data = memory_client.get_session(uuid)
    
    # Convert session to lines
    session_lines = []
    for entry in reversed(session_data):  # Newest first
        line = f"{entry['role'].title()}: {entry['message']}"
        session_lines.append(line)
    
    # Optimize
    final_prompt, metrics = optimize_prompt_size(
        base_prompt=base_prompt,
        persistent_memory=persistent_memory,
        session_memory_lines=session_lines,
        rag_context=rag_context
    )
    
    # Log metrics
    # Using uuid as both user_id and session_id for legacy compatibility
    log_prompt_metrics(uuid, uuid, metrics)
    
    return {
        "final_prompt": final_prompt,
        "metrics": metrics
    }

# Configuration backup endpoints
@router.post("/config-backup")
def create_config_backup(request: Dict[str, Any]):
    """Create a backup of the current configuration"""
    try:
        from config.config_persistence import create_config_backup
        
        backup_name = request.get("backup_name", f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        description = request.get("description", "Manual backup")
        user_id = request.get("user_id", "unknown")
        
        create_config_backup(backup_name, description, user_id)
        
        return {
            "status": "ok",
            "backup_name": backup_name,
            "message": "Configuration backup created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/config-backups")
def list_config_backups():
    """List all available configuration backups"""
    try:
        from config.config_persistence import list_config_backups
        
        backups = list_config_backups()
        return {
            "status": "ok",
            "backups": backups
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config-restore")
def restore_config_backup(request: Dict[str, Any]):
    """Restore configuration from a backup"""
    try:
        from config.config_persistence import restore_config_backup
        
        backup_name = request.get("backup_name")
        if not backup_name:
            raise ValueError("backup_name is required")
        
        user_id = request.get("user_id", "unknown")
        
        restore_config_backup(backup_name, user_id)
        
        return {
            "status": "ok",
            "message": f"Configuration restored from backup '{backup_name}'"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config-reset-defaults")
def reset_to_defaults(request: Dict[str, Any] = None):
    """Reset configuration to original system defaults"""
    try:
        from config.config_persistence import restore_config_backup
        
        user_id = request.get("user_id", "unknown") if request else "unknown"
        
        # Restore from the original defaults backup
        restore_config_backup("original_defaults", user_id)
        
        return {
            "status": "ok",
            "message": "Configuration reset to system defaults"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))