from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

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
    
    # Security
    SECRET_KEY: str = "development_key"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='allow'
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DATABASE_URL = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

settings = Settings()
