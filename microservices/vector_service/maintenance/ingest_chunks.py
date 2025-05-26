import json
import os
from pathlib import Path
from chromadb import PersistentClient
from uuid import uuid4

# Import shared embedding function
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "vector_service"))
from maintenance.embeddings import get_embedding

# Use same path logic as other scripts
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "/app/chroma_db")
client = PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name="xavigate_knowledge")

print(f"🔧 Using ChromaDB path: {CHROMA_DB_PATH}")
print(f"📊 Initial collection count: {collection.count()}")

# Load chunks from file
chunks_path = Path(__file__).parent / "bulk_chunks_all_cleaned.jsonl"
print(f"📁 Loading chunks from: {chunks_path}")

if not chunks_path.exists():
    print(f"❌ File not found: {chunks_path}")
    exit(1)

chunks = []
failed_lines = []

for i, line in enumerate(chunks_path.read_text(encoding="utf-8").splitlines(), start=1):
    clean_line = line.strip().replace('\u2028', ' ').replace('\u2029', ' ')
    if not clean_line:
        continue
    try:
        chunks.append(json.loads(clean_line))
    except json.JSONDecodeError as e:
        print(f"⚠️ Skipping malformed line {i}: {e}")
        failed_lines.append(i)

print(f"📄 Loaded {len(chunks)} chunks ({len(failed_lines)} failed)")
if failed_lines:
    print(f"❌ Failed lines: {failed_lines[:10]}...")  # Show first 10

if not chunks:
    print("❌ No valid chunks found!")
    exit(1)

# Ingest loop with progress tracking
successful_adds = 0
failed_adds = []

for i, chunk in enumerate(chunks):
    try:
        # Support both "text" and legacy "content" keys
        content = chunk.get("content") or chunk.get("text")
        if not content:
            print(f"⚠️ Skipping chunk {i+1}: no 'content' or 'text'")
            failed_adds.append(i+1)
            continue

        metadata = dict(chunk.get("metadata", {}))
        tag_list = metadata.get("tags", [])

        # Show progress for first few and every 50 chunks
        if i < 3 or (i + 1) % 50 == 0:
            print(f"🔍 Processing chunk {i+1}/{len(chunks)}: {metadata.get('source', 'unknown')}")
            print(f"  Content length: {len(content)} chars")
            print(f"  Tags: {tag_list} (type: {type(tag_list)})")

        # Normalize tags
        if isinstance(tag_list, list):
            final_tags = tag_list
        elif isinstance(tag_list, str):
            final_tags = tag_list.split() if tag_list.strip() else []
        else:
            if i < 3:  # Only warn for first few
                print(f"  ⚠️ Unexpected tag format: {type(tag_list)}")
            final_tags = []

        if not final_tags:
            final_tags = ["uncategorized"]

        metadata["tags"] = " ".join(final_tags)
        metadata["tag"] = final_tags[0]

        # Generate embedding using shared function
        try:
            embedding = get_embedding(content)
        except Exception as e:
            print(f"❌ Embedding error for chunk {i+1}: {e}")
            failed_adds.append(i+1)
            continue

        # Validate embedding
        if not isinstance(embedding, list) or len(embedding) != 1536:
            print(f"❌ Invalid embedding for chunk {i+1}: type={type(embedding)}, len={len(embedding) if hasattr(embedding, '__len__') else 'N/A'}")
            failed_adds.append(i+1)
            continue

        # Add to collection
        collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[str(uuid4())],
            embeddings=[embedding],
        )

        successful_adds += 1

        # Progress indicator
        if (i + 1) % 100 == 0:
            print(f"🟢 Progress: {i+1}/{len(chunks)} chunks processed ({successful_adds} successful)")

    except Exception as e:
        print(f"❌ Error processing chunk {i+1}: {e}")
        failed_adds.append(i+1)
        continue

# Final verification
final_count = collection.count()
print(f"\n✅ Bulk ingestion complete!")
print(f"📊 Chunks processed: {successful_adds}/{len(chunks)}")
print(f"📊 Final collection count: {final_count}")

if failed_adds:
    print(f"❌ Failed chunks: {len(failed_adds)} (IDs: {failed_adds[:10]}...)")

# Verify some data exists
if final_count > 0:
    try:
        sample = collection.get(limit=3)
        print(f"📄 Sample document IDs: {sample['ids']}")
        if sample['metadatas']:
            print(f"📄 Sample metadata: {sample['metadatas'][0]}")
    except Exception as e:
        print(f"⚠️ Could not retrieve sample: {e}")

print(f"🎉 Successfully ingested {successful_adds} chunks into ChromaDB!")