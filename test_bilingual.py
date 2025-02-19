import os
from dotenv import load_dotenv
from backend.app.models.chat_model import MovneChat

# Load environment variables
load_dotenv()

def test_bilingual_chat():
    try:
        # Initialize chat model
        chat = MovneChat()
        
        # Test Hebrew
        print("\n=== Testing Hebrew Response ===")
        hebrew_query = "שלום, אני מעוניין לשמוע על המוצרים המובנים שלכם"
        print(f"Query: {hebrew_query}")
        hebrew_response = chat.generate_response(hebrew_query, "he")
        print(f"Response: {hebrew_response}\n")
        
        # Test English
        print("=== Testing English Response ===")
        english_query = "Hello, I would like to learn about your structured products"
        print(f"Query: {english_query}")
        english_response = chat.generate_response(english_query, "en")
        print(f"Response: {english_response}")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    test_bilingual_chat()