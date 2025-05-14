# backend/memory/routes.py
from fastapi import APIRouter, HTTPException, Header, Response, Body, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime, timedelta
from uuid import UUID
import os
import json

from dotenv import load_dotenv
# Load root and service .env for unified configuration
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)
service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(dotenv_path=service_env, override=True)
ENV = os.getenv("ENV", "dev")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8014")
import requests
from memory.consolidate_session import synthesize_persistent_update
# OpenAI client for session summarization
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

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
print("✅ memory_routes.py loaded")
print("🌍 ENV =", os.getenv("ENV"))

import psycopg2
from db_service.db import get_connection
## In-memory store for dev mode
DEV_SESSION_STORE: dict[str, list[dict]] = {}
DEV_SUMMARIES: dict[str, dict] = {}
if ENV != "dev":
    # Initialize Postgres connection and cursor
    conn = get_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    ## === SCHEMA CREATION ===
    # Drop existing tables and create schema
    cursor.execute("DROP TABLE IF EXISTS memory_summary;")
    cursor.execute("DROP TABLE IF EXISTS session_memory;")
    cursor.execute("DROP TABLE IF EXISTS user_memory;")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS session_memory (
        uuid TEXT PRIMARY KEY,
        session_start TIMESTAMP DEFAULT NOW(),
        last_active TIMESTAMP,
        conversation_log JSONB,
        interim_scores JSONB,
        expires_at TIMESTAMP
    );
    """")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_memory (
        uuid TEXT PRIMARY KEY,
        initial_personality_scores JSONB,
        score_explanations JSONB,
        trait_history JSONB,
        preferences JSONB,
        created_at TIMESTAMP DEFAULT NOW(),
        last_updated TIMESTAMP DEFAULT NOW()
    );
    """")

    # === SESSION SUMMARY TABLE ===
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory_summary (
        summary_id SERIAL PRIMARY KEY,
        uuid TEXT NOT NULL,
        summary_text TEXT,
        full_transcript JSONB,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """")


# === MODELS ===

class SessionMemory(BaseModel):
    # session identifier from frontend (string)
    uuid: str
    session_start: datetime = Field(default_factory=datetime.utcnow)
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


# === ROUTES ===

# Route to support frontend (adds compatibility)
@router.post("/session-memory")
def upsert_session(mem: SessionMemory):
    upsert_session_direct(mem)
    return {"status": "session memory updated"}

def upsert_session_direct(mem: SessionMemory):
    now = datetime.utcnow()
    # Set session expiration based on timeout (minutes)
    timeout_min = int(os.getenv("SESSION_TIMEOUT_MINUTES", "120"))
    expires_at = now + timedelta(minutes=timeout_min)

    if not mem.conversation_log:
        print("⚠️ No conversation log to store — skipping upsert.")
        return

    # Use JSONB merge to preserve existing summary fields when updating partial conversation logs
    cursor.execute("""
        INSERT INTO session_memory (uuid, session_start, last_active, conversation_log, interim_scores, expires_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (uuid) DO UPDATE SET
            last_active = EXCLUDED.last_active,
            -- Merge existing conversation_log with new data, so partial updates (e.g., messages only) don't overwrite summaries
            conversation_log = session_memory.conversation_log || EXCLUDED.conversation_log,
            interim_scores = EXCLUDED.interim_scores,
            expires_at = EXCLUDED.expires_at;
    """, (
        str(mem.uuid),
        now,
        now,
        json.dumps(mem.conversation_log, default=str),
        json.dumps(mem.interim_scores or {}, default=str),
        expires_at
    ))


@router.get("/session-memory/{uuid}")
def get_session(uuid: str):
    # Dev mode: return in-memory store
    if os.getenv("ENV", "dev") == "dev":
        return {"exchanges": DEV_SESSION_STORE.get(uuid, [])}
    cursor.execute("SELECT conversation_log FROM session_memory WHERE uuid = %s", (uuid,))
    result = cursor.fetchone()
    if not result:
        return {}
    return result[0]


@router.post("/persistent-memory")
def upsert_user(mem: UserMemory):
    now = datetime.utcnow()
    cursor.execute("""
        INSERT INTO user_memory (uuid, initial_personality_scores, score_explanations, trait_history, preferences, created_at, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (uuid) DO UPDATE SET
            initial_personality_scores = EXCLUDED.initial_personality_scores,
            score_explanations = EXCLUDED.score_explanations,
            trait_history = EXCLUDED.trait_history,
            preferences = EXCLUDED.preferences,
            last_updated = EXCLUDED.last_updated;
    """, (
        str(mem.uuid),
        json.dumps(mem.initial_personality_scores, default=str),
        json.dumps(mem.score_explanations, default=str),
        json.dumps(mem.trait_history, default=str),
        json.dumps(mem.preferences, default=str),
        now,
        now
    ))

    return {"status": "persistent memory updated"}


@router.get("/persistent-memory/{uuid}")
def get_user(uuid: str):

    cursor.execute("SELECT * FROM user_memory WHERE uuid = %s", (uuid,))
    result = cursor.fetchone()
    if not result:
        # No persistent memory yet; return empty object
        return {}
    # Return stored user memory
    return {
        "uuid": result[0],
        "initial_personality_scores": result[1],
        "score_explanations": result[2],
        "trait_history": result[3],
        "preferences": result[4],
        "created_at": result[5],
        "last_updated": result[6]
    }

@router.get("/review/{uuid}")
def get_session_review(uuid: str):

    # Real DB read logic
    cursor.execute("SELECT conversation_log FROM session_memory WHERE uuid = %s", (uuid,))
    session_result = cursor.fetchone()

    cursor.execute("SELECT * FROM user_memory WHERE uuid = %s", (uuid,))
    user_result = cursor.fetchone()

    if not session_result and not user_result:
        # No memory found; return empty review structure
        return {"conversation_log": {}, "persistent_memory": {}}

    # Map tuple indices to keys for persistent memory
    return {
        "conversation_log": session_result[0] if session_result else {},
        "persistent_memory": {
            "uuid": user_result[0],
            "initial_personality_scores": user_result[1],
            "score_explanations": user_result[2],
            "trait_history": user_result[3],
            "preferences": user_result[4],
            "created_at": user_result[5],
            "last_updated": user_result[6],
        } if user_result else {}
    }

# Internal expiration logic: summarize, persist, then delete session
def expire_session_logic(user_uuid: str):
    # Fetch active session memory
    cursor.execute("SELECT conversation_log FROM session_memory WHERE uuid = %s", (user_uuid,))
    rec = cursor.fetchone()
    if not rec or not rec[0]:
        return
    conv_log = rec[0]
    # Build transcript text
    exchanges = conv_log.get("exchanges", []) if isinstance(conv_log, dict) else []
    transcript = ""
    for ex in exchanges:
        transcript += f"User: {ex.get('user_prompt','')}\nAssistant: {ex.get('assistant_response','')}\n"
    # Generate summary via OpenAI
    summary_prompt = f"Summarize the following conversation in 1-2 sentences:\n\n{transcript}"
    try:
        comp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": summary_prompt}],
            temperature=0.3,
        )
        summary = comp.choices[0].message.content.strip()
    except Exception:
        summary = "Summary unavailable."
    # Persist user memory updates via consolidate_session
    try:
        from memory.consolidate_session import synthesize_persistent_update
        persistent_update = synthesize_persistent_update(UUID(user_uuid), plan={}, critique="")
        # Upsert into user_memory
        upsert_user(persistent_update, authorization="")
    except Exception as e:
        print(f"❌ Persistence update failed: {e}")
    # Store session summary and full transcript
    cursor.execute(
        "INSERT INTO memory_summary (uuid, summary_text, full_transcript) VALUES (%s, %s, %s)",
        (user_uuid, summary, json.dumps(conv_log, default=str))
    )
    # Delete active session memory
    cursor.execute("DELETE FROM session_memory WHERE uuid = %s", (user_uuid,))
    print(f"✅ Expired session {user_uuid} and stored summary.")
    
## Endpoint to expire and summarize a session (cron/internal use)
class ExpireRequest(BaseModel):
    uuid: str

@router.post("/expire", status_code=204, tags=["memory"])
def expire_session(payload: ExpireRequest):
    # Dev mode: in-memory expire and summarize
    if ENV == "dev":
        # Remove session exchanges and store a simple in-memory summary
        exchanges = DEV_SESSION_STORE.pop(payload.uuid, [])
        from datetime import datetime
        DEV_SUMMARIES[payload.uuid] = {
            "summary_text": "",  # no real summary in dev
            "full_transcript": {"exchanges": exchanges},
            "created_at": datetime.utcnow().isoformat(),
        }
        return Response(status_code=204)
    # Production: full expiration logic (DB, OpenAI, persistence)
    expire_session_logic(payload.uuid)
    return Response(status_code=204)
    
# Frontend compatibility: alias endpoints for memory saving and retrieval
class MemorySaveRequest(BaseModel):
    userId: str
    # session identifier (string)
    sessionId: str
    messages: List[Dict[str, str]]

@router.post("/save", status_code=204, tags=["memory"])
def save_memory(req: MemorySaveRequest):
    # Dev mode: store in memory
    if os.getenv("ENV", "dev") == "dev":
        DEV_SESSION_STORE.setdefault(req.sessionId, [])
        # req.messages is [user, assistant, user, assistant, ...]
        for msg in req.messages:
            role = msg.get("role")
            content = msg.get("content")
            DEV_SESSION_STORE[req.sessionId].append({"role": role, "content": content})
        return Response(status_code=204)
    # Production: Persist to Postgres
    cursor.execute("SELECT conversation_log FROM session_memory WHERE uuid = %s", (str(req.sessionId),))
    result = cursor.fetchone()
    existing = result[0] if result and result[0] else {}
    exchanges = existing.get("exchanges", []) if isinstance(existing, dict) else []
    for entry in req.messages:
        if entry.get("role") and entry.get("content"):
            if entry["role"] == "user":
                exchanges.append({"user_prompt": entry["content"]})
            else:
                exchanges[-1]["assistant_response"] = entry["content"]
    upsert_session_direct(SessionMemory(uuid=req.sessionId, conversation_log={"exchanges": exchanges}))
    return Response(status_code=204)

@router.get("/get/{uuid}", tags=["memory"])
def get_memory(uuid: str):
    # Dev mode: return in-memory flat list
    if os.getenv("ENV", "dev") == "dev":
        return DEV_SESSION_STORE.get(uuid, [])
    cursor.execute("SELECT conversation_log FROM session_memory WHERE uuid = %s", (uuid,))
    result = cursor.fetchone()
    conv_log = result[0] if result and result[0] else {}
    messages = []
    if isinstance(conv_log, dict) and "exchanges" in conv_log:
        for ex in conv_log["exchanges"]:
            messages.append({"role": "user", "content": ex.get("user_prompt", "")})
            messages.append({"role": "assistant", "content": ex.get("assistant_response", "")})
    elif isinstance(conv_log, list):
        messages = conv_log
    return messages
    
@router.get("/summary/{uuid}", tags=["memory"])
def get_summary(uuid: str):
    # Dev mode: return in-memory summary
    if os.getenv("ENV", "dev") == "dev":
        return DEV_SUMMARIES.get(uuid, {})
    cursor.execute(
        "SELECT summary_text, full_transcript, created_at FROM memory_summary WHERE uuid = %s ORDER BY summary_id DESC LIMIT 1",
        (uuid,)
    )
    rec = cursor.fetchone()
    if not rec:
        return {}
    return {
        "summary_text": rec[0],
        "full_transcript": rec[1],
        "created_at": rec[2]
    }