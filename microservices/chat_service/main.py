from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import os
from openai import OpenAI
import httpx
from client import verify_key

openai_client = OpenAI()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://nginx:8080/api/auth")

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

    # Load environment
    STORAGE_URL = os.getenv("STORAGE_URL", "http://localhost:8011")
    RAG_URL = os.getenv("RAG_URL", "http://localhost:8017")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

    # Prepare headers for internal service calls
    internal_headers: dict = {}
    if authorization:
        internal_headers["Authorization"] = authorization
    # 1. Retrieve session memory (conversation log)
    async with httpx.AsyncClient() as client:
        mem_resp = await client.get(
            f"{STORAGE_URL}/memory/session-memory/{req.sessionId}",
            headers=internal_headers
        )
    if mem_resp.status_code != 200:
        conversation_log = {}
    else:
        conversation_log = mem_resp.json() or {}

    # Extract past exchanges (support both flat list or nested 'exchanges')
    exchanges = []
    if isinstance(conversation_log, dict) and "exchanges" in conversation_log:
        exchanges = conversation_log.get("exchanges", [])
    elif isinstance(conversation_log, list):
        exchanges = conversation_log

    # 1b. Retrieve existing session summary (if any)
    async with httpx.AsyncClient() as client:
        sum_resp = await client.get(
            f"{STORAGE_URL}/memory/summary/{req.sessionId}",
            headers=internal_headers
        )
    if sum_resp.status_code == 200:
        summary_json = sum_resp.json() or {}
        session_summary = summary_json.get("summary_text", "")
    else:
        session_summary = ""

    # Build recent history (last 5 exchanges)
    history = ""
    for ex in exchanges[-5:]:
        if "user_prompt" in ex and "assistant_response" in ex:
            history += f"User: {ex['user_prompt']}\nAssistant: {ex['assistant_response']}\n"
        elif ex.get("role") and ex.get("content"):
            role = ex.get("role").capitalize()
            history += f"{role}: {ex.get('content')}\n"

    # 2. Retrieve relevant glossary/context via Vector Search service
    async with httpx.AsyncClient() as client:
        vs_resp = await client.post(
            f"{os.getenv('RAG_URL')}/search",
            json={"query": req.message, "top_k": 5}  # ✅ No filters
        )
    if vs_resp.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch glossary chunks")
    chunks = vs_resp.json()
    # Build context string from chunks
    context = "\n\n".join([c.get("chunk", "") for c in chunks])

    # 3. Assemble GPT prompt
    SYSTEM_PROMPT = (
        "You are a Multiple Natures (MN) practitioner. The user you are helping has just completed the MNTEST, a 76-question personality assessment "
        "that evaluates 19 core traits — 10 Multiple Intelligences and 9 Multiple Natures — each on a scale of 1 to 10.\n\n"
        "Your goal is to help the user interpret and apply their MN profile in real-world contexts — including their work, energy patterns, decision-making, and sense of alignment."
        " Speak clearly and insightfully. Ground your responses in MN concepts and vocabulary. Refer to the user’s trait scores, past questions, and prior conversation when relevant."
    )
    # Profile section
    profile_section = f"USER PROFILE:\nName: {req.fullName or ''}\nUsername: {req.username}\nTrait Scores:\n"
    for trait, score in req.traitScores.items():
        profile_section += f"- {trait.title()}: {score}\n"

    # Build full prompt with optional session summary
    prompt_parts = [SYSTEM_PROMPT, "", profile_section]
    if session_summary:
        prompt_parts.append("SESSION SUMMARY:")
        prompt_parts.append(session_summary)
    prompt_parts.append("RECENT EXCHANGES:")
    prompt_parts.append(history)
    prompt_parts.append("GLOSSARY EXCERPTS:")
    prompt_parts.append(context)
    prompt_parts.append("\nCURRENT QUESTION:")
    prompt_parts.append(req.message)
    final_prompt = "\n".join(prompt_parts)

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

    # 5. Persist new exchange to memory service
    new_exchanges = exchanges.copy()
    new_exchanges.append({"user_prompt": req.message, "assistant_response": answer})
    save_payload = {"uuid": req.userId, "conversation_log": {"exchanges": new_exchanges}}
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{STORAGE_URL}/memory/session-memory",
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