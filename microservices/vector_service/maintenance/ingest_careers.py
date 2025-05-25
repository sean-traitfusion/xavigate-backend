import json
import os
from pathlib import Path
from uuid import uuid4
from chromadb import PersistentClient
from openai import OpenAI

# Load .env values
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "../chroma_db")
CHUNKS_PATH = chunks_path = Path(__file__).parent / "mn_careers_chunks.jsonl"

# Connect to Chroma
client = PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name="xavigate_knowledge")

# Load JSONL chunks
chunks = []
chunks_path = Path(CHUNKS_PATH)
for i, line in enumerate(chunks_path.read_text(encoding="utf-8").splitlines(), start=1):
    clean_line = line.strip().replace('\u2028', ' ').replace('\u2029', ' ')
    if not clean_line:
        continue
    try:
        chunks.append(json.loads(clean_line))
    except json.JSONDecodeError as e:
        print(f"⚠️ Skipping malformed line {i}: {e}")

# Init OpenAI client
openai = OpenAI()

# Ingest loop
for chunk in chunks:
    content = chunk.get("content") or chunk.get("text")
    if not content:
        print("⚠️ Skipping chunk with no 'content' or 'text'")
        continue

    raw_metadata = dict(chunk.get("metadata", {}))

    # Flatten metadata
    flattened_metadata = {}
    for k, v in raw_metadata.items():
        if isinstance(v, dict):
            for subkey, subval in v.items():
                flat_key = f"{k}_{subkey}".replace(" ", "_")
                flattened_metadata[flat_key] = subval
        elif isinstance(v, list):
            flattened_metadata[k] = " ".join(str(i) for i in v)
            if k in ("tags", "clusters"):
                flattened_metadata[k[:-1]] = v[0] if v else "uncategorized"
        else:
            flattened_metadata[k] = v

    # Fallback tag logic
    tag_list = raw_metadata.get("tags", [])
    if isinstance(tag_list, list):
        final_tags = tag_list
    elif isinstance(tag_list, str):
        final_tags = tag_list.split()
    else:
        final_tags = []

    if not final_tags:
        final_tags = ["uncategorized"]

    flattened_metadata["tags"] = " ".join(final_tags)
    flattened_metadata["tag"] = final_tags[0]

    print(f"🔍 Processing source: {flattened_metadata.get('source', 'unknown')}")
    print(f"🧾 Metadata before insert: {flattened_metadata}")

    # Create embedding
    embedding = openai.embeddings.create(
        model="text-embedding-3-small",
        input=content,
        dimensions=1536
    ).data[0].embedding

    collection.add(
        documents=[content],
        metadatas=[flattened_metadata],
        ids=[str(uuid4())],
        embeddings=[embedding],
    )

print(f"✅ Successfully ingested {len(chunks)} chunks into ChromaDB.")