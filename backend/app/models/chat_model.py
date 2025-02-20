import logging
from typing import List, Dict
from openai import OpenAI
from ..core.config import settings

logger = logging.getLogger(__name__)

class MovneChat:
    def __init__(self):
        try:
            # Initialize OpenAI client with the API key from settings
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.model_name = settings.OPENAI_MODEL
            self.temperature = settings.OPENAI_TEMPERATURE
            
            # Initialize conversation history
            self.conversation_history: List[Dict[str, str]] = []
            self.max_history_length = 5  # Keep last 5 exchanges
            
            logger.info("Chat model initialized successfully with OpenAI")
            
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            raise
    
    def is_initialized(self) -> bool:
        return hasattr(self, 'client') and self.client is not None
    
    def generate_response(self, message: str, language: str = "he") -> str:
        try:
            if not self.is_initialized():
                raise Exception("Chat model not properly initialized")
            
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": message})
            
            # Prepare system message based on language
            system_message = {
                "role": "system",
                "content": "You are a helpful assistant. Please respond in Hebrew." if language == "he" else "You are a helpful assistant."
            }
            
            # Prepare messages for the API call
            messages = [system_message] + self.conversation_history[-self.max_history_length:]
            
            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature
            )
            
            # Extract and store assistant's response
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

chat_model = MovneChat()
