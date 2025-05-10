from chromadb import PersistentClient
from fastapi import APIRouter, Query
from maintenance.embeddings import get_embedding
from typing import Optional

query_router = APIRouter()

client = PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="xavigate_ad")

@query_router.get("/query")
def handle_query(prompt: str, top_k: int = 3, tags: Optional[str] = Query(None)):
    tag_list = tags.split(",") if tags else None
    result = rag_query(prompt, tags=tag_list, top_k=top_k)
    return {"result": result}

def rag_query(prompt: str, tags: Optional[list[str]] = None, top_k: int = 3) -> str:
    filters = {"tags": {"$in": tags}} if tags else {}
    results = run_query(prompt, top_k=top_k, filters=filters)
    return "\n\n".join([r["text"] for r in results])


def run_query(question: str, top_k=3, filters: dict = None):
    query_vector = get_embedding(question)
    filters = filters or {}

    query_args = {
        "query_embeddings": [query_vector],
        "n_results": top_k,
    }

    if filters:
        query_args["where"] = filters

    results = collection.query(**query_args)

    return [
        {
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
        }
        for i in range(len(results["documents"][0]))
    ]