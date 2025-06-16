from fastapi import FastAPI, HTTPException, Header, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import os
from openai import OpenAI
import httpx
from client import verify_key
import json

openai_client = OpenAI()

# Use localhost when running outside Docker, auth_service when inside
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8014")
# Override for local testing
if os.getenv("AUTH_SERVICE_OVERRIDE"):
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_OVERRIDE")

async def verify_key(token: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{AUTH_SERVICE_URL}/verify", json={"key": token})
            return resp.status_code == 200 and resp.json().get("valid", False)
    except Exception as e:
        print("❌ Auth verification failed:", e)
        return False

# JWT authentication dependency
async def require_jwt(authorization: str | None = Header(None, alias="Authorization")):
    if os.getenv("ENV", "dev") == "dev":
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")
    token = authorization.split(" ", 1)[1]
    if not await verify_key(token):
        raise HTTPException(status_code=401, detail="Invalid token")

# Load root and service .env for unified configuration
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)

service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(dotenv_path=service_env, override=True)

ENV = os.getenv("ENV", "dev")
root_path = "/api/chat" if ENV == "prod" else ""

# Load environment
STORAGE_URL = os.getenv("STORAGE_URL", "http://localhost:8011")
RAG_URL = os.getenv("RAG_URL", "http://localhost:8017")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Default system prompt for chat if not provided in config
DEFAULT_PROMPT = "You are Xavigate, a life guide — an experienced Multiple Natures (MN) practitioner..."

app = FastAPI(
    title="Chat Service",
    description="Orchestrates chat turns by proxying to RAG, storage, auth & stats services",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"url": "openapi.json"},
    root_path=root_path,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "chat"}

class ChatRequest(BaseModel):
    """Payload for chat query including user context and MNTEST scores"""
    userId: str = Field(..., description="Cognito sub claim for the user")
    username: str = Field(..., description="User's unique username")
    fullName: Optional[str] = Field(None, description="User's display name")
    traitScores: Dict[str, float] = Field(
        ..., description="Map of 19 MNTEST trait names to their scores (1-10)"
    )
    message: str = Field(..., description="The user's current chat message")
    sessionId: str = Field(..., description="Identifier for this chat session")

    # ✅ Optional overrides from config panel
    systemPrompt: Optional[str] = Field(
        None, description="Custom system prompt to override default"
    )

    topK_RAG_hits: Optional[int] = Field(
        None, ge=1, le=10, description="How many RAG chunks to retrieve"
    )

class Document(BaseModel):
    """RAG source document returned to client"""
    text: str
    metadata: Dict[str, Any]

class ChatResponse(BaseModel):
    """Payload returned by /chat"""
    answer: str
    sources: List[Document]
    plan: Dict[str, Any]
    critique: str
    followup: str

class ErrorResponse(BaseModel):
    detail: str



# Endpoint to retrieve runtime configuration
@app.get("/config")
async def get_config():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config")
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch config from storage service: {e}")

