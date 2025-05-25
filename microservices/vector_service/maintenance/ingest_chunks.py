import json
from pathlib import Path
from chromadb import PersistentClient
from openai import OpenAI
from uuid import uuid4

# Load your Chroma collection (edit path if needed)
client = PersistentClient(path="../chroma_db")
collection = client.get_or_create_collection(name="xavigate_knowledge")

# Load chunks from file
chunks = []
# chunks_path = Path(__file__).parent / "bulk_chunks_all_cleaned.jsonl"
chunks_path = Path("../../docs/kb/careers/mn_careers_chunks.jsonl") 
chunks = []

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
    # Support both "text" and legacy "content" keys
    content = chunk.get("content") or chunk.get("text")
    if not content:
        print("⚠️ Skipping chunk with no 'content' or 'text'")
        continue

    metadata = dict(chunk.get("metadata", {}))
    tag_list = metadata.get("tags", [])

    print(f"🔍 Processing source: {metadata.get('source', 'unknown')}")
    print(f"  Original tags: {repr(tag_list)} (type: {type(tag_list)})")

    if isinstance(tag_list, list):
        final_tags = tag_list
    elif isinstance(tag_list, str):
        final_tags = tag_list.split() if tag_list.strip() else []
    else:
        print(f"  ⚠️ Unexpected tag format: {type(tag_list)}")
        final_tags = []

    if not final_tags:
        print(f"  ⚠️ No tags found, using fallback")
        final_tags = ["uncategorized"]

    metadata["tags"] = " ".join(final_tags)
    metadata["tag"] = final_tags[0]

    print(f"🧾 Metadata before insert: {metadata}")

    embedding = openai.embeddings.create(
        model="text-embedding-3-small",
        input=content,
        dimensions=1536
    ).data[0].embedding

    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[str(uuid4())],
        embeddings=[embedding],
    )

print(f"✅ Successfully ingested {len(chunks)} chunks into ChromaDB.")
