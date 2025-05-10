# ingest_onboarding_docs.py
from maintenance.chunking import prepare_chunks
from maintenance.embeddings import get_embedding
from maintenance.vectorstore import store_embeddings
import os


def embed_chunks(chunks):
    embedded = []
    for i, chunk in enumerate(chunks):
        content = chunk["content"]
        metadata = chunk.get("metadata", {})

        print(f"→ Embedding chunk {i+1}/{len(chunks)}: {len(content)} chars")

        try:
            vector = get_embedding(content)
        except Exception as e:
            print(f"❌ Error embedding chunk {i}: {e}")
            continue

        embedded.append({
            "id": f'onboarding_{i}',
            "content": content,
            "embedding": vector,
            "metadata": metadata,
        })
    return embedded

ONBOARDING_DOCS = [
    "docs/Xavigate Onboarding Developer Manual - v0.2.md",
    # "docs/Xavigate Architecture, Trait Measurement and Onboarding.md"
]

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ONBOARDING_DOCS = [
    BASE_DIR / "docs/Xavigate Architecture, Trait Measurement and Onboarding.md"
]

def main():
    all_chunks = []
    for filepath in ONBOARDING_DOCS:
        if not filepath.exists():
            print(f"File not found: {filepath}")
            continue
        print(f"Processing: {filepath}")
        chunks = prepare_chunks(filepath)
        all_chunks.extend(chunks)
    
    if not all_chunks:
        print("No chunks created.")
        return

    print("Embedding chunks...")
    embedded = embed_chunks(all_chunks)

    print("Storing embeddings...")
    store_embeddings(embedded)
    print("Done.")

if __name__ == "__main__":
    main()