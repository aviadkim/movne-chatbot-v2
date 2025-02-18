from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Movne Chatbot"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"

    MODEL_PATH: Path = Path("models/hebrew-model")
    KNOWLEDGE_BASE_PATH: Path = Path("data/knowledge_base")
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/movne"
    
    # Ollama settings
    OLLAMA_HOST: str = "http://ollama:11434"  # Updated to use Docker service name
    OLLAMA_MODEL: str = "mistral"  # or another model that supports Hebrew/English

    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SERVER: str = "db"  # Added this line to match docker-compose service name
    POSTGRES_PORT: int = 5432

    # Security
    SECRET_KEY: str

    # Optionally configure the settings class
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"  # Moved the extra allow setting here
    )


settings = Settings()
