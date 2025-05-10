import os
import openai
import hashlib
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-3-small"
CACHE_FILE = Path(__file__).parent.parent / "shared/cache/embedding_cache.json"

# Load or init cache
if CACHE_FILE.exists():
    cache = json.loads(CACHE_FILE.read_text())
else:
    cache = {}

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def get_embedding(text: str) -> list[float]:
    key = hash_text(text)
    if key in cache:
        return cache[key]

    response = openai.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    vector = response.data[0].embedding
    cache[key] = vector
    CACHE_FILE.write_text(json.dumps(cache))
    return vector