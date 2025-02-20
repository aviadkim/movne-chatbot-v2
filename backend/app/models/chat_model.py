import logging
from typing import List, Dict
from openai import OpenAI
from ..core.config import settings

logger = logging.getLogger(__name__)

class MovneChat:
    def __init__(self):
        try:
            # Initialize OpenAI client
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
        return bool(settings.OPENAI_API_KEY)

    def _create_messages(self, message: str, language: str) -> List[Dict[str, str]]:
        system_prompt = (
            "You are a knowledgeable financial advisor specializing in structured investment products. "
            "Respond in the same language as the user's message. "
            "Keep responses clear, accurate, and focused on structured investments."
        )
        
        if language == "he":
            system_prompt += " השב בעברית בצורה ברורה ומקצועית."
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history
        for entry in self.conversation_history[-self.max_history_length * 2:]:
            messages.append({
                "role": entry["role"],
                "content": entry["content"]
            })
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        return messages

    def generate_response(self, message: str, language: str = "he", is_qualified: bool = False) -> str:
        try:
            # Update conversation history with user message
            self.conversation_history.append({"role": "user", "content": message})
            if len(self.conversation_history) > self.max_history_length * 2:
                self.conversation_history = self.conversation_history[-self.max_history_length * 2:]
            
            messages = self._create_messages(message, language)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=1000,
                n=1,
                stop=None
            )
            
            # Extract and clean response
            generated_text = response.choices[0].message.content.strip()
            
            # Add response to conversation history
            self.conversation_history.append({"role": "assistant", "content": generated_text})
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

chat_model = MovneChat()
