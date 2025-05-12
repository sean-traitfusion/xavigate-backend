import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure chat_service folder is on PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from main import app

client = TestClient(app)

def test_openapi_json():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    # Ensure basic OpenAPI structure
    assert "paths" in data
    assert "/chat" in data["paths"]

def test_chat_success():
    payload = {
        "prompt": "Hello, world!",
        "user_id": "user1",
        "top_k": 2,
        "tags": "tag1,tag2"
    }
    headers = {"X-XAVIGATE-KEY": "valid_key"}
    response = client.post("/chat", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    # Expected response shape
    assert isinstance(data.get("answer"), str)
    assert isinstance(data.get("sources"), list)
    assert isinstance(data.get("plan"), dict)
    assert isinstance(data.get("critique"), str)
    assert isinstance(data.get("followup"), str)

def test_chat_unauthorized():
    payload = {"prompt": "Test without key"}
    # Provide empty key to trigger verify_key == False
    headers = {"X-XAVIGATE-KEY": ""}
    response = client.post("/chat", json=payload, headers=headers)
    assert response.status_code == 401
    data = response.json()
    assert data.get("detail") == "Invalid API key"