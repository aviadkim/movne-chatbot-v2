from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Movne Chatbot V2"
    API_V1_STR: str = "/api/v1"
    COMPOSE_PROJECT_NAME: str = "movne-chatbot-v2"
    
    # Database settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "changeme")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "movne")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    DATABASE_URL: str | None = None
    
    # Model settings
    MODEL_PATH: Path = Path("models")
    KNOWLEDGE_BASE_PATH: Path = Path("data/knowledge_base")
    HUGGINGFACE_TOKEN: str | None = os.getenv("HUGGINGFACE_TOKEN")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development_key")
    
    # Railway specific settings
    PORT: int = int(os.getenv("PORT", 8000))
    RAILWAY_STATIC_URL: str | None = None
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
