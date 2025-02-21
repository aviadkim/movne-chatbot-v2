import os
import pytest
from pathlib import Path
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.config import Settings

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment variables before running tests."""
    # Load environment variables from .env file if it exists
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    # Set default test environment variables if not already set
    if not os.getenv('OPENAI_API_KEY'):
        pytest.skip('OPENAI_API_KEY environment variable is not set')
    
    # Set test-specific environment variables
    os.environ.setdefault('ENVIRONMENT', 'test')
    os.environ.setdefault('OPENAI_MODEL', 'gpt-4-turbo-preview')
    os.environ.setdefault('OPENAI_TEMPERATURE', '0.7')
    
    # Yield to allow tests to run
    yield
    
    # Cleanup after tests if needed
    # No cleanup needed for environment variables as they're process-specific

@pytest.fixture(scope="module")
def client():
    # Create a test client using the app
    with TestClient(app) as test_client:
        yield test_client