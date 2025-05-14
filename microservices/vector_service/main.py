from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import os

# Load environment variables
# Load environment variables
from dotenv import load_dotenv
# Load root and service .env for unified configuration
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)
service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(dotenv_path=service_env, override=True)

# Embedding and Chroma client imports
from embeddings import get_embedding
from chromadb import PersistentClient

# Initialize Chroma client pointing to local Chroma DB path
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "chroma_db")
client = PersistentClient(path=CHROMA_DB_PATH)
# Use the same collection name as the RAG service
collection = client.get_or_create_collection(name="xavigate_ad")

class VectorSearchRequest(BaseModel):
    query: str = Field(..., description="The search query text")
    glossaryType: Optional[str] = Field("mn", description="Glossary type (e.g., 'mn')")
    top_k: int = Field(5, ge=1, le=10, description="Number of chunks to return")

class VectorChunk(BaseModel):
    title: str
    chunk: str
    topic: Optional[str]
    score: float

app = FastAPI(
    title="Vector Search Service",
    description="Retrieves relevant MN theory chunks via vector search",
    version="0.1.0",
)
ENV = os.getenv("ENV", "dev")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/vector/search", response_model=List[VectorChunk], tags=["vector"])
async def vector_search(body: VectorSearchRequest):
    # In dev mode, return static sample chunks
    if ENV == "dev":
        return [
            VectorChunk(
                title="Creative",
                chunk="Creative is the energy of imagination, originality, and expression.",
                topic="Trait",
                score=1.0,
            ),
            VectorChunk(
                title="Logical",
                chunk="Logical intelligence is about reasoning, pattern recognition, and critical thinking.",
                topic="Trait",
                score=0.9,
            ),
            VectorChunk(
                title="Providing",
                chunk="Providing is the energy of nurturing, support, and sustaining others' well-being.",
                topic="Trait",
                score=0.85,
            ),
        ]
    # 1. Embed the query
    try:
        embedding = get_embedding(body.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding error: {e}")

    # 2. Build filter for glossaryType
    filters = {"glossaryType": body.glossaryType} if body.glossaryType else {}

    # 3. Query the vector store
    try:
        results = collection.query(
            query_embeddings=[embedding],
            n_results=body.top_k,
            where=filters,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector store query error: {e}")

    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    # 4. Format and return
    chunks: List[VectorChunk] = []
    for text, meta, dist in zip(docs, metadatas, distances):
        # Convert distance to similarity score (cosine)
        score = 1 - dist if isinstance(dist, (float, int)) else 0.0
        chunks.append(VectorChunk(
            title=meta.get("title", ""),
            chunk=text,
            topic=meta.get("topic"),
            score=round(score, 4),
        ))
    return chunks