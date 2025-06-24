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
from chat_logger import ChatPipelineLogger
from rag_filter import filter_rag_query
from datetime import datetime

openai_client = OpenAI()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://nginx:8080/api/auth")

async def verify_key(token: str) -> bool:
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=5.0)) as client:
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
# root_path = "/api/chat" if ENV == "prod" else ""

# Load environment
STORAGE_URL = os.getenv("STORAGE_URL", "http://localhost:8011")
VECTOR_URL = os.getenv("VECTOR_URL", "http://localhost:8017")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize chat logger
chat_logger = ChatPipelineLogger(STORAGE_URL)

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
    # root_path=root_path,
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
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=5.0)) as client:
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
    # if os.getenv("ENV", "dev") == "dev":
    #     return ChatResponse(answer="Dev stub response", sources=[], plan={}, critique="", followup="")
    # Extract token for downstream calls (empty in dev)
    token = authorization.split(" ", 1)[1] if authorization else ""

    # Prepare headers for internal service calls
    internal_headers = {"Authorization": authorization} if authorization else {}
    
    # Start request timing
    chat_logger.start_request()
    request_start = datetime.utcnow()

    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=5.0)) as client:
        # 1. Retrieve session memory (conversation log)
        memory_start = datetime.utcnow()
        mem_resp = await client.get(
            f"{STORAGE_URL}/api/memory/session-memory/{req.sessionId}",
            headers=internal_headers
        )
        
        # Enhanced debug logging for session memory
        print(f"Debug - Session memory URL: {STORAGE_URL}/api/memory/session-memory/{req.sessionId}")
        print(f"Debug - Session memory response status: {mem_resp.status_code}")
        
        if mem_resp.status_code == 200:
            raw_response = mem_resp.json()
            print(f"Debug - Raw session memory response: {raw_response}")
            conversation_log = raw_response.get("exchanges", [])
        else:
            print(f"Debug - Session memory error response: {mem_resp.text}")
            conversation_log = []

        # Extract past exchanges (support both flat list or nested 'exchanges')
        exchanges = []
        if isinstance(conversation_log, dict) and "exchanges" in conversation_log:
            exchanges = conversation_log.get("exchanges", [])
        elif isinstance(conversation_log, list):
            exchanges = conversation_log
            
        print(f"Debug - Number of exchanges extracted: {len(exchanges)}")
        if exchanges:
            print(f"Debug - First exchange: {exchanges[0]}")
            print(f"Debug - Last exchange: {exchanges[-1]}")

        # 1b. Retrieve existing session summary (if any)
        sum_resp = await client.get(
            f"{STORAGE_URL}/api/memory/all-summaries/{req.userId}",
            headers=internal_headers
        )
        
        # Enhanced debug logging for summaries
        print(f"Debug - Summary URL: {STORAGE_URL}/api/memory/all-summaries/{req.userId}")
        print(f"Debug - Summary response status: {sum_resp.status_code}")

        if sum_resp.status_code == 200:
            raw_summary_response = sum_resp.json()
            print(f"Debug - Raw summary response: {raw_summary_response}")
            summaries = raw_summary_response.get("summaries", [])
            # Join oldest → newest summaries, capped to ~3000 chars
            session_summary = ""
            summary_chars = 0
            for s in summaries:
                if summary_chars + len(s) > 3000:
                    break
                session_summary += s + "\n"
                summary_chars += len(s)
            print(f"Debug - Number of summaries: {len(summaries)}")
            print(f"Debug - Total summary length: {len(session_summary)}")
            if summaries:
                print(f"Debug - First summary preview: {summaries[0][:100] if summaries[0] else 'Empty'}")
        else:
            print(f"Debug - Summary error response: {sum_resp.text}")
            session_summary = ""
        
        chat_logger.log_timing("memory_fetch_ms", memory_start)

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
            
        print(f"Debug - Built history length: {len(history)}")

        # 2. Retrieve relevant glossary/context via Vector Search service
        rag_start = datetime.utcnow()
        
        # Apply intelligent filtering to prevent specialized content dominance
        user_context = {
            'user_id': req.userId,
            'username': req.username,
            # Could add flags here like 'needs_reintegration' based on user profile
        }
        filter_params = filter_rag_query(req.message, user_context)
        
        # Enhanced debug logging for RAG
        rag_request = {
            "query": req.message, 
            "top_k": top_k,
            "tags": filter_params.get('tags', [])  # Apply tag filtering
        }
        print(f"Debug - RAG URL: {VECTOR_URL}/search")
        print(f"Debug - RAG request: {rag_request}")
        print(f"Debug - Filter params: {filter_params}")
        
        vs_resp = await client.post(f"{VECTOR_URL}/search", json=rag_request)
        
        print(f"Debug - RAG response status: {vs_resp.status_code}")
        
        if vs_resp.status_code != 200:
            print(f"Debug - RAG error response: {vs_resp.text}")
            raise HTTPException(status_code=500, detail="Failed to fetch glossary chunks")
        
        chunks = vs_resp.json()
        print(f"Debug - Raw RAG response type: {type(chunks)}")
        print(f"Debug - Raw RAG response: {chunks if isinstance(chunks, dict) else f'{len(chunks)} items'}")
        
        chat_logger.log_timing("rag_fetch_ms", rag_start)
        
        # Debug logging
        print(f"Debug - RAG response: {len(chunks) if isinstance(chunks, list) else 'Not a list'} chunks returned")
        if isinstance(chunks, list) and chunks:
            print(f"Debug - First chunk keys: {chunks[0].keys() if isinstance(chunks[0], dict) else 'Not a dict'}")
            print(f"Debug - First chunk preview: {str(chunks[0])[:200]}")

        # Build context string from chunks
        filtered_chunks = []
        if isinstance(chunks, list):
            # Apply post-filtering to results
            from rag_filter import RAGQueryFilter
            rag_filter = RAGQueryFilter()
            
            for chunk in chunks:
                if isinstance(chunk, dict):
                    # Check if this chunk should be filtered out
                    chunk_metadata = {
                        'tags': chunk.get('topic', ''),  # Map topic to tags
                        'tag': chunk.get('topic', ''),
                        'title': chunk.get('title', '')
                    }
                    
                    if not rag_filter.should_filter_result(
                        chunk.get('chunk', ''), 
                        chunk_metadata, 
                        filter_params
                    ):
                        filtered_chunks.append(chunk)
            
            # Re-rank results to ensure relevance
            filtered_chunks = rag_filter.rerank_results(filtered_chunks, req.message, filter_params)
            
            context = "\n\n".join([c.get("chunk", "") for c in filtered_chunks])
            print(f"Debug - Filtered {len(chunks)} chunks to {len(filtered_chunks)}")
        else:
            context = ""
            filtered_chunks = []
            print(f"Debug - RAG response is not a list, it's a {type(chunks)}")
            
        print(f"Debug - Final RAG context length: {len(context)}")
        if context:
            print(f"Debug - RAG context preview: {context[:200]}...")

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
        llm_start = datetime.utcnow()
        model_params = {}
        error_msg = None
        
        try:
            # Use config values for OpenAI parameters
            model = config_defaults.get("model", "gpt-3.5-turbo")
            temperature = config_defaults.get("temperature", 0.7)
            max_tokens = config_defaults.get("max_tokens", 1000)
            presence_penalty = config_defaults.get("presence_penalty", 0.1)
            frequency_penalty = config_defaults.get("frequency_penalty", 0.1)
            
            model_params = {
                "temperature": temperature,
                "max_tokens": max_tokens,
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty
            }
            
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
            chat_logger.log_timing("llm_call_ms", llm_start)
        except Exception as e:
            error_msg = str(e)
            chat_logger.log_timing("llm_call_ms", llm_start)
            raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")

        # 5. Log the complete interaction
        await chat_logger.log_chat_interaction(
            user_id=req.userId,
            session_id=req.sessionId,
            user_message=req.message,
            assistant_response=answer,
            system_prompt=SYSTEM_PROMPT,
            final_prompt=final_prompt,
            rag_context=context,
            model=model,
            model_params=model_params,
            session_memory=history,
            persistent_memory=session_summary,
            error=error_msg,
            headers=internal_headers
        )
        
        # 6. Persist new exchange to memory service
        new_exchanges = exchanges.copy()
        new_exchanges.append({"user_prompt": req.message, "assistant_response": answer})
        save_payload = {
            "uuid": req.sessionId,  # SessionMemory expects session ID in uuid field
            "conversation_log": {
                "exchanges": new_exchanges,
                "session_id": req.sessionId,  # Also pass session_id in conversation_log
                "user_id": req.userId  # Pass user_id for reference
            }
        }
        await client.post(
            f"{STORAGE_URL}/api/memory/session-memory",
            json=save_payload,
            headers=internal_headers,
            timeout=60.0  # Increased timeout for large memory saves
        )

        # 7. Build response sources from vector chunks (use filtered chunks)
        sources = []
        for c in filtered_chunks:
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
    
