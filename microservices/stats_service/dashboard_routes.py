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
    # Try to load current config from storage service
    current_config = {}
    try:
        async with httpx.AsyncClient() as client:
            # Try to get config without auth for local development
            resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config")
            if resp.status_code == 200:
                current_config = resp.json()
    except Exception as e:
        print(f"Could not load config: {e}")
    
    content = get_config_dashboard_content(current_config)
    return get_base_template("System Configuration", content, "config")

@router.post("/", response_class=HTMLResponse)
async def handle_action(
    action: str = Form(...),
):
    """Handle form actions."""
    # For now, just reload the dashboard
    # All saving is handled via AJAX
    return await dashboard_home()

@router.post("/api/save-config", response_class=JSONResponse)
async def save_config_ajax(request: Dict[str, Any]):
    """Save configuration via AJAX - for admin dashboard use."""
    # In a production environment, you would validate admin access here
    # For now, we'll save directly to the storage service
    
    config = request
    
    # Ensure both uppercase and lowercase keys are saved for compatibility
    if "system_prompt" in config:
        config["SYSTEM_PROMPT"] = config["system_prompt"]
    
    # For dashboard access, we can use a system token or no auth if running locally
    headers = {}
    if ENV == "prod":
        # In production, you'd use a system token or validate admin session
        headers = {"Authorization": "Bearer system-admin-token"}
    
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