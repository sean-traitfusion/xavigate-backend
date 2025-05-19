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
chunks_path = Path(__file__).parent / "bulk_chunks_all_cleaned.jsonl"

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
    metadata = dict(chunk["metadata"])
    
    # Get tags from metadata - they should be stored as lists
    tag_list = metadata.get("tags", [])
    
    # Debug: Print what we got
    print(f"🔍 Processing source: {metadata.get('source', 'unknown')}")
    print(f"  Original tags: {repr(tag_list)} (type: {type(tag_list)})")
    
    # Handle different tag formats
    if isinstance(tag_list, list):
        # Tags are already a list - this is the expected format
        final_tags = tag_list
    elif isinstance(tag_list, str):
        # Tags are a string - split on spaces
        final_tags = tag_list.split() if tag_list.strip() else []
    else:
        # Unexpected format
        print(f"  ⚠️ Unexpected tag format: {type(tag_list)}")
        final_tags = []
    
    # Ensure we have at least one tag
    if not final_tags:
        print(f"  ⚠️ No tags found, using fallback")
        final_tags = ["uncategorized"]
    
    print(f"  Final tags: {final_tags}")
    
    # Update metadata for ChromaDB
    metadata["tags"] = " ".join(final_tags)  # ChromaDB expects space-separated string
    metadata["tag"] = final_tags[0]          # Primary tag for easier filtering
    
    print(f"🧾 Metadata before insert: {metadata}")
    
    embedding = openai.embeddings.create(
        model="text-embedding-3-small",
        input=content,
        dimensions=1536  # Explicitly set to match API
    ).data[0].embedding
    
    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[str(uuid4())],
        embeddings=[embedding],
    )

print(f"✅ Successfully ingested {len(chunks)} chunks into ChromaDB.")