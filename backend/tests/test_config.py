import os
from app.core.config import Settings

def test_settings_openai_loading():
    """Test if Settings class properly loads OpenAI configurations"""
    settings = Settings()
    assert settings.OPENAI_API_KEY is not None, "Settings failed to load OPENAI_API_KEY"
    assert settings.OPENAI_MODEL is not None, "Settings failed to load OPENAI_MODEL"
    assert settings.OPENAI_TEMPERATURE is not None, "Settings failed to load OPENAI_TEMPERATURE"

def test_database_url_generation():
    """Test if database URL is properly generated"""
    settings = Settings()
    assert settings.DATABASE_URL is not None, "Database URL was not generated"
    assert "postgresql://" in settings.DATABASE_URL, "Database URL is not in PostgreSQL format"

def test_environment_settings():
    """Test if environment settings are properly loaded"""
    settings = Settings()
    assert settings.ENVIRONMENT in ["development", "production", "test"], "Invalid environment setting"
    assert settings.PORT is not None, "Port setting is not loaded"
    assert settings.SECRET_KEY is not None, "Secret key is not loaded"