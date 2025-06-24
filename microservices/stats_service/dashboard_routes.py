import os
from typing import Optional, Dict, Any
from fastapi import APIRouter, Form, HTTPException, Header, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
import httpx

from dashboards.base_template import get_base_template
from dashboards.config_dashboard import get_config_dashboard_content
from dashboards.logging_dashboard import get_logging_dashboard_content
from dashboards.login_page import get_login_page_content
from auth_utils import (
    get_current_user, require_auth, create_auth_url, generate_code_verifier,
    generate_code_challenge, store_pkce_verifier, get_and_clear_pkce_verifier,
    exchange_code_for_tokens, decode_id_token, generate_session_id,
    store_session, create_session_cookie, clear_session_cookie,
    create_logout_url, clear_session, BASE_URL
)

router = APIRouter()

# Get service URLs from environment
# In Docker, services communicate using service names
ENV = os.getenv("ENV", "dev")
if ENV == "prod" or os.path.exists("/.dockerenv"):
    # Running in Docker container
    STORAGE_URL = os.getenv("STORAGE_SERVICE_URL", "http://storage_service:8011")
    CHAT_URL = os.getenv("CHAT_SERVICE_URL", "http://chat_service:8015")
else:
    # Running locally
    STORAGE_URL = os.getenv("STORAGE_SERVICE_URL", "http://localhost:8011")
    CHAT_URL = os.getenv("CHAT_SERVICE_URL", "http://localhost:8015")

@router.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """Main dashboard page - shows config dashboard by default."""
    # Check authentication
    user = await get_current_user(request)
    if not user and ENV == "prod":
        return RedirectResponse(url=f"{BASE_URL}/login", status_code=303)
    
    # Try to load current config from storage service
    current_config = {}
    try:
        async with httpx.AsyncClient() as client:
            # In production, use the user's token for API calls
            headers = {}
            if ENV == "prod" and user:
                session_id = request.cookies.get("xavigate_admin_session")
                if session_id:
                    from auth_utils import get_session
                    session = get_session(session_id)
                    if session and "tokens" in session:
                        headers["Authorization"] = f"Bearer {session['tokens']['access_token']}"
            
            resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config", headers=headers)
            if resp.status_code == 200:
                current_config = resp.json()
    except Exception as e:
        print(f"Could not load config: {e}")
    
    content = get_config_dashboard_content(current_config)
    return get_base_template("System Configuration", content, "config", user)

@router.post("/", response_class=HTMLResponse)
async def handle_action(
    request: Request,
    action: str = Form(...),
):
    """Handle form actions."""
    # Check authentication
    user = await get_current_user(request)
    if not user and ENV == "prod":
        return RedirectResponse(url=f"{BASE_URL}/login", status_code=303)
    
    # For now, just reload the dashboard
    # All saving is handled via AJAX
    return await dashboard_home(request)

@router.post("/api/save-config", response_class=JSONResponse)
async def save_config_ajax(request: Request, config_data: Dict[str, Any]):
    """Save configuration via AJAX - for admin dashboard use."""
    # Check authentication
    user = await get_current_user(request)
    if not user and ENV == "prod":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    config = config_data
    
    # Ensure both uppercase and lowercase keys are saved for compatibility
    if "system_prompt" in config:
        config["SYSTEM_PROMPT"] = config["system_prompt"]
    
    # Use the user's token for API calls
    headers = {}
    if ENV == "prod" and user:
        session_id = request.cookies.get("xavigate_admin_session")
        if session_id:
            from auth_utils import get_session
            session = get_session(session_id)
            if session and "tokens" in session:
                headers["Authorization"] = f"Bearer {session['tokens']['access_token']}"
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{STORAGE_URL}/api/memory/runtime-config",
            headers=headers,
            json=config
        )
        
        if resp.status_code == 200:
            return {"status": "success", "message": "Configuration saved successfully"}
        else:
            # Try without auth for local development
            if ENV != "prod":
                resp = await client.post(
                    f"{STORAGE_URL}/api/memory/runtime-config",
                    json=config
                )
                if resp.status_code == 200:
                    return {"status": "success", "message": "Configuration saved successfully"}
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

@router.post("/api/reset-defaults", response_class=JSONResponse)
async def reset_config_to_defaults(request: Request):
    """Reset configuration to system defaults."""
    # Check authentication
    user = await get_current_user(request)
    if not user and ENV == "prod":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Use the user's token for API calls
    headers = {}
    if ENV == "prod" and user:
        session_id = request.cookies.get("xavigate_admin_session")
        if session_id:
            from auth_utils import get_session
            session = get_session(session_id)
            if session and "tokens" in session:
                headers["Authorization"] = f"Bearer {session['tokens']['access_token']}"
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{STORAGE_URL}/api/memory/config-reset-defaults",
            headers=headers,
            json={"user_id": user.get("email", "unknown") if user else "unknown"}
        )
        
        if resp.status_code == 200:
            return {"status": "success", "message": "Configuration reset to defaults successfully"}
        else:
            # Try without auth for local development
            if ENV != "prod":
                resp = await client.post(
                    f"{STORAGE_URL}/api/memory/config-reset-defaults",
                    json={"user_id": "unknown"}
                )
                if resp.status_code == 200:
                    return {"status": "success", "message": "Configuration reset to defaults successfully"}
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

