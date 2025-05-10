from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from prompt_engine.prompt_routes import router as prompt_router
from query import query_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register RAG routes
# app.include_router(prompt_router, prefix="/prompts")
app.include_router(query_router, prefix="/query")  #backward compatibility
app.include_router(query_router, prefix="/rag") 

@app.get("/health")
def health():
    return {"status": "ok", "service": "rag"}