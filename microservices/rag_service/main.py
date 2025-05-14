import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
# from prompt_engine.prompt_routes import router as prompt_router
from query import query_router

# Load .env from root and service-level
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)

service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(dotenv_path=service_env, override=True)

# Determine environment
ENV = os.getenv("ENV", "dev")
root_path = "/api/rag" if ENV == "prod" else ""


app = FastAPI(
    title="Rag Service",
    description="Querying and retrieving data from RAG",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"url": "openapi.json"},
    root_path=root_path,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register RAG routes
# app.include_router(prompt_router, prefix="/prompts")
app.include_router(query_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "rag"}
