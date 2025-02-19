from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Movne Chatbot V2"
    API_V1_STR: str = "/api/v1"
    COMPOSE_PROJECT_NAME: str = "movne-chatbot-v2"
    
    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_DB: str = "movne"
    POSTGRES_SERVER: str = "localhost"
    DATABASE_URL: str | None = None
    
    # Model settings
    MODEL_PATH: Path = Path("models")
    KNOWLEDGE_BASE_PATH: Path = Path("data/knowledge_base")
    HUGGINGFACE_TOKEN: str | None = os.getenv("HUGGINGFACE_TOKEN")
    
    # Security
    SECRET_KEY: str = "development_key"
    
    # Railway specific settings
    PORT: int = int(os.getenv("PORT", 8000))
    RAILWAY_STATIC_URL: str | None = None
    ENVIRONMENT: str = "development"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='allow'
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DATABASE_URL = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        if os.getenv("RAILWAY_STATIC_URL"):
            self.ENVIRONMENT = "production"
        # Use Railway's DATABASE_URL if provided
        self.DATABASE_URL = os.getenv("DATABASE_URL", self.DATABASE_URL)

settings = Settings()
