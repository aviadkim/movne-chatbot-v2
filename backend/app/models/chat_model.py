import logging
import httpx
from typing import List, Dict
from ..core.config import settings

logger = logging.getLogger(__name__)

class MovneChat:
    def __init__(self):
        try:
            self.ollama_host = settings.OLLAMA_HOST or "http://localhost:11434"
            self.model_name = "mistral"  # Using Mistral for good multilingual support
            
            # Initialize conversation history
            self.conversation_history: List[Dict[str, str]] = []
            self.max_history_length = 5  # Keep last 5 exchanges
            
            # Configure tokenizer settings
            self.tokenizer_config = {
                "pad_token": "[PAD]",
                "padding_side": "right",
                "truncation": True,
                "max_length": 512
            }
            
            # Test connection to Ollama
            self._test_ollama_connection()
            logger.info("Chat model initialized successfully with Ollama")
            
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            raise

    def _test_ollama_connection(self):
        try:
            with httpx.Client() as client:
                response = client.get(f"{self.ollama_host}/api/tags")
                response.raise_for_status()
                logger.info("Successfully connected to Ollama service")
        except Exception as e:
            logger.error(f"Failed to connect to Ollama service: {str(e)}")
            raise

    def _create_prompt(self, message: str, language: str) -> str:
        system_prompt = (
            "You are a knowledgeable financial advisor specializing in structured investment products. "
            "Respond in the same language as the user's message. "
            "Keep responses clear, accurate, and focused on structured investments."
        )
        
        if language == "he":
            system_prompt += " השב בעברית בצורה ברורה ומקצועית."
        
        # Format conversation history
        conversation = ""
        for entry in self.conversation_history[-self.max_history_length * 2:]:
            conversation += f"{entry['role']}: {entry['content']}\n"
        
        return f"{system_prompt}\n\nConversation history:\n{conversation}\nUser: {message}\nAssistant:"

    def _clean_response(self, response: str) -> str:
        # Remove any 'Assistant:' prefix if present
        if response.startswith("Assistant:"):
            response = response[len("Assistant:"):].strip()
        return response.strip()

    def generate_response(self, message: str, language: str = "he", is_qualified: bool = False) -> str:
        try:
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            if len(self.conversation_history) > self.max_history_length * 2:
                self.conversation_history = self.conversation_history[-self.max_history_length * 2:]
            
            prompt = self._create_prompt(message, language)
            
            # Call Ollama API with tokenizer configuration
            with httpx.Client() as client:
                response = client.post(
                    f"{self.ollama_host}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.95,
                            "top_k": 50,
                            "pad_token": self.tokenizer_config["pad_token"],
                            "padding": True,
                            "max_length": self.tokenizer_config["max_length"]
                        }
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                generated_text = result.get("response", "")
                cleaned_response = self._clean_response(generated_text)
                
                # Add response to conversation history
                self.conversation_history.append({"role": "assistant", "content": cleaned_response})
                
                return cleaned_response

        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            error_msg = "שגיאת תקשורת. אנא נסה שוב." if language == "he" else "Communication error. Please try again."
            return error_msg
        except Exception as e:
            error_msg = "שגיאה בייצור תשובה. אנא נסה שוב." if language == "he" else "Error generating response. Please try again."
            logger.error(f"Error generating response: {str(e)}")
            return error_msg

    def is_initialized(self) -> bool:
        """Check if the chat model is properly initialized and connected to Ollama"""
        try:
            self._test_ollama_connection()
            return True
        except Exception as e:
            logger.error(f"Model initialization check failed: {str(e)}")
            return False
