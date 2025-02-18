from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    PROJECT_NAME: str = "Movne Global Chatbot"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"

    MODEL_PATH: Path = Path("models/hebrew-model")
    KNOWLEDGE_BASE_PATH: Path = Path("data/knowledge_base")

    class Config:
        case_sensitive = True


settings = Settings()
