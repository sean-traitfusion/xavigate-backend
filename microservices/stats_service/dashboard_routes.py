import os
from typing import Optional, Dict, Any
from fastapi import APIRouter, Form, HTTPException, Header
from fastapi.responses import HTMLResponse, JSONResponse
import httpx

from dashboards.base_template import get_base_template
from dashboards.config_dashboard import get_config_dashboard_content
from dashboards.logging_dashboard import get_logging_dashboard_content

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
async def dashboard_home():
    """Main dashboard page - shows config dashboard by default."""
    # Show empty config - will be loaded via AJAX
    content = get_config_dashboard_content({})
    return get_base_template("System Configuration", content, "config")

@router.post("/", response_class=HTMLResponse)
async def handle_action(
    action: str = Form(...),
    auth_token: Optional[str] = Form(None),
    test_message: Optional[str] = Form(None),
):
    """Handle form actions - but ONLY for test, not save."""
    
    # For test action, just run the test and return result
    if action == "test" and auth_token and test_message:
        try:
            payload = {
                "userId": "debug-user",
                "username": "test",
                "fullName": "Admin Tester",
                "traitScores": {"creative": 7, "logical": 6, "emotional": 8},
                "message": test_message,
                "sessionId": "debug-session",
            }
            
            async with httpx.AsyncClient() as client:
                # Seed an empty session for test
                await client.post(
                    f"{STORAGE_URL}/api/memory/session-memory",
                    json={
                        "uuid": "debug-session",
                        "conversation_log": {"exchanges": []}
                    }
                )
                
                # Run test query
                auth_header = auth_token if auth_token.startswith("Bearer ") else f"Bearer {auth_token}"
                query_resp = await client.post(
                    f"{CHAT_URL}/query",
                    headers={"Authorization": auth_header},
                    json=payload
                )
                
                if query_resp.status_code == 200:
                    test_output = query_resp.json().get("answer", "[No answer returned]")
                else:
                    test_output = f"[Error {query_resp.status_code}]: {query_resp.text}"
        except Exception as e:
            test_output = f"Test failed: {str(e)}"
        
        # Return the dashboard with test output
        content = get_config_dashboard_content({}, test_output=test_output)
        return get_base_template("System Configuration", content, "config")
    
    # For other actions, just reload
    return await dashboard_home()

@router.post("/api/save-config", response_class=JSONResponse)
async def save_config_ajax(request: Dict[str, Any]):
    """Save configuration via AJAX - separate endpoint."""
    auth_token = request.get("auth_token")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Auth token required")
    
    # Remove auth_token from config
    config = {k: v for k, v in request.items() if k != "auth_token"}
    
    # Ensure both uppercase and lowercase keys are saved
    if "system_prompt" in config:
        config["SYSTEM_PROMPT"] = config["system_prompt"]
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{STORAGE_URL}/api/memory/runtime-config",
            headers=headers,
            json=config
        )
        
        if resp.status_code == 200:
            return {"status": "success", "message": "Configuration saved successfully"}
        else:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

@router.get("/logging", response_class=HTMLResponse)
async def logging_dashboard():
    """Logging dashboard page."""
    content = get_logging_dashboard_content()
    return get_base_template("Logging & Metrics", content, "logging")

@router.get("/usage", response_class=HTMLResponse)
async def usage_dashboard():
    """Usage stats dashboard (placeholder)."""
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
    return get_base_template("Usage Stats", content, "usage")

@router.get("/health", response_class=HTMLResponse)
async def health_dashboard():
    """Health monitor dashboard (placeholder)."""
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
    return get_base_template("Health Monitor", content, "health")