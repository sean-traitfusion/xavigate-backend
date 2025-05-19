from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict
import os
import httpx
from dotenv import load_dotenv
from datetime import datetime
# Database connection
from db_service.db import get_connection

# Load root and service .env for unified configuration
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)
service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(dotenv_path=service_env, override=True)
# Environment mode (unused for MNTEST stub)
ENV = os.getenv("ENV", "dev")
root_path = "/api/mntest" if ENV == "prod" else ""
# Auth service URL for token verification
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8014")

# JWT authentication dependency
async def require_jwt(authorization: str | None = Header(None, alias="Authorization")):
    print("🔐 Incoming Authorization header:", authorization)
    # In dev mode, skip auth if header missing
    if ENV == "dev":
        return
    # In prod, require valid Bearer token
    if not authorization or not authorization.startswith("Bearer "):
        print(f"📡 Calling auth service at {AUTH_SERVICE_URL}/verify")
        raise HTTPException(status_code=401, detail="Unauthorized")
        print("🧾 Auth service response:", resp.status_code, await resp.aread())
    token = authorization.split(" ", 1)[1]
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{AUTH_SERVICE_URL}/verify", json={"key": token})
    if resp.status_code != 200 or not resp.json().get("valid", False):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# In-memory store for trait scores
_store: Dict[str, Dict[str, float]] = {}

app = FastAPI(
    title="MN Test Service",
    description="Stores and retrieves MNTEST trait scores",
    version="0.1.0",
    root_path=root_path,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from psycopg2.extras import Json

# Initialize Postgres table for MN results
try:
    # Connect via DATABASE_URL or DB_CONFIG
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS mn_results (
            user_id TEXT PRIMARY KEY,
            trait_scores JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
    )
    cur.close()
    conn.close()
except Exception:
    pass

class MNSubmitRequest(BaseModel):
    userId: str = Field(..., description="Cognito sub of the user")
    traitScores: Dict[str, float] = Field(..., description="Map of 19 trait names to scores (1-10 scale)")

class MNSubmitResponse(BaseModel):
    status: str

class MNResultResponse(BaseModel):
    userId: str
    traitScores: Dict[str, float]

@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": "mntest"}

@app.post(
    "/submit",
    response_model=MNSubmitResponse,
    tags=["mntest"],
)
async def submit_mntest(
    req: MNSubmitRequest,
    _=Depends(require_jwt),
):
    # Persist trait scores to Postgres
    try:
        conn = get_connection()
        conn.autocommit = True
        cur = conn.cursor()
        # Upsert into mn_results
        cur.execute(
            """
            INSERT INTO mn_results (user_id, trait_scores)
            VALUES (%s, %s)
            ON CONFLICT (user_id)
                DO UPDATE SET trait_scores = EXCLUDED.trait_scores, created_at = NOW();
            """,
            (req.userId, Json(req.traitScores))
        )
        cur.close()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")
    return MNSubmitResponse(status="ok")

@app.get(
    "/result",
    response_model=MNResultResponse,
    tags=["mntest"],
)
async def get_mntest_result(
    userId: str,
    _=Depends(require_jwt),
):
    # Retrieve trait scores from Postgres
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT trait_scores FROM mn_results WHERE user_id = %s", (userId,)
        )
        rec = cur.fetchone()
        cur.close()
        conn.close()
        if not rec:
            raise HTTPException(status_code=404, detail="MNTEST scores not found for user")
        scores = rec[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")
    return MNResultResponse(userId=userId, traitScores=scores)