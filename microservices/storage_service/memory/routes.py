# backend/memory/routes.py
from fastapi import APIRouter, HTTPException, Header, Response, Body, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime, timedelta
from uuid import UUID
import os
import json
from memory.models import RuntimeConfig


from dotenv import load_dotenv
# Load root and service .env for unified configuration
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)
service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
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
print("🌍 ENV =", ENV)

import psycopg2
from shared.db import get_connection
## In-memory store for dev mode
DEV_SESSION_STORE: dict[str, list[dict]] = {}
DEV_SUMMARIES: dict[str, dict] = {}
if ENV != "dev":
    # Initialize Postgres connection and cursor
    conn = get_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    # Create tables if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS session_memory (
        uuid TEXT PRIMARY KEY,
        session_start TIMESTAMP DEFAULT NOW(),
        last_active TIMESTAMP,
        conversation_log JSONB,
        interim_scores JSONB,
        expires_at TIMESTAMP
    );
    """)
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
    """)
    # Runtime configuration table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS runtime_config (
        id SERIAL PRIMARY KEY,
        system_prompt TEXT NOT NULL,
        conversation_history_limit INT DEFAULT 3,
        top_k_rag_hits INT DEFAULT 4,
        updated_at TIMESTAMP DEFAULT NOW()
    );
    """)
    # Ensure a default row exists
    cursor.execute("SELECT COUNT(*) FROM runtime_config")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO runtime_config (system_prompt, conversation_history_limit, top_k_rag_hits)
            VALUES (%s, %s, %s)
        """, (
            "Hi, I’m Xavigate. Let’s explore who you are and where your energy wants to go...",
            3,
            4
        ))
    
    # Session summary table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory_summary (
        summary_id SERIAL PRIMARY KEY,
        uuid TEXT NOT NULL,
        summary_text TEXT,
        full_transcript JSONB,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)


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

MAX_SESSION_CHARACTERS = 15000  # Limit before triggering summarization and reset

def upsert_session_direct(mem: SessionMemory):
    now = datetime.utcnow()

    if not mem.conversation_log:
        print("⚠️ No conversation log to store — skipping upsert.")
        return

    # Save or update the session memory
    cursor.execute("""
        INSERT INTO session_memory (uuid, session_start, last_active, conversation_log, interim_scores, expires_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (uuid) DO UPDATE SET
            last_active = EXCLUDED.last_active,
            conversation_log = session_memory.conversation_log || EXCLUDED.conversation_log,
            interim_scores = EXCLUDED.interim_scores,
            expires_at = EXCLUDED.expires_at;
    """, (
        str(mem.uuid),
        now,
        now,
        json.dumps(mem.conversation_log, default=str),
        json.dumps(mem.interim_scores or {}, default=str),
        now + timedelta(days=90)
    ))

    # Check character count
    exchanges_text = json.dumps(mem.conversation_log.get("exchanges", []), default=str)
    if len(exchanges_text) > MAX_SESSION_CHARACTERS:
        print(f"⚠️ Session memory for {mem.uuid} exceeded {MAX_SESSION_CHARACTERS} chars — summarizing and clearing.")
        expire_session_logic(str(mem.uuid))


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
    cursor.execute("SELECT conversation_log FROM session_memory WHERE uuid = %s", (user_uuid,))
    rec = cursor.fetchone()
    if not rec or not rec[0]:
        return
    conv_log = rec[0]
    exchanges = conv_log.get("exchanges", []) if isinstance(conv_log, dict) else []

    transcript = ""
    for ex in exchanges:
        if "user_prompt" in ex:
            transcript += f"User: {ex.get('user_prompt', '')}\n"
        if "assistant_response" in ex:
            transcript += f"Assistant: {ex.get('assistant_response', '')}\n"

    # Persist user memory update
    try:
        from memory.consolidate_session import synthesize_persistent_update
        persistent_update = synthesize_persistent_update(UUID(user_uuid), plan={}, critique="", transcript=transcript)
        upsert_user(persistent_update)
    except Exception as e:
        print(f"❌ Persistence update failed: {e}")

    # Save transcript + summary
    try:
        summary_prompt = f"Summarize the following conversation in 1-2 sentences:\n\n{transcript}"
        comp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": summary_prompt}],
            temperature=0.3,
        )
        summary = comp.choices[0].message.content.strip()
    except Exception:
        summary = "Summary unavailable."

    cursor.execute(
        "INSERT INTO memory_summary (uuid, summary_text, full_transcript) VALUES (%s, %s, %s)",
        (user_uuid, summary, json.dumps(conv_log, default=str))
    )

    # Clear session
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

# Runtime configuration endpoints
@router.get("/runtime-config", response_model=RuntimeConfig)
def get_runtime_config():
    cursor.execute("SELECT system_prompt, conversation_history_limit, top_k_rag_hits FROM runtime_config ORDER BY id LIMIT 1")
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Runtime config not found")
    return {
        "system_prompt": row[0],
        "conversation_history_limit": row[1],
        "top_k_rag_hits": row[2],
    }

@router.post("/runtime-config")
def update_runtime_config(cfg: RuntimeConfig):
    now = datetime.utcnow()
    cursor.execute("""
        UPDATE runtime_config
        SET system_prompt = %s,
            conversation_history_limit = %s,
            top_k_rag_hits = %s,
            updated_at = %s
        WHERE id = 1;
    """, (
        cfg.system_prompt,
        cfg.conversation_history_limit,
        cfg.top_k_rag_hits,
        now
    ))
    return {"status": "ok"}

@router.get("/all-summaries/{uuid}")
def get_all_summaries(uuid: str):
    cursor.execute(
        "SELECT summary_text FROM memory_summary WHERE uuid = %s ORDER BY summary_id ASC",
        (uuid,)
    )
    return {"summaries": [row[0] for row in cursor.fetchall() if row[0]]}