from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Movne Global Chatbot"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432  # הוספנו את זה
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres123"
    POSTGRES_DB: str = "movne_chatbot_v2"
    
    # Model settings
    MODEL_NAME: str = "mistralai/Mistral-7B-v0.1"
    MODEL_PATH: Path = Path("models/mistral")
    
    # Knowledge Base
    KNOWLEDGE_BASE_PATH: Path = Path("data/knowledge_base")
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    
    class Config:
        case_sensitive = True

settings = Settings()
