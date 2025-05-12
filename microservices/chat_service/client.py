import os
import httpx

# Service URLs (override via environment variables)
AUTH_URL = os.getenv("AUTH_URL", "http://localhost:8014")
RAG_URL = os.getenv("RAG_URL", "http://localhost:8010")
STORAGE_URL = os.getenv("STORAGE_URL", "http://localhost:8011")
STATS_URL = os.getenv("STATS_URL", "http://localhost:8012")

ENV = os.getenv("ENV", "dev")

async def verify_key(key: str) -> bool:
    """
    Verify API key via auth service, or stub in development.
    """
    # In development, accept any non-empty key
    if os.getenv("ENV", "dev") == "dev":
        return bool(key and key.strip())
    # In production, call auth service
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{AUTH_URL}/verify", json={"key": key}, timeout=5.0
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("valid", False)
        except httpx.HTTPError:
            return False

async def rag_query(prompt: str, top_k: int = 3, tags: str | None = None) -> str:
    """
    Query the RAG service for context documents.
    """
    # In development, return a stubbed answer
    if os.getenv("ENV", "dev") == "dev":
        return f"[stub answer for prompt: '{prompt}']"
    params: dict[str, str | int] = {"prompt": prompt, "top_k": top_k}
    if tags:
        params["tags"] = tags
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{RAG_URL}/rag/query", params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("result", "")

async def get_profile(user_id: str) -> dict:
    """
    Fetch a user profile from the storage service.
    In dev, returns a stubbed profile.
    """
    if ENV == "dev":
        return {"user_id": user_id, "profile": {}}
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{STORAGE_URL}/profile/api/user/{user_id}", timeout=5.0
        )
        resp.raise_for_status()
        return resp.json()

async def append_session_log(user_id: str, conversation_log: dict) -> None:
    """
    Append a conversation log to the storage service.
    In dev, no-op stub.
    """
    if ENV == "dev":
        return
    async with httpx.AsyncClient() as client:
        # Replace with actual storage endpoint when ready
        await client.post(
            f"{STORAGE_URL}/session/api/session/reflection",
            json={"user_id": user_id, "conversation_log": conversation_log},
            timeout=5.0
        )

async def send_stats_event(event_name: str, payload: dict) -> None:
    """
    Send an analytics event to the stats service.
    In dev, no-op stub.
    """
    if ENV == "dev":
        return
    async with httpx.AsyncClient() as client:
        # Replace with actual stats endpoint when ready
        await client.post(
            f"{STATS_URL}/stats/event",
            json={"event": event_name, "payload": payload},
            timeout=5.0
        )