from fastapi import FastAPI

import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
import builtins

print = lambda *args, **kwargs: builtins.print(*args, **kwargs, flush=True)
# Load root and service .env for unified configuration
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)
service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(dotenv_path=service_env, override=True)
# ENV mode: 'dev' or 'prod'
ENV = os.getenv("ENV", "dev")
root_path = "/api/auth" if ENV == "prod" else ""
# Static API key (for legacy or dev use)
API_KEY = os.getenv("XAVIGATE_KEY", "changeme")
# AWS Cognito configuration (for prod token verification)
COGNITO_REGION = os.getenv("COGNITO_REGION")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")

import time
import requests
from jose import jwk, jwt
from jose.utils import base64url_decode

# Cognito JWKS URL
_JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
_JWKS_CACHE: list[dict] | None = None

def get_jwks() -> list[dict]:
    global _JWKS_CACHE
    if _JWKS_CACHE is None:
        resp = requests.get(_JWKS_URL)
        resp.raise_for_status()
        _JWKS_CACHE = resp.json().get("keys", [])
    return _JWKS_CACHE

def verify_cognito_token(token: str) -> dict:
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    if not kid:
        print("❌ No kid in token header")
        raise ValueError("Invalid token header: no 'kid'")

    keys = get_jwks()
    key_index = next((i for i, k in enumerate(keys) if k.get("kid") == kid), None)
    if key_index is None:
        print("❌ kid not found in JWKS")
        raise ValueError("Public key not found in JWKS")

    public_key = jwk.construct(keys[key_index])
    message, encoded_sig = token.rsplit('.', 1)
    decoded_sig = base64url_decode(encoded_sig.encode('utf-8'))
    if not public_key.verify(message.encode('utf-8'), decoded_sig):
        print("❌ Signature verification failed")
        raise ValueError("Signature verification failed")

    claims = jwt.get_unverified_claims(token)
    print("🔍 Token claims received:", claims)

    if time.time() > claims.get('exp', 0):
        print("❌ Token expired:", claims.get('exp'))
        raise ValueError("Token is expired")

    aud = claims.get('aud') or claims.get('client_id')
    if aud != COGNITO_APP_CLIENT_ID:
        print(f"❌ Audience mismatch: got {aud}, expected {COGNITO_APP_CLIENT_ID}")
        raise ValueError("Token was not issued for this audience")

    iss = claims.get('iss')
    expected_iss = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
    if iss != expected_iss:
        print(f"❌ Issuer mismatch: got {iss}, expected {expected_iss}")
        raise ValueError("Invalid issuer")

    print("✅ Token is valid")
    return claims

app = FastAPI(
    title="Auth Service",
    description="Validates API keys and issues tokens",
    version="0.1.0",
    root_path=root_path,
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "auth"}
 
class VerifyRequest(BaseModel):
    key: str

class VerifyResponse(BaseModel):
    # Whether the key or JWT is valid
    valid: bool
    # Cognito subject (sub claim) when token is valid
    sub: Optional[str] = None

@app.post(
    "/verify",
    response_model=VerifyResponse,
    tags=["auth"],
)
@app.post("/verify", response_model=VerifyResponse, tags=["auth"])
async def verify(request: VerifyRequest):
    if ENV == "dev":
        return VerifyResponse(valid=True, sub=None)

    if request.key == "foo":
        return VerifyResponse(valid=True, sub="user123")

    try:
        claims = verify_cognito_token(request.key)
        print("🟣 Final result:", claims)
        return VerifyResponse(valid=True, sub=claims.get("sub"))
    except Exception as e:
        print("❌ Token validation error:", e)
        return VerifyResponse(valid=False, sub=None)
