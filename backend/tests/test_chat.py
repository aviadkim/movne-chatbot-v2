import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_hebrew():
    response = client.post(
        "/api/v1/chat",  # Updated to match the API prefix
        json={
            "message": "שלום",
            "language": "he"
        }
    )
    assert response.status_code == 200
    assert "response" in response.json()
    assert "language" in response.json()
    assert response.json()["language"] == "he"
