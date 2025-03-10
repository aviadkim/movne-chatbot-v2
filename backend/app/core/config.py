from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os
from urllib.parse import quote_plus
from typing import Union
from functools import lru_cache

class Settings(BaseSettings):
    # OpenAI settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_TEMPERATURE: float = 0.7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='allow',
        secrets=["OPENAI_API_KEY"]  # Exclude API key from logs
    )

    @property
    def validate_openai_key(self) -> str:
        """Validate and return the OpenAI API key"""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set in environment variables")
        return self.OPENAI_API_KEY
    # Project settings
    PROJECT_NAME: str = "Movne Chatbot V2"
    API_V1_STR: str = "/api/v1"
    COMPOSE_PROJECT_NAME: str = "movne-chatbot-v2"
    
    # Database settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "changeme")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "movne")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    DATABASE_URL: Union[str, None] = None
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development_key")
    
    # Railway specific settings
    PORT: int = int(os.getenv("PORT", 8000))
    RAILWAY_STATIC_URL: Union[str, None] = None
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    @property
    def validate_environment(self) -> str:
        """Validate and return the environment setting"""
        valid_environments = ["development", "production", "test"]
        if self.ENVIRONMENT not in valid_environments:
            raise ValueError(f"ENVIRONMENT must be one of {valid_environments}")
        return self.ENVIRONMENT
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='allow'
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure password is properly URL encoded
        encoded_password = quote_plus(self.POSTGRES_PASSWORD)
        self.DATABASE_URL = os.getenv("DATABASE_URL") or \
            f"postgresql://{self.POSTGRES_USER}:{encoded_password}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

settings = Settings()
