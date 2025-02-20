from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
from typing import Union

class Settings(BaseSettings):
    # OpenAI settings
    OPENAI_API_KEY: str = "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"
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    OPENAI_TEMPERATURE: float = 0.7
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
