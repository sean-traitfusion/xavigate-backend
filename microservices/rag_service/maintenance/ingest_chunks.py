import json
from pathlib import Path
from chromadb import PersistentClient
from openai import OpenAI
from uuid import uuid4

# Load your Chroma collection (edit path if needed)
client = PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="xavigate_knowledge")

# Load chunks from file
chunks = []
chunks_path = Path(__file__).parent / "data" / "bulk_chunks_all_cleaned.jsonl"

for i, line in enumerate(chunks_path.read_text(encoding="utf-8").splitlines(), start=1):
    clean_line = line.strip().replace('\u2028', ' ').replace('\u2029', ' ')
    if not clean_line:
        continue
    try:
        chunks.append(json.loads(clean_line))
    except json.JSONDecodeError as e:
        print(f"⚠️ Skipping malformed line {i}: {e}")

# Init OpenAI client
openai = OpenAI()  # Assumes API key is set in env var OPENAI_API_KEY

# Ingest loop
for chunk in chunks:
    content = chunk["content"]
    raw_meta = chunk["metadata"]
    metadata = {
        k: (", ".join(v) if isinstance(v, list) else v)
        for k, v in raw_meta.items()
    }
    embedding = openai.embeddings.create(
        model="text-embedding-3-small",
        input=content
    ).data[0].embedding

    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[str(uuid4())],
        embeddings=[embedding],
    )

print(f"✅ Successfully ingested {len(chunks)} chunks into ChromaDB.")