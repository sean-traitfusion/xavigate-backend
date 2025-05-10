# 🧠 Embedding Procedure – `rag_service`

This guide explains how to embed glossary and main content chunks into Chroma using the `rag_service` microservice. It supports both local development and production Docker environments.

---

## 📁 Project Structure

Ensure the following layout is present in `microservices/rag_service/`:

```
rag_service/
├── maintenance/
│   ├── chunking.py
│   ├── embeddings.py
│   ├── ingest_glossary.py
│   ├── ingest_chunks.py
│   ├── data/
│   │   └── bulk_chunks_all_cleaned.jsonl
│   └── vectorstore.py
├── shared/
│   └── cache/
│       └── embedding_cache.json
├── docs/
│   └── kb/
│       └── glossary/
│           └── glossary.jsonl
```

---

## 📦 Python Requirements

Update `rag_service/requirements.txt` with the following:

```
# Database & Environment
psycopg2-binary
python-dotenv

# Document parsing
python-docx
pandas

# Embedding / RAG stack
openai
chromadb
langchain
tiktoken
tenacity
numpy

# Web service (optional, for FastAPI endpoints)
fastapi
uvicorn[standard]
pydantic

# CLI & utilities
tqdm
```

Install inside Docker using:

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

---

## ▶️ Running the Embedding Scripts

From your host machine:

```bash
docker exec -it xavigate_rag_service /bin/bash
cd /app

# Embed glossary terms
python3 maintenance/ingest_glossary.py

# Embed main document chunks
python3 maintenance/ingest_chunks.py
```

> `ingest_chunks.py` reads from:
```
/app/maintenance/data/bulk_chunks_all_cleaned.jsonl
```

Each line should already be cleaned and chunked.

---

## ⚙️ How It Works

- **prepare_chunks()** (used in glossary): detects file type and creates chunk metadata
- **get_embedding()**: sends content to OpenAI and caches results
- **store_embeddings()**: inserts embedded chunks into Chroma
- **embedding_cache.json**: local cache to avoid repeated API calls

Ensure this cache file exists and is writable:

```python
EMBEDDING_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
EMBEDDING_CACHE_PATH.touch(exist_ok=True)
```

---

## ❗ Common Issues

| Problem                                 | Solution                                                    |
|----------------------------------------|-------------------------------------------------------------|
| `0 chunks loaded`                      | Ensure `glossary.jsonl` uses `"term"` and `"definition"` fields |
| `No such file or directory`            | Ensure `shared/cache/embedding_cache.json` exists           |
| `ModuleNotFoundError`                  | Check `requirements.txt` and rebuild the container          |
| `glossary.jsonl` missing               | Re-run the CSV to JSONL converter before ingestion          |

---

## ✅ Expected Output

When successful:

```
→ Embedding chunk 1/38: 3591 chars
✅ Stored 38 embedded chunks in Chroma
```

You're now ready to power RAG-based retrieval, guided alignment, or frontend QA workflows.