@router.get("/logging", response_class=HTMLResponse)
async def logging_dashboard(request: Request):
    """Logging dashboard page."""
    # Check authentication
    user = await get_current_user(request)
    if not user and ENV == "prod":
        return RedirectResponse(url=f"{BASE_URL}/login", status_code=303)
    
    content = get_logging_dashboard_content()
    return get_base_template("Logging & Metrics", content, "logging", user)

@router.get("/usage", response_class=HTMLResponse)
async def usage_dashboard(request: Request):
    """Usage stats dashboard (placeholder)."""
    # Check authentication
    user = await get_current_user(request)
    if not user and ENV == "prod":
        return RedirectResponse(url=f"{BASE_URL}/login", status_code=303)
    
    content = """
        <div class="content-header">
            <h2>Usage Statistics</h2>
            <p>Track system usage and performance metrics</p>
        </div>
        
        <div class="card">
            <h3>Coming Soon</h3>
            <p style="color: #666;">This dashboard will display usage statistics and analytics.</p>
        </div>
    """
    return get_base_template("Usage Stats", content, "usage", user)

@router.get("/health", response_class=HTMLResponse)
async def health_dashboard(request: Request):
    """Health monitor dashboard (placeholder)."""
    # Check authentication
    user = await get_current_user(request)
    if not user and ENV == "prod":
        return RedirectResponse(url=f"{BASE_URL}/login", status_code=303)
    
    content = """
        <div class="content-header">
            <h2>Health Monitor</h2>
            <p>Monitor system health and service status</p>
        </div>
        
        <div class="card">
            <h3>Coming Soon</h3>
            <p style="color: #666;">This dashboard will display service health status and monitoring data.</p>
        </div>
    """
    return get_base_template("Health Monitor", content, "health", user)

# Authentication routes
@router.get("/login", response_class=HTMLResponse)
async def login_page(error: Optional[str] = None):
    """Display login page."""
    return get_login_page_content(error)

@router.get("/auth/login", response_class=RedirectResponse)
async def initiate_login():
    """Initiate Cognito login flow."""
    # Generate PKCE challenge
    verifier = generate_code_verifier()
    challenge = generate_code_challenge(verifier)
    
    # Generate state for CSRF protection
    state = generate_session_id()
    
    # Store verifier for later use
    store_pkce_verifier(state, verifier)
    
    # Create auth URL and redirect
    auth_url = create_auth_url(state, challenge)
    return RedirectResponse(url=auth_url)

@router.get("/auth/callback", response_class=HTMLResponse)
async def auth_callback(
    request: Request,
    response: Response,
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    error_description: Optional[str] = None
):
    """Handle Cognito callback."""
    # Check for errors
    if error:
        error_msg = error_description or error
        return RedirectResponse(url=f"{BASE_URL}/login?error={error_msg}")
    
    if not code or not state:
        return RedirectResponse(url=f"{BASE_URL}/login?error=Missing code or state")
    
    # Get PKCE verifier
    verifier = get_and_clear_pkce_verifier(state)
    if not verifier:
        return RedirectResponse(url=f"{BASE_URL}/login?error=Invalid state")
    
    try:
        # Exchange code for tokens
        tokens = await exchange_code_for_tokens(code, verifier)
        
        # Decode ID token to get user info
        user_info = decode_id_token(tokens["id_token"])
        
        # Create session
        session_id = generate_session_id()
        store_session(session_id, tokens, user_info)
        
        # Set session cookie
        redirect_response = RedirectResponse(url=BASE_URL, status_code=303)
        create_session_cookie(redirect_response, session_id)
        
        return redirect_response
        
    except Exception as e:
        print(f"Auth callback error: {e}")
        return RedirectResponse(url=f"{BASE_URL}/login?error=Authentication failed")

@router.get("/logout", response_class=RedirectResponse)
async def logout(request: Request, response: Response):
    """Logout user and clear session."""
    # Clear session
    session_id = request.cookies.get("xavigate_admin_session")
    if session_id:
        clear_session(session_id)
    
    # Clear cookie
    logout_response = RedirectResponse(url=create_logout_url())
    clear_session_cookie(logout_response)
    
    return logout_response