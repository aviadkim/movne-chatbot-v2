from pydantic import BaseSettings
from dotenv import load_dotenv
import os
load_dotenv()
class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    ENVIRONMENT: str = 'development'
    class Config:
        fields = {'OPENAI_API_KEY': {'exclude': True}}
