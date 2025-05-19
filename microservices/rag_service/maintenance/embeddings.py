#rag_service/maintenance/embeddings.py
import os
import openai
import hashlib
import json
from pathlib import Path
from dotenv import load_dotenv

# Load root and service .env for unified configuration
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536  # Explicitly set dimensions to match ingestion
# Point to shared cache under /app/shared
CACHE_FILE = Path(__file__).parent.parent / "shared/cache/embedding_cache.json"

# Initialize or load embedding cache
if CACHE_FILE.exists():
    _cache = json.loads(CACHE_FILE.read_text())
else:
    _cache = {}

def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def get_embedding(text: str) -> list[float]:
    """
    Returns a vector embedding for the given text, using cache when available.
    """
    key = _hash_text(text)
    if key in _cache:
        return _cache[key]

    response = openai.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
        dimensions=EMBEDDING_DIMENSIONS  # Explicitly set dimensions
    )
    vector = response.data[0].embedding
    _cache[key] = vector
    # Persist cache
    try:
        CACHE_FILE.write_text(json.dumps(_cache))
    except Exception:
        pass
    return vector