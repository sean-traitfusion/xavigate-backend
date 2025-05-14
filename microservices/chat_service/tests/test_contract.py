import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure chat_service folder is on PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import main
# Stub out external calls for contract tests
main.verify_key = lambda token: True
main.rag_query = lambda prompt, top_k=None, tags=None: "stub response"
from main import app

client = TestClient(app)

def test_openapi_json():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    # Ensure basic OpenAPI structure
    assert "paths" in data
    assert "/query" in data["paths"]

def test_chat_success():
    payload = {
        "userId": "user1",
        "username": "user1",
        "fullName": "User One",
        "traitScores": {"creative": 8.0},
        "message": "Hello, world!",
        "sessionId": "session1"
    }
    headers = {"Authorization": "Bearer valid_key"}
    response = client.post("/query", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    # Expected response shape
    assert isinstance(data.get("answer"), str)
    assert isinstance(data.get("sources"), list)
    assert isinstance(data.get("plan"), dict)
    assert isinstance(data.get("critique"), str)
    assert isinstance(data.get("followup"), str)

def test_chat_unauthorized():
    payload = {
        "userId": "user1",
        "username": "user1",
        "traitScores": {"creative": 5.0},
        "message": "Test without token",
        "sessionId": "session1"
    }
    # Missing or invalid Authorization header
    headers = {"Authorization": ""}
    response = client.post("/query", json=payload, headers=headers)
    assert response.status_code == 401
    data = response.json()
    assert data.get("detail") == "Invalid or missing Authorization header"