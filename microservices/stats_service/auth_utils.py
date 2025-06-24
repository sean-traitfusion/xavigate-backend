import os
import base64
import hashlib
import secrets
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import httpx
import jwt
from fastapi import HTTPException, Request, Response
from fastapi.responses import RedirectResponse

# Cognito configuration
CLIENT_ID = os.getenv("COGNITO_CLIENT_ID", "56352i5933v40t36u1fqs2fe3e")
AUTH_DOMAIN = os.getenv("COGNITO_AUTH_DOMAIN", "https://us-east-1csh9tzfjf.auth.us-east-1.amazoncognito.com")
TOKEN_ENDPOINT = f"{AUTH_DOMAIN}/oauth2/token"
AUTHORIZE_ENDPOINT = f"{AUTH_DOMAIN}/oauth2/authorize"
LOGOUT_ENDPOINT = f"{AUTH_DOMAIN}/logout"
JWKS_URL = f"{AUTH_DOMAIN}/.well-known/jwks.json"

# Redirect URLs
if os.getenv("ENV") == "prod":
    REDIRECT_URI = "https://chat.xavigate.com/system-admin/auth/callback"
    BASE_URL = "https://chat.xavigate.com/system-admin"
else:
    REDIRECT_URI = "http://localhost:8015/dashboard/auth/callback"
    BASE_URL = "http://localhost:8015/dashboard"

# Session configuration
SESSION_COOKIE_NAME = "xavigate_admin_session"
SESSION_DURATION_HOURS = 24
SECURE_COOKIES = os.getenv("ENV") == "prod"

# Token storage (in production, use Redis or similar)
# For now, using in-memory storage
token_storage: Dict[str, Dict[str, Any]] = {}

def generate_code_verifier(length: int = 128) -> str:
    """Generate a PKCE code verifier."""
    return base64.urlsafe_b64encode(
        secrets.token_bytes(length)
    ).decode('utf-8').rstrip('=')

def generate_code_challenge(verifier: str) -> str:
    """Generate a PKCE code challenge from the verifier."""
    digest = hashlib.sha256(verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')

def generate_session_id() -> str:
    """Generate a secure session ID."""
    return secrets.token_urlsafe(32)

def create_auth_url(state: str, code_challenge: str) -> str:
    """Create the Cognito authorization URL."""
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "email openid phone",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }
    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{AUTHORIZE_ENDPOINT}?{query_string}"

async def exchange_code_for_tokens(code: str, code_verifier: str) -> Dict[str, Any]:
    """Exchange authorization code for tokens."""
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_ENDPOINT,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Token exchange failed: {response.text}"
            )
        
        return response.json()

async def refresh_tokens(refresh_token: str) -> Dict[str, Any]:
    """Refresh access token using refresh token."""
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_ENDPOINT,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Token refresh failed: {response.text}"
            )
        
        return response.json()

def decode_id_token(id_token: str) -> Dict[str, Any]:
    """Decode ID token to get user info (without verification for now)."""
    try:
        # In production, verify the token signature using JWKS
        # For now, just decode without verification
        payload = jwt.decode(id_token, options={"verify_signature": False})
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid ID token: {str(e)}")

def store_session(session_id: str, tokens: Dict[str, Any], user_info: Dict[str, Any]):
    """Store session tokens and user info."""
    token_storage[session_id] = {
        "tokens": tokens,
        "user_info": user_info,
        "created_at": datetime.utcnow(),
        "last_accessed": datetime.utcnow()
    }

def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Get session data by session ID."""
    session = token_storage.get(session_id)
    if session:
        # Check if session is expired
        if datetime.utcnow() - session["created_at"] > timedelta(hours=SESSION_DURATION_HOURS):
            del token_storage[session_id]
            return None
        # Update last accessed time
        session["last_accessed"] = datetime.utcnow()
        return session
    return None

def clear_session(session_id: str):
    """Clear session data."""
    if session_id in token_storage:
        del token_storage[session_id]

async def get_current_user(request: Request) -> Optional[Dict[str, Any]]:
    """Get current user from session cookie."""
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if not session_id:
        return None
    
    session = get_session(session_id)
    if not session:
        return None
    
    # Check if access token is expired and refresh if needed
    tokens = session["tokens"]
    if "expires_in" in tokens:
        # Simple expiry check (in production, decode the token to check exp claim)
        # For now, assume tokens expire after 1 hour
        token_age = datetime.utcnow() - session["last_accessed"]
        if token_age > timedelta(hours=1) and "refresh_token" in tokens:
            try:
                new_tokens = await refresh_tokens(tokens["refresh_token"])
                session["tokens"].update(new_tokens)
                store_session(session_id, session["tokens"], session["user_info"])
            except:
                # Refresh failed, clear session
                clear_session(session_id)
                return None
    
    return session["user_info"]

def require_auth(func):
    """Decorator to require authentication for a route."""
    async def wrapper(request: Request, *args, **kwargs):
        user = await get_current_user(request)
        if not user:
            # Redirect to login
            return RedirectResponse(url=f"{BASE_URL}/login", status_code=303)
        # Add user to request state
        request.state.user = user
        return await func(request, *args, **kwargs)
    return wrapper

def create_session_cookie(response: Response, session_id: str):
    """Create a secure session cookie."""
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        max_age=SESSION_DURATION_HOURS * 3600,
        httponly=True,
        secure=SECURE_COOKIES,
        samesite="lax"
    )

def clear_session_cookie(response: Response):
    """Clear the session cookie."""
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        secure=SECURE_COOKIES,
        samesite="lax"
    )

def create_logout_url() -> str:
    """Create the Cognito logout URL."""
    logout_uri = f"{BASE_URL}/login"
    return f"{LOGOUT_ENDPOINT}?client_id={CLIENT_ID}&logout_uri={logout_uri}"

# Storage for PKCE verifiers during auth flow
pkce_storage: Dict[str, str] = {}

def store_pkce_verifier(state: str, verifier: str):
    """Store PKCE verifier for auth flow."""
    pkce_storage[state] = verifier

def get_and_clear_pkce_verifier(state: str) -> Optional[str]:
    """Get and clear PKCE verifier."""
    return pkce_storage.pop(state, None)