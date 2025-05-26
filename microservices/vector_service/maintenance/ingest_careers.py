import json
import os
from pathlib import Path
from uuid import uuid4
from chromadb import PersistentClient

# Import shared embedding function
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "vector_service"))
from maintenance.embeddings import get_embedding

# Use same path logic as other scripts
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "/app/chroma_db")
CHUNKS_PATH = Path(__file__).parent / "mn_careers_chunks.jsonl"

print(f"🔧 Using ChromaDB path: {CHROMA_DB_PATH}")
print(f"📁 Loading chunks from: {CHUNKS_PATH}")

# Connect to ChromaDB
client = PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name="xavigate_knowledge")

print(f"📊 Initial collection count: {collection.count()}")

# Check if chunks file exists
if not CHUNKS_PATH.exists():
    print(f"❌ File not found: {CHUNKS_PATH}")
    exit(1)

# Load JSONL chunks
chunks = []
failed_lines = []

for i, line in enumerate(CHUNKS_PATH.read_text(encoding="utf-8").splitlines(), start=1):
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
        content = chunk.get("content") or chunk.get("text")
        if not content:
            print(f"⚠️ Skipping chunk {i+1}: no 'content' or 'text'")
            failed_adds.append(i+1)
            continue

        raw_metadata = dict(chunk.get("metadata", {}))

        # Show progress for first few and every 25 chunks
        if i < 3 or (i + 1) % 25 == 0:
            print(f"🔍 Processing chunk {i+1}/{len(chunks)}: {raw_metadata.get('source', 'unknown')}")
            print(f"  Content length: {len(content)} chars")

        # Flatten metadata (preserve existing logic)
        flattened_metadata = {}
        for k, v in raw_metadata.items():
            if isinstance(v, dict):
                for subkey, subval in v.items():
                    flat_key = f"{k}_{subkey}".replace(" ", "_")
                    flattened_metadata[flat_key] = subval
            elif isinstance(v, list):
                flattened_metadata[k] = " ".join(str(item) for item in v)
                if k in ("tags", "clusters"):
                    flattened_metadata[k[:-1]] = v[0] if v else "uncategorized"
            else:
                flattened_metadata[k] = v

        # Fallback tag logic (preserve existing logic)
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

        # Show metadata for first few chunks
        if i < 3:
            print(f"🧾 Flattened metadata: {flattened_metadata}")

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
            metadatas=[flattened_metadata],
            ids=[str(uuid4())],
            embeddings=[embedding],
        )

        successful_adds += 1

        # Progress indicator
        if (i + 1) % 50 == 0:
            print(f"🟢 Progress: {i+1}/{len(chunks)} chunks processed ({successful_adds} successful)")

    except Exception as e:
        print(f"❌ Error processing chunk {i+1}: {e}")
        failed_adds.append(i+1)
        continue

# Final verification
final_count = collection.count()
print(f"\n✅ MN Careers ingestion complete!")
print(f"📊 Chunks processed: {successful_adds}/{len(chunks)}")
print(f"📊 Final collection count: {final_count}")

if failed_adds:
    print(f"❌ Failed chunks: {len(failed_adds)} (IDs: {failed_adds[:10]}...)")

# Verify some careers data exists
if final_count > 0:
    try:
        # Look for careers-specific data
        careers_sample = collection.get(
            where={"tag": "careers"},
            limit=3
        )
        if careers_sample['ids']:
            print(f"📄 Careers sample IDs: {careers_sample['ids']}")
        else:
            # Fall back to general sample
            sample = collection.get(limit=3)
            print(f"📄 Sample document IDs: {sample['ids']}")
            if sample['metadatas']:
                print(f"📄 Sample metadata: {sample['metadatas'][0]}")
    except Exception as e:
        print(f"⚠️ Could not retrieve sample: {e}")

print(f"🎉 Successfully ingested {successful_adds} MN careers chunks into ChromaDB!")