from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from memory.routes import router as memory_router
from session.aq_routes import router as aq_router
from session.session_routes import router as session_router
from session.user_profile_routes import router as profile_router

import os
from contextlib import asynccontextmanager
import time
from threading import Thread
from memory.routes import expire_session_logic
from db_service.db import get_connection
from dotenv import load_dotenv


# Load .env from root and service-level
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)

service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(dotenv_path=service_env, override=True)

# Determine environment
ENV = os.getenv("ENV", "dev")
root_path = "/api/storage" if ENV == "prod" else ""

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Background thread to expire stale sessions every hour
    def periodic_expire():
        interval = int(os.getenv("SESSION_EXPIRE_INTERVAL_SEC", "3600"))
        while True:
            time.sleep(interval)
            try:
                conn = get_connection()
                conn.autocommit = True
                cur = conn.cursor()
                cur.execute("SELECT uuid FROM session_memory WHERE expires_at < NOW()")
                rows = cur.fetchall()
                cur.close()
                conn.close()
                for (user_uuid,) in rows:
                    try:
                        expire_session_logic(str(user_uuid))
                    except Exception as e:
                        print(f"Error expiring session {user_uuid}: {e}")
            except Exception as e:
                print(f"Error during periodic expiration: {e}")
    Thread(target=periodic_expire, daemon=True).start()
    print("🕒 Session expiration cron started")
    yield
    # Teardown if needed

app = FastAPI(
    lifespan=lifespan,
    title="Storage Service",
    description="Memory and session storage service",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"url": "openapi.json"},
    root_path=root_path,)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Register routes
# Memory service endpoints
app.include_router(memory_router, prefix="/memory")
# Alignment Quotient (AQ) routes
app.include_router(aq_router, prefix="/aq")
app.include_router(session_router, prefix="/session")
app.include_router(profile_router, prefix="/profile")

@app.get("/health")
def health():
    return {"status": "ok", "service": "storgage"}