import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_hebrew(settings):
    # Ensure we have a valid API key for testing
    assert settings.OPENAI_API_KEY is not None, "OpenAI API key is not set"
    
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "שלום",
            "language": "he"
        }
    )
    assert response.status_code == 200
    assert "response" in response.json()
    assert isinstance(response.json()["response"], str)
    assert len(response.json()["response"]) > 0
    assert "שלום" in response.json()["response"].lower()
