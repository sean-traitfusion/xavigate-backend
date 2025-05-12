from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

from client import verify_key, rag_query

load_dotenv()

app = FastAPI(
    title="Chat Service",
    description="Orchestrates chat turns by proxying to RAG, storage, auth & stats services",
    version="0.1.0",
    root_path="/api/chat"
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
    """Incoming chat request"""
    prompt: str
    user_id: Optional[str] = None
    top_k: int = 3
    tags: Optional[str] = None

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
    "/chat",
    response_model=ChatResponse,
    responses={401: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
    tags=["chat"],
)
async def chat_endpoint(
    req: ChatRequest,
    x_xavigate_key: str = Header(..., alias="X-XAVIGATE-KEY"),
):
    if not await verify_key(x_xavigate_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Stub: delegate to RAG service for initial MVP
    result = await rag_query(req.prompt, req.top_k, req.tags)
    # Return dummy ChatResponse for frontend integration
    return ChatResponse(
        answer=result,
        sources=[],
        plan={},
        critique="",
        followup="",
    )