import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import Settings

@pytest.fixture(scope="session")
def settings():
    # Set test environment variables
    os.environ["OPENAI_API_KEY"] = "sk-test-key"  # Use a test API key
    os.environ["ENVIRONMENT"] = "test"
    return Settings()

@pytest.fixture(scope="module")
def client(settings):
    # Create a test client using the app
    with TestClient(app) as test_client:
        yield test_client