from fastapi import FastAPI

import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
# ENV mode: 'dev' or 'prod'
ENV = os.getenv("ENV", "dev")
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
    # Decode header to get kid
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    if not kid:
        raise ValueError("Invalid token header: no 'kid'")
    # Fetch JWKs and find matching key
    keys = get_jwks()
    key_index = next((i for i, k in enumerate(keys) if k.get("kid") == kid), None)
    if key_index is None:
        raise ValueError("Public key not found in JWKS")
    public_key = jwk.construct(keys[key_index])
    # Verify signature
    message, encoded_sig = token.rsplit('.', 1)
    decoded_sig = base64url_decode(encoded_sig.encode('utf-8'))
    if not public_key.verify(message.encode('utf-8'), decoded_sig):
        raise ValueError("Signature verification failed")
    # Validate claims
    claims = jwt.get_unverified_claims(token)
    # Check expiration
    if time.time() > claims.get('exp', 0):
        raise ValueError("Token is expired")
    # Check audience (app client id)
    aud = claims.get('aud') or claims.get('client_id')
    if aud != COGNITO_APP_CLIENT_ID:
        raise ValueError("Token was not issued for this audience")
    # Check issuer
    iss = claims.get('iss')
    expected_iss = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
    if iss != expected_iss:
        raise ValueError("Invalid issuer")
    return claims

app = FastAPI(
    title="Auth Service",
    description="Validates API keys and issues tokens",
    version="0.1.0",
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "auth"}
 
class VerifyRequest(BaseModel):
    key: str

class VerifyResponse(BaseModel):
    valid: bool

@app.post(
    "/verify",
    response_model=VerifyResponse,
    tags=["auth"],
)
async def verify(request: VerifyRequest):
    """
    Verify that the provided API key (X-XAVIGATE-KEY) is valid.
    """
    # Development mode: simple stub
    if ENV == "dev":
        return VerifyResponse(valid=(request.key == API_KEY))
    # Production mode: verify as Cognito JWT
    try:
        verify_cognito_token(request.key)
        return VerifyResponse(valid=True)
    except Exception:
        return VerifyResponse(valid=False)