@app.post(
    "/query",
    response_model=ChatResponse,
    responses={401: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
    tags=["chat"],
)
async def chat_endpoint(
    req: ChatRequest,
    authorization: str | None = Header(None, alias="Authorization"),
    _=Depends(require_jwt),
):
    # Stub response in dev mode to avoid real OpenAI calls
    if os.getenv("ENV", "dev") == "dev":
        return ChatResponse(answer="Dev stub response", sources=[], plan={}, critique="", followup="")
    # Extract token for downstream calls (empty in dev)
    token = authorization.split(" ", 1)[1] if authorization else ""

    # Prepare headers for internal service calls
    internal_headers = {"Authorization": authorization} if authorization else {}

    async with httpx.AsyncClient() as client:
        # 1. Retrieve session memory (conversation log)
        mem_resp = await client.get(
            f"{STORAGE_URL}/api/memory/session-memory/{req.sessionId}",
            headers=internal_headers
        )
        conversation_log = mem_resp.json().get("exchanges", []) if mem_resp.status_code == 200 else []

        # Extract past exchanges (support both flat list or nested 'exchanges')
        exchanges = []
        if isinstance(conversation_log, dict) and "exchanges" in conversation_log:
            exchanges = conversation_log.get("exchanges", [])
        elif isinstance(conversation_log, list):
            exchanges = conversation_log

        # 1b. Get persistent memory (user summary) instead of session summaries
        persistent_resp = await client.get(
            f"{STORAGE_URL}/api/memory/persistent-memory/{req.userId}",
            headers=internal_headers
        )
        persistent_memory = ""
        if persistent_resp.status_code == 200:
            data = persistent_resp.json()
            persistent_memory = data.get("summary", "")

        # 1c. Get config defaults from storage service
        try:
            config_resp = await client.get(
                f"{STORAGE_URL}/api/memory/runtime-config",
                headers=internal_headers
            )
            config_defaults = config_resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch runtime config: {e}")

        top_k = req.topK_RAG_hits or config_defaults.get("top_k_rag_hits", 5)
        SYSTEM_PROMPT = req.systemPrompt or config_defaults.get("system_prompt", DEFAULT_PROMPT)

        # Convert exchanges to session lines for prompt optimization
        session_lines = []
        for ex in reversed(exchanges):  # Most recent first
            if "user_prompt" in ex and "assistant_response" in ex:
                session_lines.append(f"User: {ex['user_prompt']}")
                session_lines.append(f"Assistant: {ex['assistant_response']}")
            elif ex.get("role") and ex.get("content"):
                session_lines.append(f"{ex['role'].capitalize()}: {ex['content']}")

        # 2. Retrieve relevant glossary/context via Vector Search service
        vs_resp = await client.post(f"{RAG_URL}/search", json={"query": req.message, "top_k": top_k})
        if vs_resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch glossary chunks")
        chunks = vs_resp.json()

        # Build context string from chunks
        context = "\n\n".join([c.get("chunk", "") for c in chunks])

        # 3. Build base prompt with user profile
        profile_parts = [
            f"Name: {req.fullName or 'Unknown'}",
            f"Username: {req.username}",
            "Trait Scores:"
        ]
        for trait, score in req.traitScores.items():
            profile_parts.append(f"- {trait.title()}: {score}")
        
        # Create base prompt with system prompt and profile
        base_prompt_parts = [SYSTEM_PROMPT]
        if req.fullName or req.username:
            base_prompt_parts.append(f"\nUser Profile:\n" + "\n".join(profile_parts))
        
        base_prompt = "\n".join(base_prompt_parts)
        
        # 3b. Optimize prompt using the prompt manager
        optimize_resp = await client.post(
            f"{STORAGE_URL}/api/memory/optimize-prompt",
            json={
                "base_prompt": base_prompt,
                "uuid": req.userId,
                "rag_context": context
            },
            headers=internal_headers
        )
        
        if optimize_resp.status_code == 200:
            optimize_data = optimize_resp.json()
            final_prompt = optimize_data["final_prompt"]
            metrics = optimize_data["metrics"]
            
            # Log metrics for monitoring
            print(f"📊 Prompt metrics for {req.userId}:")
            print(f"   Total: {metrics['total_chars']} chars")
            print(f"   Utilization: {metrics['utilization_percent']:.1f}%")
        else:
            # Fallback to simple prompt if optimization fails
            final_prompt = f"{base_prompt}\n\nCurrent Question: {req.message}\n\nContext:\n{context}"

        # 4. Call OpenAI
    
        try:
            completion = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": final_prompt}
                ],
                temperature=0.3,
            )
            answer = completion.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")

        # 5. Save the interaction using new memory endpoint
        save_payload = {
            "userId": req.userId,
            "sessionId": req.sessionId,
            "messages": [
                {"role": "user", "content": req.message},
                {"role": "assistant", "content": answer}
            ]
        }
        
        await client.post(
            f"{STORAGE_URL}/api/memory/save",
            json=save_payload,
            headers=internal_headers
        )

        # 6. Build response sources from vector chunks
        sources = []
        for c in chunks:
            sources.append({
                "text": c.get("chunk", ""),
                "metadata": {
                    "title": c.get("title"),
                    "topic": c.get("topic"),
                    "score": c.get("score"),
                }
            })
        return ChatResponse(
            answer=answer,
            sources=sources,
            plan={},
            critique="",
            followup="",
        )
    
@app.get("/__admin/config-ui", response_class=HTMLResponse)
async def config_ui():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config")
            cfg = resp.json()
        except Exception:
            cfg = {
                "system_prompt": "Failed to load config.",
                "top_k_rag_hits": 5
            }

    return f"""
    <html>
    <head>
        <title>Xavigate Config Panel</title>
        <style>
            body {{ font-family: sans-serif; max-width: 800px; margin: 2rem auto; padding: 1rem; }}
            textarea {{ width: 100%; height: 300px; font-family: monospace; padding: 1rem; }}
            input {{ width: 100px; padding: 0.5rem; font-size: 1rem; }}
            button {{ margin-top: 1rem; padding: 0.75rem 1.5rem; font-size: 1rem; }}
            label {{ display: block; margin-top: 1rem; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Xavigate Runtime Config</h1>
        <form method="POST" action="/api/chat-ui">
            <label for="system_prompt">System Prompt:</label>
            <textarea name="system_prompt">{cfg.get("system_prompt", "")}</textarea>

            <label for="top_k">Top K RAG Hits:</label>
            <input type="number" name="top_k" value="{cfg.get("top_k_rag_hits", 5)}" min="1" max="10"/>

            <br/>
            <button type="submit" name="action" value="save">💾 Save Config</button>
            <button type="submit" name="action" value="test">▶️ Run Test Prompt</button>
            <br>/>
            <label for="auth_token">Auth Token:</label>
            <input type="text" name="auth_token" style="width:100%" />

            <label for="test_message">Test Prompt:</label>
            <input type="text" name="test_message" style="width:100%" placeholder="What would you like to explore today?" />

            
        </form>
    </body>
    </html>
    """

