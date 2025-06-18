from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import os
from openai import OpenAI
import httpx
from client import verify_key
from prompt_builder import build_styled_prompt, format_user_context, DEFAULT_MN_PROMPT

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

# Load environment
STORAGE_URL = os.getenv("STORAGE_URL", "http://localhost:8011")
RAG_URL = os.getenv("RAG_URL", "http://localhost:8017")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Import default prompt from prompt_builder
from prompt_builder import DEFAULT_MN_PROMPT as DEFAULT_PROMPT

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

        # 1b. Retrieve existing session summary (if any)
        sum_resp = await client.get(
            f"{STORAGE_URL}/api/memory/all-summaries/{req.userId}",
            headers=internal_headers
        )

        if sum_resp.status_code == 200:
            summaries = sum_resp.json().get("summaries", [])
            # Join oldest → newest summaries, capped to ~3000 chars
            session_summary = ""
            summary_chars = 0
            for s in summaries:
                if summary_chars + len(s) > 3000:
                    break
                session_summary += s + "\n"
                summary_chars += len(s)
        else:
            session_summary = ""

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
        base_prompt = req.systemPrompt or config_defaults.get("system_prompt", DEFAULT_PROMPT)
        prompt_style = config_defaults.get("prompt_style", "default")
        custom_style_modifier = config_defaults.get("custom_style_modifier", None)
        
        # Build styled system prompt
        SYSTEM_PROMPT = build_styled_prompt(base_prompt, prompt_style, custom_style_modifier)

        # Build recent history (# of exchanges depends on config)
        MAX_HISTORY_CHARS = 10000
        history = ""
        char_count = 0

        # Reverse loop to prioritize most recent turns
        for ex in reversed(exchanges):
            turn = ""
            if "user_prompt" in ex and "assistant_response" in ex:
                turn = f"User: {ex['user_prompt']}\nAssistant: {ex['assistant_response']}\n"
            elif ex.get("role") and ex.get("content"):
                turn = f"{ex['role'].capitalize()}: {ex['content']}\n"

            if char_count + len(turn) > MAX_HISTORY_CHARS:
                break

            history = turn + history  # prepend so history flows oldest → newest
            char_count += len(turn)

        # 2. Retrieve relevant glossary/context via Vector Search service
        vs_resp = await client.post(f"{RAG_URL}/search", json={"query": req.message, "top_k": top_k})
        if vs_resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch glossary chunks")
        chunks = vs_resp.json()

        # Build context string from chunks
        context = "\n\n".join([c.get("chunk", "") for c in chunks])

        # 3. Assemble GPT prompt
        # Build user profile section with trait scores
        profile_lines = [f"Name: {req.fullName or 'User'}", f"Username: {req.username}"]
        profile_lines.append("\nTrait Scores:")
        
        # Group traits by score range for better interpretation
        dominant_traits = []
        balanced_traits = []
        suppressed_traits = []
        
        for trait, score in req.traitScores.items():
            trait_entry = f"- {trait.replace('_', ' ').title()}: {score}/10"
            if score >= 7:
                dominant_traits.append((trait, score))
            elif score <= 3:
                suppressed_traits.append((trait, score))
            else:
                balanced_traits.append((trait, score))
            profile_lines.append(trait_entry)
        
        # Add trait analysis summary
        if dominant_traits:
            profile_lines.append(f"\nDominant Traits (strengths): {', '.join([t[0].replace('_', ' ').title() for t in dominant_traits])}")
        if suppressed_traits:
            profile_lines.append(f"Suppressed Traits (growth areas): {', '.join([t[0].replace('_', ' ').title() for t in suppressed_traits])}")
        
        profile_section = "\n".join(profile_lines)
        
        # Format user context using the utility function
        user_context = format_user_context(
            user_profile=profile_section,
            session_summary=session_summary,
            recent_history=history,
            rag_context=context
        )
        
        # Build the final user message
        final_prompt = f"{user_context}\n\nCURRENT QUESTION:\n{req.message}"

        # 4. Call OpenAI with improved prompting
        try:
            # Use config values for OpenAI parameters
            model = config_defaults.get("model", "gpt-3.5-turbo")
            temperature = config_defaults.get("temperature", 0.7)
            max_tokens = config_defaults.get("max_tokens", 1000)
            presence_penalty = config_defaults.get("presence_penalty", 0.1)
            frequency_penalty = config_defaults.get("frequency_penalty", 0.1)
            
            completion = openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": final_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty
            )
            answer = completion.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")

        # 5. Persist new exchange to memory service
        new_exchanges = exchanges.copy()
        new_exchanges.append({"user_prompt": req.message, "assistant_response": answer})
        save_payload = {"uuid": req.userId, "conversation_log": {"exchanges": new_exchanges}}
        # 5. Persist new exchange to memory service
        await client.post(
            f"{STORAGE_URL}/api/memory/session-memory",
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
    
