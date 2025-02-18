from typing import List
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def process_message(self, message: str, language: str = "he") -> str:
        try:
            # TODO: Implement actual chat logic
            return f"Processed message: {message} in {language}"
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            raise
