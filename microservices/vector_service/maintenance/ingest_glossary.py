from maintenance.chunking import prepare_chunks
from maintenance.embeddings import get_embedding
from maintenance.vectorstore import store_embeddings
from pathlib import Path

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
            "id": f'glossary_{i}',
            "content": content,
            "embedding": vector,
            "metadata": metadata,
        })
    return embedded

def ingest_all_data():
    data_root = Path("docs/kb/glossary")
    doc_paths = list(data_root.rglob("*.docx")) + list(data_root.rglob("*.jsonl"))

    for path in doc_paths:
        print(f"Ingesting: {path}")
        chunks = prepare_chunks(str(path))
        print(f"→ {len(chunks)} raw chunks loaded")
        embedded = embed_chunks(chunks)
        store_embeddings(embedded)

if __name__ == "__main__":
    ingest_all_data()
if __name__ == "__main__":
    ingest_all_data()