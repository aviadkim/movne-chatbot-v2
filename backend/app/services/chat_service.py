
from typing import Dict, Optional
from app.memory.memory_store import MemoryStore
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from app.core.config import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AdvancedChatService:
    def __init__(self):
        self.memory = MemoryStore(settings.MEMORY_DIR)
        self.load_model()
        
    def load_model(self):
        """טעינת המודל והטוקנייזר"""
        try:
            # טעינת המודל מקומית
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.MODEL_PATH,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_PATH)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    async def process_message(
        self,
        client_id: str,
        message: str,
        language: str = "he",
        context: Optional[Dict] = None
    ) -> Dict:
        """עיבוד הודעה מהמשתמש"""
        try:
            # שליפת היסטוריה והקשר
            client_history = self.memory.get_client_history(
                client_id=client_id,
                limit=5,
                language=language
            )
            client_profile = self.memory.get_client_profile(client_id)

            # בניית פרומפט
            prompt = self.build_prompt(
                message=message,
                history=client_history,
                profile=client_profile,
                language=language
            )

            # יצירת תשובה
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=settings.MAX_NEW_TOKENS,
                pad_token_id=self.tokenizer.eos_token_id
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # שמירת השיחה בזיכרון
            self.memory.add_conversation(
                client_id=client_id,
                message=message,
                response=response,
                language=language,
                metadata=context
            )

            # עדכון פרופיל לקוח
            self.update_client_profile(client_id, message, response, language)

            return {
                "response": response,
                "client_id": client_id,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise

    def build_prompt(
        self,
        message: str,
        history: list,
        profile: Optional[Dict],
        language: str
    ) -> str:
        """בניית פרומפט חכם עם היסטוריה והקשר"""
        system_prompt = self.get_system_prompt(language)
        
        context = f"\nClient Profile: {profile}" if profile else ""
        history_text = "\n".join([
            f"User: {h['message']}\nAssistant: {h['response']}"
            for h in history
        ])

        return f"{system_prompt}{context}\n\nChat History:\n{history_text}\n\nUser: {message}\nAssistant:"

    def get_system_prompt(self, language: str) -> str:
        """קבלת פרומפט מערכת בהתאם לשפה"""
        if language == "he":
            return """אתה עוזר וירטואלי מתקדם של חברת מובנה גלובל, המתמחה במוצרים פיננסיים מובנים.
            עליך לספק מידע מדויק ומקצועי, תוך שמירה על שיחה טבעית ואמפתית.
            
            הנחיות חשובות:
            - שמור על שפה מקצועית אך ידידותית
            - התאם את התשובות להיסטוריה של הלקוח
            - הימנע ממתן המלצות השקעה ספציפיות
            - הדגש תמיד את חשיבות הייעוץ המקצועי"""
        else:
            return """You are an advanced virtual assistant for Movne Global, specializing in structured financial products.
            Provide accurate and professional information while maintaining a natural and empathetic conversation.
            
            Important guidelines:
            - Maintain professional yet friendly language
            - Adapt responses to client history
            - Avoid giving specific investment advice
            - Always emphasize the importance of professional consultation"""

    def update_client_profile(
        self,
        client_id: str,
        message: str,
        response: str,
        language: str
    ):
        """עדכון פרופיל לקוח על בסיס השיחה"""
        try:
            current_profile = self.memory.get_client_profile(client_id) or {}
            
            # עדכון מידע בסיסי
            current_profile.update({
                "last_interaction": datetime.utcnow().isoformat(),
                "preferred_language": language,
                "interaction_count": current_profile.get("interaction_count", 0) + 1
            })
            
            self.memory.update_client_profile(client_id, current_profile)
        except Exception as e:
            logger.error(f"Error updating client profile: {str(e)}")
