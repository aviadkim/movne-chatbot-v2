from typing import Optional
from ..models.chat_model import MovneChat
from ..core.config import Settings
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.settings = Settings()
        self.initialized = False
        try:
            self.chat_model = MovneChat()
            logger.info("Chat service initialized successfully")
            self.initialized = True
        except Exception as e:
            logger.error(f"Error initializing chat service: {str(e)}")
            self.initialized = False

    def _log_chat_interaction(self, message: str, response: str, language: str, error: Optional[str] = None):
        """Log chat interactions for monitoring and analytics"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "language": language,
            "message_length": len(message),
            "response_length": len(response),
            "error": error,
            "environment": self.settings.ENVIRONMENT
        }
        logger.info(f"Chat interaction: {json.dumps(log_entry)}")

    async def process_message(self, message: str, language: str = "he", is_qualified: bool = False) -> str:
        if not self.initialized:
            error_msg = "שירות הצ'אט זמני לא זמין. אנא נסה שוב מאוחר יותר." if language == "he" else "Service temporarily unavailable. Please try again later."
            logger.error(f"Attempted to process message but service is not initialized")
            self._log_chat_interaction(message, error_msg, language, "Service not initialized")
            return error_msg

        try:
            logger.info(f"Processing message in {language} language, qualified investor: {is_qualified}")
            response = self.chat_model.generate_response(message, language)
            response = response.strip()
            self._log_chat_interaction(message, response, language)
            return response

        except Exception as e:
            error_msg = "שגיאה בייצור תשובה. אנא נסה שוב." if language == "he" else "Error generating response. Please try again."
            logger.error(f"Error processing message: {str(e)}")
            self._log_chat_interaction(message, error_msg, language, str(e))
            return error_msg
