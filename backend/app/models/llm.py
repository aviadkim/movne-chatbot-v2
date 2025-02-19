from transformers import pipeline, AutoTokenizer
import logging

logger = logging.getLogger(__name__)

class SimpleChat:
    def __init__(self):
        # Using a smaller, open-source model that doesn't require login
        self.model_name = "Helsinki-NLP/opus-mt-en-he"
        try:
            self.translator = pipeline("translation", model=self.model_name)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            # Fallback to simple responses if model fails
            self.translator = None

    def generate_response(self, message: str, language: str = "he") -> str:
        try:
            if language == "he":
                base_response = "תודה על שאלתך בנוגע להשקעות ומוצרים מובנים. "
                return base_response + f"שאלתך: {message}"
            else:
                return f"Thank you for your question about structured investments. Your query: {message}"
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "שירות הצ'אט זמני לא זמין. אנא נסה שוב מאוחר יותר."

# Initialize the model once as a global instance
chat_model = SimpleChat()
