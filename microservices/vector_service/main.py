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

# Determine environment
ENV = os.getenv("ENV", "dev")
root_path = "/api/vector" if ENV == "prod" else ""

# Embedding and Chroma client imports
from maintenance.embeddings import get_embedding
from chromadb import PersistentClient

# Initialize Chroma client pointing to local Chroma DB path
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "chroma_db")
client = PersistentClient(path=CHROMA_DB_PATH)
# Use the same collection name as the RAG service
collection = client.get_or_create_collection(name="xavigate_knowledge")

class VectorSearchRequest(BaseModel):
    query: str = Field(..., description="The search query text")
    glossaryType: Optional[str] = Field("mn", description="Glossary type (e.g., 'mn')")
    top_k: int = Field(5, ge=1, le=10, description="Number of chunks to return")
    tags: Optional[List[str]] = None

class VectorChunk(BaseModel):
    title: str
    chunk: str
    topic: Optional[str]
    score: float

app = FastAPI(
    title="Vector Search Service",
    description="Retrieves relevant MN theory chunks via vector search",
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

@app.post("/search", response_model=List[VectorChunk], tags=["vector"])
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

    # 2. Build filter for metadata tags (optional)
    filters = {}
    if body.tags:
        # Try different filter formats for ChromaDB compatibility
        if len(body.tags) == 1:
            # Single tag - direct match
            filters = {"tag": body.tags[0]}
        else:
            # Multiple tags - use $in operator
            filters = {"tag": {"$in": body.tags}}

    # 3. Query the vector store
    try:
        print("🔍 Searching collection:", collection.name)
        print("🔎 Query:", body.query)
        print("🔧 Filters:", filters if filters else "None")

        query_args = {
            "query_embeddings": [embedding],
            "n_results": body.top_k,
        }
        if filters:
            query_args["where"] = filters

        results = collection.query(**query_args)
        print("🧠 Results:", results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector store query error: {e}")

    # 4. Unpack and format results
    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    chunks: List[VectorChunk] = []
    for text, meta, dist in zip(docs, metadatas, distances):
        score = 1 - dist if isinstance(dist, (float, int)) else 0.0
        chunks.append(VectorChunk(
            title=meta.get("source", "").replace("_", " ").title(),  # Use source as title
            chunk=text,
            topic=meta.get("type", ""),  # Use type as topic
            score=round(score, 4),
        ))

    return chunks

@app.get("/debug/embedding", tags=["debug"])
async def debug_embedding():
    try:
        # Import here to get fresh copy
        from maintenance.embeddings import get_embedding, CACHE_FILE, EMBEDDING_DIMENSIONS
        
        # Test embedding generation
        test_text = "Hello world"
        embedding = get_embedding(test_text)
        
        return {
            "cache_file_path": str(CACHE_FILE),
            "cache_file_exists": CACHE_FILE.exists(),
            "embedding_dimensions_config": EMBEDDING_DIMENSIONS,
            "actual_embedding_length": len(embedding),
            "test_text": test_text,
            "embedding_sample": embedding[:5]  # First 5 values
        }
    except Exception as e:
        return {"error": str(e), "traceback": str(e.__traceback__)}
    
@app.post("/debug/clear-cache", tags=["debug"])
async def clear_embedding_cache():
    try:
        from maintenance.embeddings import CACHE_FILE
        
        # Remove the cache file
        if CACHE_FILE.exists():
            CACHE_FILE.unlink()
            return {"message": "Cache cleared successfully", "cache_file": str(CACHE_FILE)}
        else:
            return {"message": "Cache file didn't exist", "cache_file": str(CACHE_FILE)}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/debug/chromadb", tags=["debug"])
async def debug_chromadb():
    try:
        # Test basic collection info
        count = collection.count()
        
        # Get sample documents to inspect metadata
        sample_docs = collection.get(limit=3)
        
        # Test query using OUR embedding function (not ChromaDB's internal one)
        query_embedding = get_embedding("Menu of Life")
        
        # Test simple query without filters using our embedding
        simple_results = collection.query(
            query_embeddings=[query_embedding],  # Use our embedding function
            n_results=3
        )
        
        # Test query with filters using our embedding  
        filtered_results = collection.query(
            query_embeddings=[query_embedding],  # Use our embedding function
            n_results=3,
            where={"tag": "menu_of_life"}
        )
        
        return {
            "chroma_db_path": CHROMA_DB_PATH,
            "collection_count": count,
            "query_embedding_length": len(query_embedding),
            "simple_query_count": len(simple_results.get("documents", [[]])[0]),
            "filtered_query_count": len(filtered_results.get("documents", [[]])[0]),
            "sample_metadata": sample_docs.get("metadatas", [])[:3],
            "simple_results": simple_results,
            "filtered_results": filtered_results
        }
    except Exception as e:
        return {"error": str(e)}