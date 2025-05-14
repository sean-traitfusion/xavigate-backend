import os
from fastapi import FastAPI
from dotenv import load_dotenv
from analytics_routes import router as analytics_router

# Load .env from root and service-level
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)

service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(dotenv_path=service_env, override=True)

# Determine environment
ENV = os.getenv("ENV", "dev")
root_path = "/api/stats" if ENV == "prod" else ""

app = FastAPI(
    title="Stats Service",
    description="Analytics and statistics service",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"url": "openapi.json"},
    root_path=root_path,
)

app.include_router(analytics_router, prefix="/stats")

@app.get("/health")
def health():
    return {"status": "ok", "service": "stats"}