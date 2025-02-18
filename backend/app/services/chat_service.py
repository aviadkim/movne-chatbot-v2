from typing import Optional, Dict
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from app.core.config import settings
import logging
from app.services.rag_service import RAGService

logger = logging.getLogger(__name__)

class AdvancedChatService:  # שינינו את השם מ-ChatService ל-AdvancedChatService
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.rag_service = RAGService()
        self.initialize_model()
        
    def initialize_model(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.MODEL_NAME,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    async def process_message(
        self,
        message: str,
        language: str = "he",
        context: Optional[Dict] = None
    ) -> str:
        try:
            # Get relevant context from RAG
            relevant_docs = await self.rag_service.get_relevant_docs(message, language)
            
            # Create prompt
            system_prompt = self._get_system_prompt(language)
            context_text = "\n".join(relevant_docs) if relevant_docs else ""
            
            full_prompt = f"{system_prompt}\nContext: {context_text}\n\nUser: {message}\nAssistant:"
            
            # Generate response
            inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7,
                do_sample=True
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up response
            response = response.split("Assistant:")[-1].strip()
            
            return response

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def _get_system_prompt(self, language: str) -> str:
        if language == "he":
            return """אתה נציג שירות מקצועי של חברת מובנה גלובל, המתמחה במוצרים פיננסיים מובנים.
            תפקידך לספק מידע מדויק ומקצועי על המוצרים והשירותים שלנו."""
        else:
            return """You are a professional service representative of Movne Global.
            Your role is to provide accurate information about structured financial products."""
