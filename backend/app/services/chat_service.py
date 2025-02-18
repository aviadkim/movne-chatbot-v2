import logging
from typing import Dict, Any
from .rag_service import RAGService

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.rag_service = RAGService()
        self.logger = logging.getLogger(__name__)

    async def process_message(self, message: str, language: str = "he") -> str:
        try:
            # Get relevant context
            context = self.rag_service.get_relevant_context(message)
            
            # Create response based on context
            if context:
                context_text = "\n".join(context)
                response = f"Based on context:\n{context_text}\n\nResponse: {message}"
            else:
                response = f"No relevant context found. Query: {message}"
                
            if language == "he":
                # Add Hebrew-specific processing here
                pass
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            raise

    def add_knowledge(self, texts: list[str], metadata: list[dict] = None):
        """Add knowledge to the RAG system"""
        return self.rag_service.add_documents(texts, metadata)
