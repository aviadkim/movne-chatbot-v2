import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.chat_service import AdvancedChatService

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_hebrew():
    response = client.post("/api/chat", json={"message": "שלום", "language": "he"})
    assert response.status_code == 200
    assert "response" in response.json()


def test_chat_english():
    response = client.post("/api/chat", json={"message": "hello", "language": "en"})
    assert response.status_code == 200
    assert "response" in response.json()
