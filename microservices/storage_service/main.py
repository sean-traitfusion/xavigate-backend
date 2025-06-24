from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from memory.routes_enhanced import router as memory_router
from session.aq_routes import router as aq_router
from session.session_routes import router as session_router
from session.user_profile_routes import router as profile_router
from logging_routes import router as logging_router
# from admin.admin_dashboard import router as admin_router  # Temporarily disabled

import os
from dotenv import load_dotenv


# Load .env from root and service-level
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)

service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(dotenv_path=service_env, override=True)

# Determine environment
ENV = os.getenv("ENV", "dev")
# root_path = "/api/storage" if ENV == "prod" else ""

app = FastAPI(
    title="Storage Service",
    description="Memory and session storage service",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"url": "openapi.json"}
    # root_path=root_path
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Register routes
# Memory service endpoints
app.include_router(memory_router, prefix="/api/memory")
# Alignment Quotient (AQ) routes
app.include_router(aq_router, prefix="/aq")
app.include_router(session_router, prefix="/session")
app.include_router(profile_router, prefix="/profile")
# Logging endpoints
app.include_router(logging_router, prefix="/api/logging")
# Admin dashboard - temporarily disabled
# app.include_router(admin_router)

@app.on_event("startup")
async def startup_event():
    """Initialize database and load configuration on startup."""
    # Initialize memory tables first
    from memory.db import initialize_memory_tables
    initialize_memory_tables()
    
    # Load configuration from database
    try:
        from config.config_persistence import load_config_from_db, init_config_tables
        init_config_tables()  # Ensure config tables exist
        load_config_from_db()
        print("✅ Loaded configuration from database on startup", flush=True)
    except Exception as e:
        print(f"⚠️ Could not load persisted config on startup: {e}", flush=True)
        import traceback
        traceback.print_exc()

@app.get("/health")
def health():
    return {"status": "ok", "service": "storage"}