from fastapi import Form

@app.post("/__admin/config-ui", response_class=HTMLResponse)
async def save_config_ui(
    system_prompt: Optional[str] = Form(None),
    top_k: Optional[int] = Form(None),
    auth_token: Optional[str] = Form(None),
    test_message: Optional[str] = Form(None),
    action: Optional[str] = Form(None),
):
    payload = None
    test_output = None
    status_message = None

    if not system_prompt and auth_token:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config")
                cfg = resp.json()
                system_prompt = cfg.get("system_prompt", "")
                top_k = top_k or cfg.get("top_k_rag_hits", 5)
            except Exception:
                system_prompt = ""
                top_k = 5

    # 1. Save updated config
    if action == "save":
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{STORAGE_URL}/api/memory/runtime-config",
                headers=headers,
                json={
                    "system_prompt": system_prompt,
                    "conversation_history_limit": 0,
                    "top_k_rag_hits": top_k
                }
            )
            if resp.status_code == 200:
                status_message = "✅ Configuration saved successfully."
            else:
                status_message = f"❌ Save failed: {resp.status_code} — {await resp.aread()}"

    # 2. Run test
    if action == "test" and auth_token and test_message:
        try:
            payload = {
                "userId": "debug-user",
                "username": "test",
                "fullName": "Admin Tester",
                "traitScores": {"creative": 7, "logical": 6, "emotional": 8},
                "message": test_message,
                "sessionId": "debug-session",
                "systemPrompt": system_prompt,
                "topK_RAG_hits": top_k,
            }
            async with httpx.AsyncClient() as client:
                # Seed an empty session for test
                await client.post(
                    f"{STORAGE_URL}/api/memory/session-memory",
                    json={
                        "uuid": "debug-session",
                        "conversation_log": {"exchanges": []}
                    }
                )
                test_prompt = payload.copy()
                test_prompt["message"] = "[Prompt not visible]"
                query_resp = await client.post(
                    f"{os.getenv('CHAT_SERVICE_URL', 'http://localhost:8015')}/query",
                    headers={"Authorization": f"Bearer {auth_token}"},
                    json=payload
                )
                if query_resp.status_code == 200:
                    test_output = query_resp.json().get("answer", "[No answer returned]")
                else:
                    test_output = f"[Error {query_resp.status_code}]: {query_resp.text}"
        except Exception as e:
            test_output = f"Test failed: {e}"
    # Refresh config from storage after test or save to pre-populate form fields
    if auth_token:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{STORAGE_URL}/api/memory/runtime-config",
                    headers={"Authorization": f"Bearer {auth_token}"}
                )
                if resp.status_code == 200:
                    cfg = resp.json()
                    system_prompt = cfg.get("system_prompt", system_prompt)
                    top_k = cfg.get("top_k_rag_hits", top_k)
            except Exception:
                pass  # Keep existing values if fetch fails

    # Render HTML output
    return f"""
    <html><body>
        <h1>Xavigate Runtime Config</h1>
        {f'<div style="margin: 1rem 0; padding: 1rem; background-color: #eef; border-left: 4px solid #88f;">{status_message}</div>' if status_message else ''}
        <form method="POST" action="/api/chat-ui">
            <label>System Prompt:</label><br>
            <textarea name="system_prompt" rows="10" cols="80">{system_prompt or ""}</textarea><br><br>

            <label>Top K:</label><br>
            <input type="number" name="top_k" value="{top_k or 5}" min="1" max="10"><br><br>

            <label>Auth Token:</label><br>
            <input type="text" name="auth_token" style="width:100%" value="{auth_token or ''}"><br><br>

            <label>Test Prompt:</label><br>
            <input type="text" name="test_message" style="width:100%" value="{test_message or ''}"><br><br>

            <button type="submit" name="action" value="save">💾 Save Config</button>
            <button type="submit" name="action" value="test">▶️ Run Test Prompt</button>
        </form>
        {f'<div style="color: red; margin-top: 1rem;">⚠️ Auth token required to view current config.</div>' if not auth_token else ''}

        <hr>
        <h3>Test Output:</h3>
        <div style="width: 100%; max-height: 300px; overflow: auto; border: 1px solid #ccc; padding: 1rem; font-family: monospace; background-color: #f9f9f9;">
            {test_output or "—"}
        </div>
        <hr>
        <h3>Final Prompt Sent:</h3>
        <div style="width: 100%; max-height: 300px; overflow: auto; border: 1px solid #ccc; padding: 1rem; font-family: monospace; background-color: #f9f9f9;">
            {json.dumps(payload, indent=2) if payload else "—"}
        </div>
        <hr>
    </body></html>
    """