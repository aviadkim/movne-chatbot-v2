from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Allow all origins by default
    ALLOWED_ORIGINS: str = "*"
    # Set default values for required fields
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "development_key"
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
