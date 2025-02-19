import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app.services.chat_service import ChatService

async def test_bilingual_chat():
    print("Initializing chat service...")
    try:
        chat = ChatService()
        
        # Test English
        print("\nTesting English responses...")
        en_questions = [
            "What are structured products?",
            "How do alternative investments work?",
            "Can you explain the benefits of diversification?",
            "What is the minimum investment amount?"
        ]
        
        for question in en_questions:
            try:
                print(f"\nQuestion: {question}")
                response = await chat.process_message(question, 'en')
                print(f"Response: {response}")
                await asyncio.sleep(1)  # Add small delay between requests
            except Exception as e:
                print(f"Error processing English question: {e}")
        
        # Test Hebrew
        print("\nTesting Hebrew responses...")
        he_questions = [
            "מה הם מוצרים מובנים?",
            "איך עובדות השקעות אלטרנטיביות?",
            "האם תוכל להסביר את היתרונות של פיזור השקעות?",
            "מה סכום ההשקעה המינימלי?"
        ]
        
        for question in he_questions:
            try:
                print(f"\nQuestion: {question}")
                response = await chat.process_message(question, 'he')
                print(f"Response: {response}")
                await asyncio.sleep(1)  # Add small delay between requests
            except Exception as e:
                print(f"Error processing Hebrew question: {e}")
    
    except Exception as e:
        print(f"\nError initializing chat service: {e}")
        print("Please ensure all required models are properly configured and accessible.")

if __name__ == '__main__':
    asyncio.run(test_bilingual_chat())