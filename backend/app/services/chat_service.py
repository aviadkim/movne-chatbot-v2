from ..models.chat_model import MovneChat
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        try:
            self.chat_model = MovneChat()
            logger.info("Chat service initialized successfully")
            self.initialized = True
        except Exception as e:
            logger.error(f"Error initializing chat service: {str(e)}")
            self.initialized = False

    async def process_message(self, message: str, language: str = "he", is_qualified: bool = False) -> str:
        if not self.initialized:
            error_msg = "שירות הצ'אט זמני לא זמין. אנא נסה שוב מאוחר יותר." if language == "he" else "Service temporarily unavailable. Please try again later."
            logger.error(f"Attempted to process message but service is not initialized: {error_msg}")
            return error_msg

        try:
            logger.info(f"Processing message in {language} language, qualified investor: {is_qualified}")
            response = self.chat_model.generate_response(message, language, is_qualified)
            return response.strip()

        except Exception as e:
            error_msg = "שגיאה בייצור תשובה. אנא נסה שוב." if language == "he" else "Error generating response. Please try again."
            logger.error(f"Error processing message: {str(e)}")
            return error_msg
