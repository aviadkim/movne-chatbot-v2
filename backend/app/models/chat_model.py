from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging

logger = logging.getLogger(__name__)

class MovneChat:
    def __init__(self):
        try:
            model_name = "mistralai/Mistral-7B-Instruct-v0.2"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                load_in_8bit=True
            )
            logger.info("Mistral model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = None
            self.tokenizer = None

    def generate_response(self, message: str, language: str = "he") -> str:
        if not self.model or not self.tokenizer:
            return "שירות הצ'אט זמני לא זמין. אנא נסה שוב מאוחר יותר."

        try:
            prompt = self._create_prompt(message, language)
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return self._clean_response(response)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "שגיאה בייצור תשובה. אנא נסה שוב."

    def _create_prompt(self, message: str, language: str) -> str:
        if language == "he":
            return f"""<s>[INST] אתה יועץ מומחה למוצרים מובנים והשקעות אלטרנטיביות. 
            ענה בעברית על השאלה הבאה בצורה מקצועית ומפורטת:
            {message} [/INST]</s>"""
        return f"""<s>[INST] You are an expert advisor in structured products and alternative investments.
        Please answer the following question professionally and in detail:
        {message} [/INST]</s>"""

    def _clean_response(self, response: str) -> str:
        # Remove the prompt and get only the model's response
        parts = response.split("[/INST]")
        return parts[-1].strip() if len(parts) > 1 else response.strip()

chat_model = MovneChat()
