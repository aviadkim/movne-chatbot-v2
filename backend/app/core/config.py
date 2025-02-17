from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Movne Global Chatbot"
    MODEL_PATH: str = "models/hebrew-model"
    KNOWLEDGE_BASE_PATH: str = "data/knowledge_base"
    
    class Config:
        case_sensitive = True

settings = Settings()
