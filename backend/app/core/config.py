from pydantic_settings import BaseSettings
from pathlib import Path
import secrets

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Movne Global Advanced Chatbot"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MODEL_PATH: Path = BASE_DIR / "models" / "mistral-7b-hebrew"
    MEMORY_DIR: Path = BASE_DIR / "data" / "memory"
    PROFILES_DIR: Path = BASE_DIR / "data" / "client_profiles"
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "movne_chatbot_v2"
    
    # Memory Settings
    MEMORY_BACKEND: str = "chroma"  # או 'redis' או 'milvus'
    MEMORY_RETENTION_DAYS: int = 90
    
    # Model Settings
    MODEL_TYPE: str = "mistral"
    CONTEXT_WINDOW: int = 4096
    MAX_NEW_TOKENS: int = 512
    
    # Language Settings
    DEFAULT_LANGUAGE: str = "he"
    SUPPORTED_LANGUAGES: list = ["he", "en"]

    class Config:
        case_sensitive = True

settings = Settings()
